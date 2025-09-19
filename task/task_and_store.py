from environments.task import Task
from utils.core_types import (
    TaskObject,
    Pose,
    Point3D,
    Rotation,
    Workspace,
    _from_pybullet_pose,
    _to_pybullet_pose,
)
from environments.environment import Environment
from agents.model.environment_configuration import EnvironmentConfiguration
import pybullet as p

import time
import random

import utils.general_utils as utils

import numpy as np


class Task(Task):
    """
    Provides a simple API to enable setting up the environment in a chat-based manner
    For example, adding different objects in different places
    This is more for myself... I could write each environment setup myself, but I think this would lead to more variety
    each environment setup is given as a function which returns a Task

    Another reason for this was to enable storing the environment setup, so we can restore it later
    1. This allows storing of configs, so we can use the robot itself to set up a task (allowing task setup to benefit from a smarter robot)
    2. To allow us to run prior task examples (by setting up exact environment state, when having previously generated the environment setup)
        -- this is necessary when skill code is overwritten, to see if the overwritten code still solves prior tasks
    """

    def __init__(self, config=None, lang_goal=None):
        super().__init__()
        self.taskObjects: list[TaskObject] = []
        self.lang_goal = lang_goal
        self.config = config

    def reset(self, env):
        super().reset(env)

        if self.config is not None:
            self.restore_from_config(env, self.config)
            # wait for blocks to settle...
            for _ in range(500):
                p.stepSimulation()
                time.sleep(1 / 400)
        else:
            self.taskObjects = []

    def set_lang_goal(self, lang_goal):
        self.lang_goal = lang_goal

    def add_blocks(
        self,
        env: Environment,
        num_blocks: int = 20,
        color=None,
        size: tuple[float, float, float] = (0.04, 0.04, 0.04),
        collision_free: bool = True,
    ):
        for _ in range(num_blocks):
            self.add_block(
                env,
                color=color or random.choice(list(utils.COLORS.keys())),
                size=size,
                collision_free=collision_free,
            )

        # might cause some issues with blocks flying everywhere...
        if not collision_free:
            self.wait_for_objects_to_settle()

    def add_block(
        self,
        env: Environment,
        color: str = "red",
        size: tuple[float, float, float] = (0.04, 0.04, 0.04),
        pose: Pose = None,
        collision_free: bool = True,
    ):
        block_urdf = "box/box-template.urdf"

        if collision_free:
            block_pose = (
                self.get_random_pose(env, size)
                if pose is None
                else _to_pybullet_pose(pose)
            )
        else:
            block_pose = _to_pybullet_pose(self.get_random_pose_not_collision_free())

        sized_block_urdf = self.fill_template(block_urdf, {"DIM": size})
        block_id = env.add_object(
            sized_block_urdf,
            block_pose,
            color=color or random.choice(list(utils.COLORS.keys())),
        )
        # p.changeVisualShape(block_id, -1, rgbaColor=utils.COLORS[color] + [1])

        task_obj = TaskObject(
            objectType="block", color=color, id=block_id, category="rigid", size=size
        )

        self.taskObjects.append(task_obj)

    def add_cylinder(self, env: Environment, color: str = "red", scale=0.5):
        cylinder_size = (0.04, 0.04, 0.01)
        cylinder_pose = self.get_random_pose(env, cylinder_size)
        cylinder_urdf = "cylinder/cylinder-template.urdf"
        cylinder_id = env.add_object(
            cylinder_urdf, cylinder_pose, color=color, scale=0.5
        )
        task_obj = TaskObject(
            objectType="cylinder",
            color=color,
            id=cylinder_id,
            category="rigid",
            size=(
                cylinder_size[0] * scale,
                cylinder_size[1] * scale,
                cylinder_size[2] * scale,
            ),
        )
        self.taskObjects.append(task_obj)

    def wait_for_objects_to_settle(self):
        for _ in range(500):
            p.stepSimulation()
            time.sleep(1 / 400)

    def add_zone(
        self,
        env: Environment,
        color: str,
        scale: float = 1,
        pose: Pose = None,
    ):
        _SIZE = (0.1, 0.1, 0.01)
        SIZE = _SIZE * scale
        zone_pose = (
            self.get_random_pose(env, SIZE) if pose is None else _to_pybullet_pose(pose)
        )

        zone_id = env.add_object(
            "zone/zone.urdf", zone_pose, "fixed", scale=scale, color=color
        )

        task_obj = TaskObject(
            objectType="zone",
            color=color,
            id=zone_id,
            category="fixed",
            size=SIZE,
        )
        self.taskObjects.append(task_obj)

    def add_pallet(self, env: Environment, pose=None):
        pallet_size = (0.2, 0.2, 0.02)
        pallet_pose = self.get_random_pose(env, pallet_size)
        pallet_urdf = "pallet/pallet.urdf"
        pallet_id = env.add_object(pallet_urdf, pallet_pose, category="fixed")

        task_obj = TaskObject(
            objectType="pallet",
            color="brown",
            id=pallet_id,
            category="fixed",
            size=pallet_size,
        )
        self.taskObjects.append(task_obj)

    def get_random_pose_not_collision_free(self) -> Pose:
        def random_in_range(low, high):
            return np.random.uniform(low, high)

        pos = [
            random_in_range(Workspace.bounds[0][0], Workspace.bounds[0][1]),
            random_in_range(Workspace.bounds[1][0], Workspace.bounds[1][1]),
            random_in_range(Workspace.bounds[2][0], Workspace.bounds[2][1]),
        ]
        theta = np.random.rand() * 2 * np.pi
        rot = utils.eulerXYZ_to_quatXYZW((0, 0, theta))

        return Pose(Point3D.from_xyz(pos), Rotation.from_quat(rot))

    def get_current_configuration(self, env: Environment) -> EnvironmentConfiguration:
        """gets all the objects and their properties, so we can reinitialise the scene..."""
        config = []
        for obj in self.taskObjects:
            pose = _from_pybullet_pose(env.get_object_pose(obj.id))
            config.append((obj, pose))

        img = env.render()

        storable = EnvironmentConfiguration(config, img)
        return storable

    def restore_from_config(self, env: Environment, config: EnvironmentConfiguration):
        self.taskObjects = []
        for obj, pose in config.objects_with_poses:
            if obj.objectType == "block":
                self.add_block(env, obj.color, obj.size, pose)
            if obj.objectType == "zone":
                scale = obj.size[0] / 0.1
                self.add_zone(env, obj.color, scale, pose)


class GeneratedTask(Task):
    def __init__(self, task_setup_code, task_description=None):
        super().__init__()
        self.task_setup_code = task_setup_code
        self.lang_goal = task_description

    def reset(self, env):
        super().reset(env)

        exec(self.task_setup_code)
