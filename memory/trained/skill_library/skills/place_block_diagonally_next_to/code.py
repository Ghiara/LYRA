def place_block_diagonally_next_to(
    block: TaskObject, referenceBlock: TaskObject, direction: str
):
    """Places the specified block diagonally adjacent to the reference block.
    This function will position the given block next to the reference block,
    such that the new block is diagonally aligned relative to the reference block's position
    on the x-y plane within the workspace. The direction should specify whether the block
    is placed towards the "front-back" and "left-right" directions.
    Args:
        block: The TaskObject representing the block to be placed.
        referenceBlock: The TaskObject representing the reference block next to which the new block will be placed.
        direction: A string indicating the direction in which to place the block relative to the reference block.
                   Valid directions are combinations of "front" or "back" with "left" or "right", e.g., "front-left", "back-right".
    """
    reference_pose = get_object_pose(referenceBlock)
    block_size = get_object_size(block)
    reference_size = get_object_size(referenceBlock)
    dx = dy = 0
    gap = 0.005
    if "front" in direction:
        dx = reference_size[0] / 2 + block_size[0] / 2 + gap
    elif "back" in direction:
        dx = -(reference_size[0] / 2 + block_size[0] / 2 + gap)
    if "right" in direction:
        dy = reference_size[1] / 2 + block_size[1] / 2 + gap
    elif "left" in direction:
        dy = -(reference_size[1] / 2 + block_size[1] / 2 + gap)
    target_position = get_point_at_distance_and_rotation_from_point(
        reference_pose.position, reference_pose.rotation, dx, (1, 0, 0)
    )
    target_position = get_point_at_distance_and_rotation_from_point(
        target_position, reference_pose.rotation, dy, (0, 1, 0)
    )

    placePose = Pose(target_position, reference_pose.rotation)
    put_first_on_second(get_object_pose(block), placePose)
