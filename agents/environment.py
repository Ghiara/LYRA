from agents.model import EnvironmentConfiguration
from environments.environment import Environment
from agents.memory import MemoryManager, ConfigManager
from prompts.task_gen_prompt import task_setup_system_prompt
from utils.llm_utils import query_llm, parse_code_response
from task.task_and_store import Task, GeneratedTask
from task import all_tasks

from utils.cli_utils import *

import streamlit as st


class EnvironmentAgent:
    """
    responsible for aiding in environment setup
    like the actor, should get better and better at setting the environment to a specific configuration
    for now just a two-pass attempt
    first: retrieve previous configs
    if none chosen, generate new from string
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
        config_manager: ConfigManager = None,
        debug=False,
    ):
        self.debug = debug
        self.is_recording = False

        self.current_task = Task()
        self.setup_environment()
        self.reset()
        self.memory_manager = memory_manager
        self.config_manager = config_manager

    def parse_task_description(self):
        task_str = simple_user_prompt("What task do you want the agent to solve?")
        return task_str

    def task_setup(self, gui_mode=False):
        """there is 3 basic ways to set up the task:
        (1) generate a new one
        (2) use an existing config
        (3) use a predefined task (in task/tasks.py)
        options 1 and 2 require you to specify the task description, while dynamically forming the initial environment state
        option 3 presumes both initial state and task description are given

        this function ensures the task is set up correctly
        """
        if gui_mode:
            st.subheader("Task Setup", divider=True)
            st.write(
                "**This is the task setup interface. You can set up a task in three ways:**"
            )
            st.write(
                """
                - 1. Generate a new task based on a description you provide.
                - 2. Use an existing stored environment state.
                - 3. Use a predefined task from the available tasks.
                """
            )
            selection = st.radio(
                "How would you like to set up the task?",
                options=[
                    "Generate new task",
                    "Use stored environment state",
                    "Use predefined task",
                ],
                index=None,
            )
            if selection == "Generate new task":
                self.task_with_generated_setup_code(gui_mode=True)
            elif selection == "Use stored environment state":
                self.task_with_stored_config()
            elif selection == "Use predefined task":
                # identifier = st.text_input(
                #     "Select the predefined task you want to use:"
                # )
                identifier = st.selectbox(
                    "Select the predefined task you want to use:",
                    options=list(all_tasks.keys()),
                    index=None,
                )
                st.write(f"Selected task identifier: **{identifier}**")
                if identifier:
                    self.initialise_predefined_task(identifier)
        else:
            system_cli_message("TASK SETUP")

            choice = choice_from_input_items(
                [
                    "Generate new task",
                    "Use stored environment state",
                    "Use predefined task",
                ],
                "How would you like to set up the task?",
            )
            match choice:
                case 1:
                    self.task_with_generated_setup_code()
                case 2:
                    self.task_with_stored_config()
                case 3:
                    self.initialise_predefined_task()

    def task_with_generated_setup_code(self, gui_mode=False):
        if gui_mode:
            env_setup_prompt = st.text_input("How should the environment be set up?")
        else:
            env_setup_prompt = simple_user_prompt("How should the environment be set up?")
        setup_code = self.generate_task_setup_code(env_setup_prompt)
        self.current_task = GeneratedTask(setup_code)
        self.reset()
        self.current_task.lang_goal = self.parse_task_description()

    def task_with_stored_config(self, gui_mode=False):
        """checks for existing configs for initial environment state"""
        if gui_mode:
            config_description = st.text_input(
                "Give a description of the stored environment state you're looking for",
                )
        else:
            config_description = simple_user_prompt(
                "Give a description of the stored environment state you're looking for"
            )

        existing_configs = self.config_manager.retrieve_configs(
            config_description, num_results=10
        )
        descriptions = [config.description for config in existing_configs]
        choice = choice_from_input_items(
            descriptions,
            "Which of the following configurations would you like to use?",
        )

        if choice is None:
            return self.task_setup()

        config = existing_configs[choice - 1]
        self.current_task = Task(config=config)
        self.reset()
        task_str = self.parse_task_description()
        self.current_task.lang_goal = task_str

    def initialise_predefined_task(self, identifier:str=None):
        """initialises the task from a provided python file"""
        if identifier is None:
            identifier = simple_user_prompt("Give the descriptor of the task")

        if identifier in all_tasks:
            task = all_tasks[identifier]
            self.current_task = task()
            return
        else:
            print("A task with that identifier does not exist.")
            return self.task_setup()

    def setup_environment(self):
        from pathlib import Path
        from datetime import datetime

        video_save_dir = Path(__file__).parent.parent / "data"
        env = Environment(
            "environments/assets",
            ##############################################################
            disp=True, # TODO: rendering in streamlit is not supported yet
            ##############################################################
            shared_memory=False,
            hz=480,
            record_cfg={
                "save_video": self.is_recording,
                "save_video_path": video_save_dir,
                "add_text": False,
                "add_task_text": False,
                "fps": 20,
                "video_height": 640,
                "video_width": 720,
            },
        )

        self.env = env

    def reset(self):
        self.env.set_task(self.current_task)
        self.env.reset()
        config = self.get_current_config()
        self.config_stack = [config]

        if self.is_recording:
            from datetime import datetime

            video_file_name = datetime.now().strftime("%d_%H-%M-%S")
            self.env.start_rec(video_file_name)

        return config

    def reset_in_gui(self):
        self.env.set_task(self.current_task)
        self.env.reset()
        config = self.get_current_config()
        self.config_stack = [config]

        if self.is_recording:
            from datetime import datetime

            video_file_name = datetime.now().strftime("%d_%H-%M-%S")
            self.env.start_rec(video_file_name)
        color_img = self.env.render()
        return config, color_img

    def pop_config(self) -> EnvironmentConfiguration:
        # TODO: this function should enable the user to solve a task in steps,
        # rather than generating the entire solution code in one go
        # while simple in principle, actually generating code in a manner that enables this is not trivial
        # would definitely be a useful function though

        config = self.configs[-1]
        self.set_to_task_and_config(self.current_task.lang_goal, config)

    def get_current_config(self) -> EnvironmentConfiguration:
        return self.env.task.get_current_configuration(self.env)

    def set_to_task_and_config(self, task: str, config: EnvironmentConfiguration):
        reset_task = Task()
        reset_task.config = config
        reset_task.lang_goal = task
        self.current_task = reset_task
        self.reset()

    def set_task(self, task: Task):
        self.current_task = task

    def generate_task_setup_code(self, task_setup_prompt: str):
        messages = [
            {"role": "system", "content": task_setup_system_prompt},
            {"role": "user", "content": task_setup_prompt},
        ]

        response = query_llm(messages)
        code = parse_code_response(response)
        if self.debug:
            debug_message(code, "Generated task setup code")
        return code


if __name__ == "__main__":
    import time

    env_agent = EnvironmentAgent(
        MemoryManager("memory/memory"), config_manager=ConfigManager()
    )

    env_agent.task_setup()
    env_agent.reset()

    time.sleep(10)
