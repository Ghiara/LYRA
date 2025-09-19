from utils.core_primitives import *
from utils.core_types import *
from agents.model import TaskExample
import inspect
import textwrap


def example1():
    #put one block on top of another block
    objects = get_objects()
    blocks = [block for block in objects if block.objectType == "block"]
    pose0 = get_object_pose(blocks[0])
    pose1 = get_object_pose(blocks[1])
    put_first_on_second(pose0, pose1)

def example2():
    #put the red block in the middle of the workspace
    objects = get_objects()
    red_block = next(block for block in objects if block.objectType == "block" and block.color == "red")
    middle_pose = Pose(position=Workspace.middle, rotation=Rotation.identity())
    put_first_on_second(red_block, middle_pose)

def example3():
    #rotate the blue block by 45 degrees
    objects = get_objects()
    red_block = next(block for block in objects if block.objectType == "block" and block.color == "blue")
    red_block_pose = get_object_pose(red_block)
    rotated_pose = Pose(red_block_pose.position, red_block_pose.rotation * Rotation.from_euler('z', 90, degrees=True))
    put_first_on_second(red_block_pose, rotated_pose)

def example4():
    #move the smallest block 10cm to the left
    objects = get_objects()
    smallest_block = min(objects, key=lambda x: x.size[0])
    smallest_block_pose = get_object_pose(smallest_block)
    translated_pose = Pose(smallest_block_pose.position.translate(Point3D(0, -0.1, 0)), smallest_block_pose.rotation)
    put_first_on_second(smallest_block_pose, translated_pose)

def example5():
    #move the end effector to the middle of the workspace
    move_end_effector_to(Pose(Workspace.middle))


def base_task_examples() -> list[TaskExample]:
    examples = [example1, example2, example3, example4, example5]
    task_examples = []
    for example in examples:
        lines = inspect.getsourcelines(example)[0]
        task_descr = textwrap.dedent(lines[1])[1:]
        code = textwrap.dedent(''.join(lines[2:]))
        task_example = TaskExample(task= task_descr, code=code)
        task_examples.append(task_example)

    return task_examples


if __name__ == "__main__":
    base_task_examples()