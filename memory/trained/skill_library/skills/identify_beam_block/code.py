def identify_beam_block(blocks: list[TaskObject]) -> TaskObject:
    """Identifies the beam block from a list of blocks.
    A beam block is defined by the following criteria:
    - It must have the color 'brown'.
    - It has one square side, meaning two side lengths must be the same.
    - The third side should be at least 3 times as long as the square sides.
    Args:
    blocks (list[TaskObject]): The list of block objects to be evaluated.
    Returns:
    TaskObject: Returns the TaskObject identified as a beam block.
    If no beam block is found, returns None.
    """

    for block in blocks:
        if block.color != "brown":
            continue
        width, depth, height = sorted(block.size)
        if width == depth and height >= 3 * width:
            return block
    return None
