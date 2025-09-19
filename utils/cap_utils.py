import ast
import re

import traceback

from PIL import Image
import io
import base64
import os

from utils import core_primitives, core_types
import numpy as np
import itertools

from prompts.actor import bug_fix_prompt
from utils.llm_utils import query_llm, parse_code_response, query_llm_structured

from pydantic import BaseModel

from agents.model import Skill


def get_global_vars(env):
    # need to set the current environment as global variable for core primitives
    core_primitives.env = env

    vars = {name: getattr(core_primitives, name) for name in core_primitives.__all__}
    vars.update({name: getattr(core_types, name) for name in core_types.__all__})
    vars.update({"np": np, "itertools": itertools})
    return vars


def cap_code_exec(code_str, env, dependencies=[], lvars={}, max_num_attempts=1):
    # execute code in a simulated environment
    # handles setting up the code environment (i.e. loading all the variables), including all the dependencies
    attempts = 1
    bug_fix_messages = [
        {
            "role": "system",
            "content": "you write python code to control a robotic arm. You receive pieces of code that contain an error, as well as the error traceback, and you are supposed to fix it.",
        }
    ]
    while True:
        try:
            gvars = get_global_vars(env)
            # dependency_resolved_code_str = prepend_code_string_with_dependencies(
            #     code_str, dependencies
            # )
            parse_dependencies(dependencies, gvars)
            exec(code_str, gvars, lvars)
        except:
            traceback.print_exc()
            if attempts < max_num_attempts:
                bug_fix_messages.extend(
                    [
                        {"role": "assistant", "content": code_str},
                        {
                            "role": "user",
                            "content": bug_fix_prompt(code_str, traceback.format_exc()),
                        },
                    ]
                )
                response = query_llm(bug_fix_messages)
                print("attempting to fix bugs")
                code_str = parse_code_response(response)
                attempts += 1
            else:
                return
        else:
            return lvars


def parse_dependencies(dependencies, gvars):
    for skill in dependencies:
        exec(skill.code, gvars)
    return gvars


def prepend_code_string_with_dependencies(code_str, dependencies):
    new_code_str = code_str
    for skill in dependencies:
        new_code_str = skill.code + "\n\n" + new_code_str

    return new_code_str


# def get_calls(code_str, uniquing):
#     fs, f_assigns = {}, {}
#     f_parser = FunctionParser(fs, f_assigns)
#     f_parser.visit(ast.parse(code_str))
#     for f_name, f_assign in f_assigns.items():
#         if f_name in fs:
#             fs[f_name] = f_assign

#     return fs


def get_defs(code_str, full_function_codes=False):
    tree = ast.parse(code_str)
    if full_function_codes:
        return [
            ast.get_source_segment(code_str, node)
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]
    else:
        return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def get_calls(code_str, unique=True):
    tree = ast.parse(code_str)
    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    calls = list(set(visitor.calls)) if unique else visitor.calls
    return calls


def get_non_function_code(code):
    # Parse the code into an AST
    tree = ast.parse(code)
    # Extract non-function top-level code
    non_function_code_nodes = [
        node
        for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    # Convert AST nodes back to source code
    non_function_code = "\n".join(ast.unparse(node) for node in non_function_code_nodes)

    return non_function_code


class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        # Extract function name if it's a direct function call (not a method or attribute)
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        # elif isinstance(
        #     node.func, ast.Attribute
        # ):  # Handles method calls like obj.method()
        #     self.calls.append(node.func.attr)
        self.generic_visit(node)  # Continue visiting child nodes


def extract_task_and_skill_code(code) -> tuple[str, str]:
    """given a code string with a function and some flat code, separate the two, and return both"""
    task_code = get_non_function_code(code)
    defs = get_defs(code, full_function_codes=True)
    if len(defs) != 1:
        print(defs)
        return task_code, None
    skill_code = defs[0]

    return task_code, skill_code


code = """
def build_cube(a):
    x = 5

def sample_func(a, b, c):
    build_cube(a)
    move_end_effector_to(a, b)
    get_bbox(a)

"""

other_code = """
def place_blue_blocks_around_red_block(gap: float = 0.0):
    \"""
    Place one blue block on each side of the red block, aligning their edges perfectly.
    :param gap: The gap to leave between the blocks. Default is 0 for perfect alignment.
    \"""
    # Retrieve all objects in the environment
    objects = get_objects()
    # Get the red block
    red_block = get_block_by_color("red", objects)
    # Get all blue blocks
    blue_blocks = [obj for obj in objects if obj.color == "blue" and obj.objectType == "block"]
    # Ensure there are at least four blue blocks
    if len(blue_blocks) < 4:
        raise ValueError("Not enough blue blocks in the environment to perform the task.")
    # Get the pose of the red block
    red_block_pose = get_object_pose(red_block)
    # Calculate the positions for the blue blocks on each side of the red block
    blue_block_size = blue_blocks[0].size  # Assuming all blue blocks are the same size
    red_block_size = red_block.size
    # Calculate positions for each side
    positions = calculate_positions_around_block(red_block_pose.position, red_block_size, blue_block_size, gap)
    # Place each blue block at the calculated positions with the same rotation as the red block
    for i, position in enumerate(positions):
        place_block_with_rotation(blue_blocks[i], position, red_block_pose.rotation)
        say(f"Placed blue block {blue_blocks[i].description} at position {position} with aligned edges.")
def calculate_positions_around_block(center_position: Point3D, base_block_size: tuple[float, float, float], adjacent_block_size: tuple[float, float, float], gap: float) -> list[Point3D]:
    \"""
    Calculate the positions for blocks to be placed around a central block, aligning their edges.
    :param center_position: The center position of the base block.
    :param base_block_size: The size of the base block.
    :param adjacent_block_size: The size of the adjacent blocks.
    :param gap: The gap to leave between the blocks.
    :return: A list of target positions for the adjacent blocks.
    \"""
    positions = []
    # Calculate offsets for each side
    offsets = [
        (base_block_size[0] / 2 + gap + adjacent_block_size[0] / 2, 0, 0),  # Right
        (-(base_block_size[0] / 2 + gap + adjacent_block_size[0] / 2), 0, 0),  # Left
        (0, base_block_size[1] / 2 + gap + adjacent_block_size[1] / 2, 0),  # Front
        (0, -(base_block_size[1] / 2 + gap + adjacent_block_size[1] / 2), 0)  # Back
    ]
    for offset in offsets:
        new_position = Point3D(
            center_position.x + offset[0],
            center_position.y + offset[1],
            center_position.z + offset[2]
        )
        positions.append(new_position)
    return positions
# Execute the plan
place_blue_blocks_around_red_block()

"""

if __name__ == "__main__":
    # deps = resolve_dependencies(code)
    # print([dep.name for dep in deps])
    # print(prepend_code_string_with_dependencies(code))
    print(resolve_dependencies(other_code))
