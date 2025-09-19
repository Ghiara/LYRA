from utils.llm_utils import (
    query_llm,
    parse_code_response,
    query_llm_structured,
    print_code,
)
from utils.cap_utils import cap_code_exec
from utils.cli_utils import *

from agents.model.skill import Skill
from agents.model.example import TaskExample
from agents.memory import MemoryManager
from agents.skill_parser import SkillParser

from collections import Counter


class Actor:
    """
    responsible for handling the main action loop
    generates policy code by dynamically composing the prompt (i.e. retrieving skills and examples),
    and rewrites code according to user feedback
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
        skill_parser: SkillParser = None,
        debug=False,
    ):
        self.debug = debug
        self.memory_manager = memory_manager
        self.skill_parser = skill_parser
        self.reset()

    def reset(self):
        self.messages = []
        self.env = None
        self.task = None
        self.lvars = {}

    def learn_skill(self, env, task, skill: Skill):
        """when we are solving a task with a given skill, we are learning the skill
        means we are both writing the skill code and the actual task-specific code
        """

        from prompts.skill_learning import (
            actor_skill_learning_system_prompt,
            skill_learning_prompt,
        )

        self.env = env
        self.task = task

        examples = self.memory_manager.example_manager.retrieve_similar_examples(
            task, num_results=5
        )

        # TODO: we tried a few retrieval strategies here, but none worked that well
        # this is a hard problem, and the current solution is more of a placeholder...
        # this ties the retrieved skills to having solved similar tasks previously
        # so if example retrieval fails, so does this, and then the agent has no chance
        # HINTS provide a simple fallback – the user can override default retrieval
        # Alternatively, we could add more autonomy for the agent to interact with its own memory
        skills = self.retrieve_task_related_skills(
            task=task, task_examples=examples, num_results=10
        )

        if self.debug:
            print_examples(examples)
            print_list([skill.name for skill in skills], "Skills")

        prompt = skill_learning_prompt(
            task=task,
            few_shot_examples=examples,
            skill=skill,
            other_useful_skills=skills,
        )

        self.messages = [
            {"role": "system", "content": actor_skill_learning_system_prompt},
            {
                "role": "user",
                "content": prompt,
            },
        ]

        code = self.write_and_run_code(self.messages)

        return code

    def attempt_task(self, env, task):
        """solves a task without a skill to be learned"""
        from prompts.actor import (
            actor_system_prompt,
            actor_prompt,
        )

        self.env = env
        self.task = task

        # need function for retrieving other potentially task-relevant skills
        examples = self.memory_manager.example_manager.retrieve_similar_examples(
            task, num_results=5
        )
        skills = self.retrieve_task_related_skills(task, num_results=10)

        if self.debug:
            print_examples(examples)
            print_list([skill.name for skill in skills], "Skills")

        prompt = actor_prompt(task=task, few_shot_examples=examples, api=skills)

        # print(prompt)

        self.messages = [
            {"role": "system", "content": actor_system_prompt},
            {
                "role": "user",
                "content": prompt,
            },
        ]

        code = self.write_and_run_code(self.messages)

        return code

    def revise_code_with_hint(self, hint: str):
        examples = self.skill_parser.apply_task_hint(hint)
        self.revise_code_with_feedback(hint, examples)

    def revise_code_with_feedback(
        self, feedback: str, examples: list[TaskExample] = []
    ):
        """code revision should be different from initial task plan - there should be a different retrieval strategy for this
        for example also finding past examples of how feedback was incorporated into a solution
        """

        from prompts.actor import actor_iteration_prompt

        self.messages.append(
            {
                "role": "user",
                "content": actor_iteration_prompt(feedback, examples),
            }
        )

        code = self.write_and_run_code(self.messages)

        return code

    def write_and_run_code(self, messages):
        response = query_llm(messages)
        code = parse_code_response(response)
        self.last_code_str = code
        self.messages.append({"role": "assistant", "content": self.last_code_str})

        if self.debug:
            debug_message(code, "Generated code")

        dependencies = self.memory_manager.skill_manager.resolve_dependencies(
            self.last_code_str
        )
        new_lvars = cap_code_exec(
            code,
            self.env,
            dependencies,
            self.lvars,
        )
        return code

    def run_last_code_str(self):
        """just run the last piece of code again"""
        dependencies = self.memory_manager.skill_manager.resolve_dependencies(
            self.last_code_str
        )
        cap_code_exec(
            self.last_code_str,
            self.env,
            dependencies,
            self.lvars,
        )
        return self.last_code_str

    def run_code_str(self, env, code):
        """run a given piece"""
        dependencies = self.memory_manager.skill_manager.resolve_dependencies(code)
        cap_code_exec(
            code,
            env,
            dependencies,
            self.lvars,
        )

    def generated_subtask_based_retrieval(self, task) -> list[Skill]:
        # generate a plan by decomposing the task into subtasks, and then retrieving a skill for each subtask
        # TODO: another sensible retrieval strategy – instead of retrieving by task similarity,
        # allow the agent to decompose into subtasks (in natural language) and retrieve based on that
        pass

    def retrieve_task_related_skills_naive(self, task, num_results=20) -> list[Skill]:
        # naive strategy: retrieve skills by
        return self.memory_manager.skill_manager.retrieve_skills(
            task, num_results=num_results
        )

    def retrieve_task_related_skills(
        self, task=None, task_examples: list[TaskExample] = None, num_results=10
    ) -> list[Skill]:
        """can specify either a task, or a list of task examples - if specifying a task, it retrieves similar tasks first"""
        similar_tasks = (
            self.memory_manager.example_manager.retrieve_similar_examples(task)
            if task_examples is None
            else task_examples
        )
        skills = self.extract_skill_calls_from_code_strings(
            [task.code for task in similar_tasks], num_results
        )

        return skills

    def retrieve_skill_related_skills(
        self, skill: Skill, num_results=10
    ) -> list[Skill]:
        similar_skills = self.memory_manager.skill_manager.retrieve_skills(
            skill.description
        )
        return self.extract_skill_calls_from_code_strings(
            [skill.code for skill in similar_skills], num_results
        )

    def extract_skill_calls_from_code_strings(
        self, codes: list[str], max_skills=10
    ) -> list[Skill]:
        """can be used either to extract from task code or from skill codes"""
        per_code_skill_calls = [
            self.memory_manager.skill_manager.get_skill_calls(code) for code in codes
        ]
        counter = Counter(
            skill_call.name
            for task_calls in per_code_skill_calls
            for skill_call in task_calls
        )
        sorted_skill_names = [skill for (skill, _) in counter.most_common(max_skills)]
        sorted_skills = [
            self.memory_manager.skill_manager.retrieve_skill_with_name(name)
            for name in sorted_skill_names
        ]
        return sorted_skills

    def retrieve_skill_related_skills_naive(self, skill: Skill):
        return self.memory_manager.retrieve_skills(skill.description)


if __name__ == "__main__":

    memory_manager = MemoryManager()
    actor = Actor(memory_manager)

    # skill = Skill.parse_function_string(code)

    # task_skills = actor.retrieve_task_related_skills("put one block next to the other")
    # skills = actor.retrieve_skill_related_skills(skill)
    # Skill.print_skills(task_skills)
    # Skill.print_skills(skills)

    # naive_task_skills = actor.retrieve_task_related_skills_naive(
    #     "put one block next to the other"
    # )
    # naive_skills = actor.retrieve_skill_related_skills_naive(skill)

    # Skill.print_skills(naive_task_skills)
    # Skill.print_skills(naive_skills)
