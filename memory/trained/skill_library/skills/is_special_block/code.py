from utils.core_types import *

def is_special_block(block: TaskObject) -> bool:
    """ 
    Verify whether a block is a special block based on predefined criteria:
    A special block is defined as having the color 'red' and exactly two sides that are the same length, with one side that is a different length.
    Args:
    block (TaskObject): The block object to be verified.
    Returns:
    bool: Returns True if the block meets the criteria for being a special block, else False.
    """
    if block.color.lower() != 'red':
        return False
    size = get_object_size(block)
    unique_dims = set(size)
    # Check if there are exactly 2 unique dimensions, which corresponds to 2 equal sides and 1 differing side
    return len(unique_dims) == 2