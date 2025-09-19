from agents.model import Skill, TaskExample
from agents.memory import MemoryManager

from utils.llm_utils import (
    query_llm,
    parse_code_response,
    format_code_to_print,
    query_llm_structured,
)
from utils.cli_utils import *
import textwrap


class SkillParser:
    """parses a python function header from the description of this function
    either by generating a new function header, or by retrieving an existing skill from the skill library
    TODO: hide python code behind a layer of natural language description, make requirements parsing more explicit
    """

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.messages = []

    def parse_skill(self) -> Skill:
        system_cli_message("SKILL PARSING")
        # First check if there is an existing similar skill, and if so prompt user to determine whether this matches
        # If not, generate a new skill based on the user input
        skill_prompt = input("Describe the skill you want to learn:\n")
        skill = self.check_for_existing_similar_skills(skill_prompt)
        if skill is None:
            skill = self.generate_skill(skill_prompt)

        skill = self.refine_skill(skill)
        return skill

    def generate_skill(self, skill_prompt):
        from prompts.parse_skill import (
            generate_function_header_system_prompt,
            generate_skill_prompt,
        )

        similar_skills = self.memory_manager.skill_manager.retrieve_skills(
            skill_prompt, num_results=5
        )

        self.messages = [
            {"role": "system", "content": generate_function_header_system_prompt},
            {
                "role": "user",
                "content": generate_skill_prompt(skill_prompt, similar_skills),
            },
        ]

        response = query_llm(self.messages)
        code = parse_code_response(response)
        self.messages.append({"role": "assistant", "content": code})
        skill = Skill.parse_function_string(code)

        return skill

    def check_for_existing_similar_skills(self, skill_prompt) -> Skill | None:
        """checks if there are any existing skills that match the skill prompt"""
        similar_skills = self.memory_manager.skill_manager.retrieve_skills(
            skill_prompt, no_core_primitives=True, num_results=5
        )
        if len(similar_skills) == 0:
            print("No similar skills found.")
            return None

        skill_descriptions = [
            format_code_to_print(skill.description) for skill in similar_skills
        ]
        choice = choice_from_input_items(
            skill_descriptions,
            "Is one of these the skill you want to learn?",
            allow_none=True,
        )

        chosen_skill = similar_skills[choice - 1] if choice is not None else None

        return chosen_skill

    def refine_skill(self, skill: Skill) -> Skill | None:
        from prompts.parse_skill import (
            refine_function_header_prompt,
            generate_function_header_system_prompt,
        )

        if len(self.messages) == 0:
            self.messages = [
                {"role": "system", "content": generate_function_header_system_prompt}
            ]

        function_code = skill.code

        while True:
            print(
                textwrap.dedent(
                    f"""
                    \n
                    \n
                The current function code is: 
                {format_code_to_print(function_code)}
                """
                )
            )

            options = [
                "Accept",
                "Feedback & Iterate",
                "Abort",
            ]

            choice = choice_from_input_items(
                options, "Proceed with the following function?"
            )
            chosen_option = options[choice - 1]

            match chosen_option:
                case "Accept":
                    skill.code = function_code
                    self.messages = []
                    return skill
                case "Feedback & Iterate":
                    refinement_input = simple_user_prompt(
                        "How would you like to refine this function?"
                    )
                    self.messages.append(
                        {
                            "role": "user",
                            "content": refine_function_header_prompt(
                                function_code, refinement_input
                            ),
                        }
                    )
                    response = query_llm(self.messages)
                    function_code = parse_code_response(response)
                    self.messages.append(
                        {"role": "assistant", "content": function_code}
                    )
                case "Abort":
                    self.messages = []
                    return None

    def apply_task_hint(self, hint) -> list[TaskExample]:
        # "this is similar to when..."
        # this represents skill **uses**

        # first split task hints within string, then perform retrieval for each
        from prompts.parse_skill import ParsedList, parse_hint_to_list_prompt

        messages = [{"role": "user", "content": parse_hint_to_list_prompt(hint)}]
        tasks = query_llm_structured(messages, ParsedList)
        task_descriptions = tasks.parsed_list

        retrieved_task_examples = []
        for task_desc in task_descriptions:
            ret_tasks = self.memory_manager.example_manager.retrieve_similar_examples(
                task_desc, num_results=5
            )
            retrieved_task_examples.extend(ret_tasks)
        return retrieved_task_examples

    def apply_skill_hint(self, hint) -> list[Skill]:
        # actually retrieves the skill objects, so that we can look inside for: this is "like" that
        # and so we can append them to the prompt, instead of appending all skills every time...

        # first split task hints within string, then perform retrieval for each
        from prompts.parse_skill import ParsedList, parse_hint_to_list_prompt

        messages = [{"role": "user", "content": parse_hint_to_list_prompt(hint)}]
        skills_object = query_llm_structured(messages, ParsedList)
        skill_descriptions = skills_object.parsed_list

        retrieved_skills = []
        for skill_desc in skill_descriptions:
            ret_skill = self.memory_manager.skill_manager.retrieve_skills(
                skill_desc, num_results=1
            )
            retrieved_skills.extend(ret_skill)

        return retrieved_skills


if __name__ == "__main__":
    skill_parser = SkillParser(MemoryManager(memory_dir="trained"))
    skill_parser.parse_skill()
    # skills = skill_parser.apply_skill_hint(
    #     "use the skills put_first_on_second and clear_blocks_from_area"
    # )
    # examples = skill_parser.apply_task_hint(
    #     "this is like when you had to build a block pyramid"
    # )
