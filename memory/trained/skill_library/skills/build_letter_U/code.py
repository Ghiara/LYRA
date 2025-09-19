def build_letter_U(blocks: list[TaskObject], starting_pose: Pose):
    """Constructs the letter 'U' in the workspace using a list of block TaskObjects starting from a specified pose.
    Args:
    blocks (list[TaskObject]): A list of blocks to use in forming the letter 'U'. Each block should have uniform attributes such as size and color.
    starting_pose (Pose): The starting position and orientation in the workspace from which to begin constructing the letter 'U'.
    Note:
    The function assumes that there are sufficient blocks in the list to complete the letter 'U'.
    Blocks will be arranged to follow a typical layout design for a 'U'.
    """
    gap = 0.005  # Small gap between blocks

    # Start from the top-right corner of the 'U'
    current_block = blocks[0]
    put_first_on_second(get_object_pose(current_block), starting_pose)

    # Place 3 blocks towards the front (x-axis) from the first block
    for i in range(1, 4):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="x", gap=gap)
        current_block = next_block

    # Place 2 blocks towards the right (y-axis) starting from the first block
    for i in range(4, 6):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="y", gap=gap)
        current_block = next_block

    for i in range(6, 10):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="-x", gap=gap)
        current_block = next_block
