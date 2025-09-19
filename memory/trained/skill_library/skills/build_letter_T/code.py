def build_letter_T(blocks: list[TaskObject], starting_pose: Pose):
    """
    Constructs the letter 'T' in the workspace using a list of block TaskObjects starting from a specified pose.
    Args:
    blocks (list[TaskObject]): A list of blocks to use in forming the letter 'T'. Each block should have uniform attributes such as size and color.
    starting_pose (Pose): The starting position and orientation in the workspace from which to begin constructing the letter 'T'.
    Note:
    The function assumes that there are sufficient blocks in the list to complete the letter 'T'.
    Blocks will be arranged to follow a typical layout design for a 'T'.
    """
    # Define the workspace center
    workspace_center = Workspace.middle
    # Build the vertical stem of 'T' consisting of 4 blocks
    initial_pose = Pose(workspace_center, starting_pose.rotation)
    for i in range(4):
        if i == 0:
            put_first_on_second(get_object_pose(blocks[i]), initial_pose)
        else:
            move_block_next_to_reference(blocks[i], blocks[i - 1], axis="-x", gap=0.005)
    # Position the horizontal top part of 'T'
    top_most_block = blocks[3]
    move_block_next_to_reference(blocks[4], top_most_block, axis="-y", gap=0.005)
    move_block_next_to_reference(blocks[5], top_most_block, axis="y", gap=0.005)
