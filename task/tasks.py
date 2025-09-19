from task.task_and_store import Task
from utils.core_types import Workspace, Pose, Point3D, Rotation


class PlaceGreenNextToYellow(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "place the green block next to the yellow block"

    def reset(self, env):
        super().reset(env)
        self.add_block(env, "green")
        self.add_block(env, "yellow")


class PlaceBlocksDiagonally(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = (
            "place the red block diagonally to the front-right of the blue block"
        )

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 20, "red", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 20, "blue", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 20, "green", size=(0.04, 0.04, 0.04))


class PlaceBlueBlocksAroundRedBlock(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = (
            "put the blue blocks around the red block, aligning their edges perfectly"
        )

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, "red", size=(0.08, 0.08, 0.08))
        self.add_blocks(env, "blue", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, "blue", size=(0.03, 0.02, 0.01))
        self.add_blocks(env, "blue", size=(0.06, 0.04, 0.04))
        self.add_blocks(env, "blue", size=(0.02, 0.02, 0.04))


class StackBlocks(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "stack the blocks on top of each other"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 1, "red", size=(0.08, 0.08, 0.08))
        self.add_blocks(env, 1, "green", size=(0.08, 0.08, 0.08))
        self.add_blocks(env, 1, "blue", size=(0.08, 0.08, 0.08))
        self.add_blocks(env, 1, "yellow", size=(0.08, 0.08, 0.08))


class StackBlocksBigToSmall(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "stack the blocks from biggest to smallest"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 20, "red", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 20, "blue", size=(0.06, 0.06, 0.06))
        self.add_blocks(env, 20, "green", size=(0.08, 0.08, 0.08))


class StackBlocksInduceFailure(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = (
            f"stack the blocks in the middle of the workspace (i.e. {Workspace.middle})"
        )

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 3, "blue", size=(0.04, 0.04, 0.04))
        self.add_block(
            env,
            "red",
            size=(0.04, 0.04, 0.04),
            pose=Pose(
                position=Point3D.from_xyz(
                    (Workspace.middle.x, Workspace.middle.y - 0.03, 0.04)
                ),
                rotation=Rotation.identity(),
            ),
        )


class BuildHouse(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a house from the blocks"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 14, "yellow", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.14, 0.01))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.025, 0.025))
        self.add_blocks(env, 6, "red", size=(0.07, 0.06, 0.01))


class BuildJengaLayer(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a single layer of a Jenga tower from the blocks"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 3, size=(0.15, 0.05, 0.03))


class BuildJengaTower(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a jenga tower"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 24, size=(0.09, 0.03, 0.02))


class BuildJengaTowerLongDescription(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a jenga tower. Do this by placing the three blocks next to each other, so that they form a square (each block has one dimension that is 3 times larger than another). Then do the same thing, placing three blocks on top of these, again forming a square, but rotated by 90 degrees. Continue this way until you've used all the blocks."

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 24, size=(0.09, 0.03, 0.02))


class ConstructSmileyFace(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "construct a smiley face from the blocks."

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 10, "yellow", size=(0.02, 0.02, 0.02))
        self.add_cylinder(env, "blue")  # eyes
        self.add_cylinder(env, "blue")  # eyes
        self.add_blocks(env, 1, "red", size=(0.08, 0.02, 0.01))  # mouth


class ConstructSmileyFaceLongDescription(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "construct a smiley face from the blocks. Use the yellow blocks to form a circle, the blue blocks to form the eyes, and the red block for the mouth."

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 10, "yellow", size=(0.02, 0.02, 0.02))
        self.add_blocks(env, 2, "blue", size=(0.04, 0.04, 0.04))  # eyes
        self.add_block(env, 1, "red", size=(0.08, 0.02, 0.01))  # mouth


class BuildBlockPyramid(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a pyramid with a 3*3 base from the blocks"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 14, "yellow", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.14, 0.01))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.04, 0.04))
        self.add_blocks(env, 6, "red", size=(0.07, 0.06, 0.01))


class BuildCube(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a 2*2*2 cube from the blocks"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 8, size=(0.04, 0.04, 0.04))


class BuildZigZagTower(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a zig-zag tower from the blocks"

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 6, "red", size=(0.04, 0.04, 0.04))


class BuildZigZagTowerLongDescription(Task):
    def __init__(self):
        super().__init__()
        self.lang_goal = "build a zig-zag tower from the blocks. you do this by stacking blocks with small y offsets, so that the blocks are not directly on top of each other. Put two blocks towards the left, and two blocks towards the right, etc..."

    def reset(self, env):
        super().reset(env)
        self.add_blocks(env, 14, "yellow", size=(0.04, 0.04, 0.04))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.14, 0.01))
        self.add_blocks(env, 1, "brown", size=(0.18, 0.04, 0.04))
        self.add_blocks(env, 6, "red", size=(0.07, 0.06, 0.01))
