from utils.core_types import *


def build_jenga_layer(jenga_blocks: list[TaskObject], base_pose: Pose, spacing: float):
    """Construct a layer of a Jenga tower using a given list of jenga blocks.
    The blocks will be placed in parallel orientation with each other, with spacing between them on a given base pose.
    Args:
    - jenga_blocks: A list of TaskObject each representing a Jenga block.
    - base_pose: Pose representing the starting pose for the first block in the layer.
    - spacing: A float indicating the space that should be maintained between each Jenga block.
    """
    # Assuming the blocks are homogeneous and all have the same dimensions
    if not jenga_blocks or len(jenga_blocks) < 3:
        raise ValueError(
            "At least three jenga blocks are required to form a single layer."
        )
    # Get the size of one block to determine alignment
    block_size = get_object_size(jenga_blocks[0])
    block_length = block_size[1]  # assuming y-axis is the longer side for alignment
    # Calculate the middle block's initial position based on the base_pose
    middle_block_index = len(jenga_blocks) // 2
    middle_block_position = base_pose.position
    middle_block_pose = Pose(middle_block_position, base_pose.rotation)
    # Place the middle block
    put_first_on_second(
        get_object_pose(jenga_blocks[middle_block_index]), middle_block_pose
    )
    # Place one block on each side of the middle block
    left_index = middle_block_index - 1
    right_index = middle_block_index + 1
    if left_index >= 0:
        move_block_next_to_reference(
            jenga_blocks[left_index], jenga_blocks[middle_block_index], "y", spacing
        )
    if right_index < len(jenga_blocks):
        move_block_next_to_reference(
            jenga_blocks[right_index], jenga_blocks[middle_block_index], "-y", spacing
        )
