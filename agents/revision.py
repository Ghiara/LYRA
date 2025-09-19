from utils.cap_utils import cap_code_exec
from task.task_and_store import Task
from agents.model import EnvironmentConfiguration, Skill, TaskExample
from agents.memory import MemoryManager
from agents.environment import EnvironmentAgent
from environments.environment import Environment


class RevisionAgent:
    """checks whether a task is still solved successfully when skill code changes,
    but checking based on EnvironmentConfiguration equality is too strict for most cases (i.e. we may get false negatives)
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
        env_agent: EnvironmentAgent,
    ):
        self.memory_manager = memory_manager
        self.env_agent = env_agent

    def test_modified_skill_on_past_task_examples(
        self, skill: Skill, modified_skill_code
    ) -> TaskExample | None:
        """code change has been proposed - tests whether prior task sequences are still solved by the updated code
        assumes this function is run before actually committing skill and task example
        """
        task_examples = self.memory_manager.skill_task_examples(skill)

        current_task = self.env_agent.current_task
        current_config = self.env_agent.get_current_config()

        is_failure = False

        for task_example in task_examples:
            print(f"testing task example {task_example.task}")
            code = modified_skill_code + "\n\n" + task_example.code
            did_solve_task = self.test_revision(
                code,
                task_example.initial_config,
                task_example.final_config,
                self.env_agent.env,
            )
            print(did_solve_task)

            if not did_solve_task:
                how_to_handle = input("how to handle this? (skip, discard, accept)")
                match how_to_handle:
                    case "skip":
                        continue
                    case "discard":
                        self.memory_manager.example_manager.delete_example(task_example)
                        skill.remove_task_example(task_example)
                        skill.dump()
                        continue
                    case "accept":
                        is_failure = True
                        break

        self.env_agent.set_to_task_and_config(current_task.lang_goal, current_config)

        return is_failure

    def test_revision(
        self,
        code,
        initial_config: EnvironmentConfiguration,
        final_config: EnvironmentConfiguration,
        env: Environment,
    ) -> bool:
        """should add code here to somehow handle when configurations are not equal
        should review - if they're equal we don't need to look, but if they aren't then we should check if it isn't possibly still good enough
        """
        # print(initial_config)
        # print(final_config)
        attempt_final_config = self.run_and_get_final_config(code, initial_config, env)
        return attempt_final_config == final_config

    def run_and_get_final_config(
        self, code, initial_config: EnvironmentConfiguration, env: Environment
    ) -> EnvironmentConfiguration:

        task = Task()
        task.config = initial_config
        env.set_task(task)
        env.reset()

        cap_code_exec(
            code, env, self.memory_manager.skill_manager.resolve_dependencies(code)
        )

        attempt_final_config = task.get_current_configuration(env)

        return attempt_final_config


if __name__ == "__main__":
    pass
    # skill = Skill.retrieve_skill_with_name("make_line_with_blocks")
    # modified_skill_code = skill.code

    # env = Environment(
    #     "environments/assets",
    #     disp=True,
    #     shared_memory=False,
    #     hz=480,
    #     record_cfg={
    #         "save_video": False,
    #         "save_video_path": "${data_dir}/${task}-cap/videos/",
    #         "add_text": True,
    #         "add_task_text": True,
    #         "fps": 20,
    #         "video_height": 640,
    #         "video_width": 720,
    #     },
    # )

    # test_modified_skill_on_past_task_examples(skill, modified_skill_code, env)
