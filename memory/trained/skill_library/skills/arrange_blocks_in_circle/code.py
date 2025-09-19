def arrange_blocks_in_circle(blocks: list[TaskObject], center: Point3D, radius: float):
    """Arranges blocks in a circle around a given center point, with each block's longer side rotated to face the center.
    Args:
        blocks (list[TaskObject]): List of block objects to be arranged.
        center (Point3D): The center point of the circle.
        radius (float): The radius of the circle on which the blocks will be placed.
    """
    num_blocks = len(blocks)
    angle_increment = 2 * np.pi / num_blocks
    for i, block in enumerate(blocks):
        # Calculate angle for current block
        angle = i * angle_increment
        # Determine block position on the circle
        x = center.x + radius * np.cos(angle)
        y = center.y + radius * np.sin(angle)
        # Calculate rotation so that each block is rotated by 90 degrees relative to its position towards the center
        rotation_angle = np.arctan2(center.y - y, center.x - x)
        rotation = Rotation.from_euler('z', rotation_angle)
        # Position and rotate the block
        pick_pose = get_object_pose(block)
        place_pose = Pose(Point3D(x, y, pick_pose.position.z), rotation)
        put_first_on_second(pick_pose, place_pose)