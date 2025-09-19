from utils.cap_utils import cap_code_exec
from utils.task_and_store import Task
from agents.model import EnvironmentConfiguration
from environments.environment import Environment


def test_revision(initial_config, final_config, code):
    env = Environment(
        "environments/assets",
        disp=False,
        shared_memory=False,
        hz=480,
        record_cfg={
            "save_video": False,
            "save_video_path": "${data_dir}/${task}-cap/videos/",
            "add_text": True,
            "add_task_text": True,
            "fps": 20,
            "video_height": 640,
            "video_width": 720,
        },
    )
    task = Task()
    task.config = initial_config
    env.set_task(task)
    env.reset()

    cap_code_exec(code, env)

    attempt_final_config = task.get_current_configuration(env)
    return attempt_final_config == final_config


def generate_sample_configs():
    env = Environment(
        "environments/assets",
        disp=True,
        shared_memory=False,
        hz=480,
        record_cfg={
            "save_video": False,
            "save_video_path": "${data_dir}/${task}-cap/videos/",
            "add_text": True,
            "add_task_text": True,
            "fps": 20,
            "video_height": 640,
            "video_width": 720,
        },
    )

    from utils.sample_tasks import Place2Blocks
    from utils import core_primitives as cp

    cp.env = env

    task = Place2Blocks()
    env.set_task(task)
    env.reset()
    initial_config = task.get_current_configuration(env)
    initial_config.dump("initial.pkl")

    blocks = cp.get_objects()
    placePose = cp.get_object_pose(blocks[0])
    pickPose = cp.get_object_pose(blocks[1])
    cp.put_first_on_second(pickPose, placePose)

    final_config = task.get_current_configuration(env)
    final_config.dump("final.pkl")


code = """
blocks = get_objects()
placePose = get_object_pose(blocks[0])
pickPose = get_object_pose(blocks[0])
put_first_on_second(pickPose, placePose)
"""

if __name__ == "__main__":
    generate_sample_configs()
    initial_config = EnvironmentConfiguration.from_path("initial.pkl")
    final_config = EnvironmentConfiguration.from_path("final.pkl")

    print(test_revision(initial_config, final_config, code))
