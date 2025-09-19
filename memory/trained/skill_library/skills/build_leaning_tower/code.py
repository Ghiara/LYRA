def build_leaning_tower(blocks: list[TaskObject], base_pose: Pose, tilt_offset: float):
    """Constructs a leaning tower from a list of blocks starting at a given base pose.
    The tower will lean with a specified tilt offset while maintaining stability.
    Args:
    - blocks: A list of TaskObject representing the building blocks for the tower.
    - base_pose: A Pose indicating the starting position and orientation for the base of the leaning tower.
    - tilt_offset: A float specifying the horizontal translation of the top of the tower from the base center.
    """
    number_of_blocks = len(blocks)
    if number_of_blocks < 3:
        raise ValueError("At least 3 blocks are required to build a leaning tower.")
    # Assuming the blocks are roughly calculated the same size, for this example, we will use the size of the first block.
    block_size = get_object_size(blocks[0])
    # Start building the leaning tower
    current_pose = base_pose
    for index, block in enumerate(blocks):
        # Calculate the offset for the current block based on its height and the index in the stack
        # Make the tilt offset smaller by adjusting this calculation
        horizontal_shift = (tilt_offset / (number_of_blocks)) * index  # Reduced tilt offset
        vertical_shift = block_size[2]  # Height shift, assuming blocks are placed directly on top of each other
        # New position for the block, tilting towards the left (negative y-axis)
        new_position = Point3D(
            current_pose.position.x,
            current_pose.position.y - horizontal_shift,
            current_pose.position.z + vertical_shift
        )
        # Place the block with calculated new position
        put_first_on_second(get_object_pose(block), Pose(new_position, current_pose.rotation))
        # Update the current pose for the next block
        current_pose = Pose(new_position, current_pose.rotation)