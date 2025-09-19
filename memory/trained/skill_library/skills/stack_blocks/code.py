def stack_blocks(blocks: list[TaskObject], start_pose: Pose):
    """Stacks a sequence of blocks on top of each other starting from a specified pose.
    Args:
    blocks: A list of TaskObject instances representing the blocks to be stacked.
    start_pose: A Pose indicating the initial position and orientation of the bottom block.
    """
    # Check if there's already a block in the starting position
    all_blocks = get_objects()
    for block in all_blocks:
        block_pose = get_object_pose(block)
        # Check if block is close enough to the starting position, considering some tolerance
        if (
            abs(block_pose.position.x - start_pose.position.x) < 0.05 and
            abs(block_pose.position.y - start_pose.position.y) < 0.05 and
            abs(block_pose.position.z - start_pose.position.z) < 0.05
        ):
            # Move the block to the top-left corner (back_left)
            workspace = Workspace()
            top_left_position = workspace.back_left
            put_first_on_second(block_pose, Pose(top_left_position, Rotation.identity()))
            break

    current_pose = start_pose
    for block in blocks:
        pick_pose = get_object_pose(block)  # Get current pose of the block
        put_first_on_second(pick_pose, current_pose)  # Place block on the current pose
        # Get the size of the block to calculate the new position for the next block
        block_size = get_object_size(block)
        # Update the current pose to place the next block on top
        current_pose = Pose(
            position=Point3D(
                x=current_pose.position.x,
                y=current_pose.position.y,
                z=current_pose.position.z
                + block_size[2],  # Increment z by block height
            ),
            rotation=current_pose.rotation,
        )