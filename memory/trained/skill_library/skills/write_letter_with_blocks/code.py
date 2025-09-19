from utils.core_types import *


def write_letter_with_blocks(
    letter: str, starting_pose: Pose, blocks: list[TaskObject]
):
    """
    Arranges blocks in the workspace to form the shape of a specified letter.
    Args:
    letter (str): The letter to form using the blocks. Only uppercase and supported letters should be attempted.
    starting_pose (Pose): The starting pose in the workspace from where to begin placing blocks. This includes position and rotation.
    blocks (list[TaskObject]): A list of block objects to be used for forming the letter. Each block includes its properties like size and color.

    Note:
    removes used blocks from the input list, so after finishing they are no longer in the list
    """
    # Get the grid representation of the letter
    letter_pixels = get_letter_pixels(letter)
    # Assume each block occupies one pixel in the grid
    block_size = blocks[0].size[0]  # Assuming all blocks have the same size
    gap = 0.005  # Additional gap between blocks
    for j, row in enumerate(letter_pixels):  # Switch j and i to correct rotation
        for i, pixel in enumerate(row):  # Switch j and i to correct rotation
            if pixel == 1:
                # Calculate target pose for the block based on starting_pose
                position = Point3D(
                    starting_pose.position.x
                    + j * (block_size + gap),  # Add gap to x-axis
                    starting_pose.position.y
                    + i * (block_size + gap),  # Add gap to y-axis
                    starting_pose.position.z,
                )
                pose = Pose(position=position, rotation=starting_pose.rotation)
                # Pick and place a block at the calculated position
                if blocks:
                    block = blocks.pop()
                    put_first_on_second(get_object_pose(block), pose)
