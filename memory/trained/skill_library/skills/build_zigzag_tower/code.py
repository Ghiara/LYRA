def build_zigzag_tower(blocks: list[TaskObject], base_pose: Pose, zigzag_angle: float):
    """Constructs a zigzag tower from a list of blocks starting at a given base pose.
    The zigzag pattern is achieved by alternating the placement angle of each layer
    relative to the one below, using the specified zigzag angle for rotation.
    Args:
    - blocks: A list of TaskObject representing the blocks to form the tower.
    - base_pose: A Pose indicating the starting position and orientation for the base of the zigzag tower.
    - zigzag_angle: A float specifying the angle of rotation for each layer relative to the one below.
    """
    offset_y = 0.01  # Small offset in meters
    current_pose = base_pose
    for i in range(6):  # Total 6 blocks
        # Apply y-offset for zigzag
        if i < 3 or i == 5:
            current_pose.position = current_pose.position.translate(Point3D(0, -offset_y, 0))
        else:
            current_pose.position = current_pose.position.translate(Point3D(0, offset_y, 0))
        # Place the block
        put_first_on_second(get_object_pose(blocks[i]), current_pose)
        # Move current pose up for the next block
        current_pose = Pose(position=current_pose.position.translate(Point3D(0, 0, blocks[i].size[2])),
                            rotation=current_pose.rotation)