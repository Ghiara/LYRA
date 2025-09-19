from utils.core_types import TaskObject, Pose
from utils.core_primitives import (
    get_object_pose,
    get_object_size,
    put_first_on_second,
    get_point_at_distance_and_rotation_from_point,
)


def make_line_with_blocks(
    blocks: list[TaskObject], start_pose: Pose, gap: float = 0.005
):
    """Arranges the given blocks in a straight line starting from the specified start pose.
    Args:
        blocks (list[TaskObject]): A list of block objects to be arranged in a line.
        start_pose (Pose): The pose in the workspace where the line of blocks should start.
                           The position will be used as the starting point, and the rotation
                           will be used as the direction vector.
        gap (float): The gap between consecutive blocks.
    Note:
        The function places the blocks in the order in which they are passed.
    """
    current_block = blocks[0]
    put_first_on_second(get_object_pose(current_block), start_pose)
    for block in blocks[1:]:
        # Get the current pose of the block
        move_block_next_to_reference(block, current_block, axis="x", gap=gap)
        current_block = block
