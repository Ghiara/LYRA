def build_letter_M(blocks: list[TaskObject], starting_pose: Pose):
    """Constructs the letter 'M' in the workspace using a list of block TaskObjects starting from a given pose.
    Args:
    blocks (list[TaskObject]): A list of blocks to use for forming the letter 'M'. Each block in the list should have consistent properties like size and color.
    starting_pose (Pose): The initial position and orientation in the workspace from where to start constructing the letter 'M'.
    Note:
    The function assumes that there are enough blocks in the list to complete the letter 'M'.
    The design will follow a common block arrangement pattern for an 'M'.
    """
    # Place the first block at the starting position (base of M)
    first_block = blocks[0]
    put_first_on_second(get_object_pose(first_block), starting_pose)
    current_block = first_block
    # Place 4 blocks next to it towards the back (y axis)
    for i in range(1, 4):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="y", gap=0.005)
        current_block = next_block
    # Place three blocks below the second block
    current_block = blocks[1]
    for i in range(4, 7):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="x", gap=0.005)
        current_block = next_block
    # Place three blocks below the fourth block
    current_block = blocks[3]
    for i in range(7, 10):
        next_block = blocks[i]
        move_block_next_to_reference(next_block, current_block, axis="x", gap=0.005)
        current_block = next_block
