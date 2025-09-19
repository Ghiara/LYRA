import numpy as np
from utils.core_types import *
from utils.core_types import _from_pybullet_pose, _to_pybullet_pose
import utils.general_utils as utils

import pybullet as p

"""
-----------------------------------------------------------------------------
the following functions require an initialised environment - 
the agent doesn't need to know anything about the environment, only what methods are available to it
we are responsible for properly initialising the environment, and ensuring that the agent has access to it
"""

"""
IMPORTANT
- pybullet can only handle one server at a time, if this is not commented out, this is the environment being used
"""

# env = Environment(
#     "/Users/maxfest/vscode/thesis/thesis/environments/assets",
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
# from tasks.tasks.place_blocks import Place5Blocks

# task = Place5Blocks()

# env.set_task(task)
# env.reset()
"""-----------------------------------------------------------------------------"""

__all__ = [
    "get_objects",
    "get_object_size",
    "get_object_pose",
    "get_end_effector_pose",
    "put_first_on_second",
    "move_end_effector_to",
    "get_bbox",
    "get_point_at_distance_and_rotation_from_point",
]


def get_object_pose(obj: TaskObject) -> Pose:
    """returns the pose (Point3d, Rotation) of a given object in the environment."""
    return _from_pybullet_pose(env.get_object_pose(obj.id))


def get_object_size(task_object: TaskObject) -> tuple[float, float, float]:
    """Returns the size of the given TaskObject as a tuple (width, depth, height)."""
    return task_object.size


def get_object_color(task_object: TaskObject) -> str:
    return task_object.color


def get_end_effector_pose() -> Pose:
    """gets the current pose of the end effector"""
    return _from_pybullet_pose(env.get_ee_pose())


def get_bbox(obj: TaskObject) -> AABBBoundingBox:
    """gets the axis-aligned bounding box of an object - this is useful primarily for collision detection"""
    aabb_min, aabb_max = env.get_bounding_box(obj.id)

    return AABBBoundingBox(Point3D.from_xyz(aabb_min), Point3D.from_xyz(aabb_max))


def get_objects() -> list[TaskObject]:
    """gets all objects in the environment"""
    return env.task.taskObjects


def move_end_effector_to(pose: Pose, speed=0.001):
    """moves the end effector from its current Pose to a given new Pose"""
    env.movep(_to_pybullet_pose(pose), speed=speed)


def put_first_on_second(pickPose: Pose, placePose: Pose):
    """
    This is the main pick-and-place primitive.
    It allows you to pick up the TaskObject at 'pickPose', and place it at the Pose specified by 'placePose'.
    If 'placePose' is occupied, it places the object on top of 'placePose.
    """
    return env.step(
        action={
            "pose0": _to_pybullet_pose(pickPose),
            "pose1": _to_pybullet_pose(placePose),
        }
    )


def get_point_at_distance_and_rotation_from_point(
    point: Point3D, rotation: Rotation, distance: float, direction=np.array([1, 0, 0])
) -> Point3D:
    """compute a point that is at a specific 'distance' from 'point', at a specified 'rotation'
    The direction specifies the base direction in which to apply the rotation.
    This is useful for placing objects relative to other objects.
    """

    rotated_direction = rotation.apply(direction)
    new_point = point.np_vec + distance * rotated_direction
    return Point3D.from_xyz(new_point)


def say(msg: str):
    """prints a message for the user to the terminal"""
    msg = f"robot says: {msg}"
    print(msg)
    return msg


def activate_end_effector():
    """activates the gripper - if there is an object in contact with the gripper, it will grasp this object
    if there is no object, it just won't work"""
    env.ee.activate()


def release_end_effector():
    """releases the end effector, and any object that was previously grasped"""
    import time

    env.ee.release()
    for _ in range(500):
        p.stepSimulation()
        time.sleep(1 / 400)


def check_grasp() -> bool:
    """checks whether the gripper is currently holding an object"""
    return env.ee.check_grasp()


def pick(object: TaskObject) -> bool:
    """moves end effector to the pick pose and activates"""
    object_pose = get_object_pose(object)
    size = get_object_size(object)
    pick_pose = Pose(
        object_pose.position.translate(Point3D(0, 0, size[2] / 2)), object_pose.rotation
    )
    pick_pose = _to_pybullet_pose(pick_pose)
    speed = 0.001
    # Execute picking primitive.
    prepick_to_pick = ((0, 0, 0.32), (0, 0, 0, 1))
    prepick_pose = utils.multiply(pick_pose, prepick_to_pick)
    timeout = env.movep(prepick_pose, speed)

    # Move towards pick pose until contact is detected.
    delta = (np.float32([0, 0, -0.001]), utils.eulerXYZ_to_quatXYZW((0, 0, 0)))
    targ_pose = prepick_pose
    while not env.ee.detect_contact():  # and target_pose[2] > 0:
        targ_pose = utils.multiply(targ_pose, delta)
        timeout |= env.movep(targ_pose)
        if timeout:
            return True

    # Activate end effector, move up, and check picking success.
    env.ee.activate()
    pick_success = env.ee.check_grasp()
    return pick_success


if __name__ == "__main__":

    import time

    block = get_objects()[0]
    pose = get_object_pose(block)
    size = get_object_size(block)

    pos = pose.position.translate(Point3D(0, size[1] + 0.02, 0))

    ee_pose = get_end_effector_pose()

    over_prenudge_pos = Point3D(pos.x, pos.y, ee_pose.position.z)
    prenudge_pos = Point3D(pos.x, pos.y, pos.z)
    prenudge_pose = Pose(position=prenudge_pos)

    nudge_pose = Pose(position=pos.translate(Point3D(0, -0.07, 0)))
    move_end_effector_to(Pose(over_prenudge_pos), speed=0.0001)
    move_end_effector_to(prenudge_pose, speed=0.0001)
    move_end_effector_to(nudge_pose, speed=0.0001)

    time.sleep(5)
