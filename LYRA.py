from agents.memory import MemoryManager, ConfigManager
from agents.action import Actor
from agents.environment import EnvironmentAgent
# from agents.revision import RevisionAgent
from agents.skill_parser import SkillParser
from agents.model import Skill, TaskExample, InteractionTrace
# from task.task_and_store import Task

from utils.cap_utils import extract_task_and_skill_code
from utils.cli_utils import *

class LYRA:
    """
    the main agent class, initialises the necessary submodules and contains most of the CLI
    the user goes through (skill-parsing) - task-setup - task-attempt
    skill-parsing can be skipped if we just want to attempt a task based on the agents current memory
    """

    def __init__(self, memory_dir="baseline", debug=False):
        self.debug = debug

        self.memory_manager = MemoryManager(memory_dir)
        self.config_manager = ConfigManager()
        self.env_agent = EnvironmentAgent(
            memory_manager=self.memory_manager, debug=debug
        )
        self.skill_parser = SkillParser(memory_manager=self.memory_manager)
        self.actor = Actor(
            memory_manager=self.memory_manager,
            skill_parser=self.skill_parser,
            debug=debug,
        )
        # self.revision_agent = RevisionAgent(
        #     memory_manager=self.memory_manager,
        #     env_agent=self.env_agent,
        # )

    def run(self):
        """runs the main user interaction loop"""
        system_cli_message("Welcome to the Cap-Optioner agent!")

        while True:
            system_cli_message("Choose an Interaction!")

            options = ["Learn a new skill", "Attempt a task", "Run past example"]
            choice = choice_from_input_items(
                options, "What would you like to do?", is_vertical=False
            )
            match choice:
                case 1:
                    skill = self.skill_parser.parse_skill()
                    if skill is None:
                        break

                    while True:
                        self.env_agent.task_setup()
                        self.attempt_task(skill)
                        choice = choice_from_input_items(
                            ["yes", "no"],
                            "Do you want to provide another task to learn this skill?",
                            is_vertical=False,
                        )
                        if choice == 2:
                            break
                case 2:
                    self.env_agent.task_setup()
                    self.attempt_task()
                case 3:
                    self.run_past_example()

    def attempt_task(self, skill: Skill = None):
        """
        if skill is given, we are trying to solve the task while also learning a specific skill
        otherwise we are just trying to solve the task
        the skill to be learned can be updated - all other skills can only be used
        """
        system_cli_message("ATTEMPTING TASK" if skill is None else "LEARNING SKILL")

        inital_config = self.env_agent.reset()
        task = self.env_agent.current_task.lang_goal
        trace = InteractionTrace(task=task, initial_config=inital_config)

        def get_initial_code():
            return (
                self.actor.learn_skill(self.env_agent.env, task, skill)
                if skill is not None
                else self.actor.attempt_task(self.env_agent.env, task)
            )

        # first attempt at solving the task prior to allowing user corrections
        code = get_initial_code()

        while True:
            # --------------------------------------------------------------------------------
            # use this when display set to false... supposed to be faster, but I'm not sure...
            # img = self.env_agent.env.render()
            # import matplotlib.pyplot as plt

            # plt.imshow(img)
            # plt.show()
            # --------------------------------------------------------------------------------
            options = [
                "Success",
                "Give up",
                "Re-run (last code)",
                "Try again (with new code)",
                "Apply hint",
                "Feedback & iterate",
            ]
            choice = choice_from_input_items(
                options, "How did the agent do? How would you like to proceed?"
            )
            chosen_option = options[choice - 1]

            match chosen_option:
                case "Success":
                    example_code, skill_code = extract_task_and_skill_code(code)

                    final_config = self.env_agent.get_current_config()

                    task_example = TaskExample(
                        task=task,
                        code=example_code,
                        initial_config=inital_config,
                        final_config=final_config,
                        skill_code=skill_code,
                    )

                    self.memory_manager.example_manager.add_example_to_library(
                        task_example
                    )

                    trace.success(task_example)
                    self.memory_manager.add_trace(trace)

                    if skill is not None:
                        # skip skill testing for now...
                        # TODO: this works – you can see whether or not the updated skill still solves prior tasks it was learned on
                        # but there's no way of handling it well right now... so it's a bit pointless
                        # failed_task = self.revision_agent.test_modified_skill_on_past_task_examples(
                        #     skill, skill_code
                        # )

                        # # only update the skill if the new skill is successful on all previous tasks
                        # if failed_task:
                        #     # TODO: handle this somehow...
                        #     print(
                        #         "failed to solve prior tasks - aborting commit! continue iterating!"
                        #     )
                        #     continue

                        skill.code = skill_code
                        skill.add_task_example(task_example)
                        self.memory_manager.skill_manager.add_skill_to_library(skill)

                    self.actor.reset()

                    return
                case "Give up":
                    self.actor.reset()
                    self.memory_manager.add_trace(trace)
                    return
                case "Re-run":
                    self.env_agent.reset()
                    self.actor.run_last_code_str()
                case "Try again":
                    self.env_agent.reset()
                    code = get_initial_code()
                case "Apply hint":
                    hint = simple_user_prompt("What hint would you like to apply?")
                    trace.add_feedback_round(hint)
                    self.env_agent.reset()
                    self.actor.revise_code_with_hint(hint)
                case "Feedback & iterate":
                    feedback = simple_user_prompt(
                        "What constructive feedback can you give the agent?"
                    )
                    trace.add_feedback_round(feedback)
                    self.env_agent.reset()
                    code = self.actor.revise_code_with_feedback(feedback)

    def run_past_example(self, gui_mode=False):
        """retrieves past solved tasks from the agents memory similar to the requested task string,
        and then rolls them out in the environment"""

        system_cli_message("RUNNING PAST EXAMPLE")
        example_string = input("give a task:")
        example = self.memory_manager.example_manager.retrieve_similar_examples(
            example_string, num_results=10
        )
        example_tasks = [example.task for example in example]
        example_index = choice_from_input_items(
            example_tasks, "which task would you like to run?"
        )
        example = example[example_index - 1]
        self.env_agent.set_to_task_and_config(example.task, example.initial_config)
        if self.debug:
            debug_message(example.code, "Running past example code")
        self.actor.run_code_str(self.env_agent.env, example.code)

    def chat_about_capabilities(self):
        """TODO: allows the user to chat with the agent about its capabilities, by interacting with its memory"""
        pass

    def list_all_example_tasks(self):
        """lists all tasks for which the agent has positive successful examples in the agents memory"""
        examples = self.memory_manager.example_manager.all_examples
        tasks = [example.task for example in examples]
        print_list(tasks, "Learned tasks:")

    def list_all_learned_skills(self):
        """lists all learned skills in the agents memory"""
        skills = self.memory_manager.skill_manager.all_skills
        if len(skills) == 0:
            print("No learned skills found.")
            return

        skills = [skill.name for skill in skills if not skill.is_core_primitive]
        print_list(skills, "Learned skills:")





if __name__ == "__main__":
    agent = LYRA(memory_dir="baseline")
    agent.run()
    # agent.run_past_example()
