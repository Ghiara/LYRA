def make_line_of_blocks_next_to(blocks: list[TaskObject], referenceBlock: TaskObject, direction: str, gap: float = 0.005):
    """
    Arranges the given blocks in a straight line next to a reference block in the specified direction.
    Args:
        blocks (list[TaskObject]): A list of TaskObject instances representing the blocks to be arranged in a line.
        referenceBlock (TaskObject): The TaskObject representing the reference block next to which the line will start.
        direction (str): A string indicating the direction in which to align the line of blocks. 
                         Valid directions are "front", "back", "left", and "right".
        gap (float): The gap between the reference block and the first block in the line, and between consecutive blocks.
    This function will arrange the specified blocks in a single line, starting from the chosen side of the reference block,
    following the given direction along the x or y axis in the workspace, depending on the specified direction.
    """
    axis = ''
    if direction == "front":
        axis = 'x'
    elif direction == "back":
        axis = '-x'
    elif direction == "left":
        axis = '-y'
    elif direction == "right":
        axis = 'y'
    else:
        raise ValueError("Invalid direction provided. Use 'front', 'back', 'left', or 'right'.")
    current_reference = referenceBlock
    for block in blocks:
        move_block_next_to_reference(block, current_reference, axis=axis, gap=gap)
        current_reference = block