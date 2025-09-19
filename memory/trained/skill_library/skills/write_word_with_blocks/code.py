from utils.core_types import *

def write_word_with_blocks(word: str, blocks: list[TaskObject], start_position: Point3D):
    """Arranges blocks in the workspace to form the given word starting from the specified position.
    Args:
        word: The word to be written with blocks.
        blocks: A list of TaskObjects representing the blocks to be used.
        start_position: The initial position in the workspace where the writing will start.
    Notes:
        The blocks should be arranged in sequence to spell out the word.
        It's assumed that each character of the word requires a certain number of blocks, and the caller 
        ensures there are enough blocks of suitable size before invoking this function.
    """
    # Assuming each character fits within 11 times the width of a block
    if not blocks:
        raise ValueError("The block list must not be empty.")
    block_size = get_object_size(blocks[0])
    character_spacing = 11 * block_size[0]
    current_position = start_position
    for letter in word:
        if len(blocks) == 0:
            raise ValueError("Not enough blocks to write the entire word.")
        # Calculate Pose for the current letter
        letter_pose = Pose(current_position, Rotation.identity())
        # Use pre-defined function to write the letter with blocks
        write_letter_with_blocks(letter, letter_pose, blocks)
        # Update current position for next letter
        current_position = Point3D(current_position.x, current_position.y + character_spacing, current_position.z)