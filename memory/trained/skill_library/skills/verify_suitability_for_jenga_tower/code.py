from utils.core_types import *
import get_object_size


def verify_suitability_for_jenga_tower(block: TaskObject) -> bool:
    """
    Verify if the given block is suitable for a Jenga tower.
    A block is considered suitable if one dimension is exactly 3 times one of its other dimensions.
    Args:
    - block: TaskObject representing the block to be verified.
    Returns:
    - bool: True if the block is suitable for use in a Jenga tower, False otherwise.
    """
    # Retrieve the block size
    block_size = get_object_size(block)
    # Check the dimension criteria for Jenga block suitability
    for i in range(3):
        for j in range(3):
            if i != j and abs(block_size[i] - 3 * block_size[j]) <= 0.0001:
                return True
    return False
