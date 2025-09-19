def get_block_side_position(block: TaskObject, side: str) -> Point3D:
    """gets the specified side of the block
    valid sides are: "front", "back", "left", "right"
    """
    pose = get_object_pose(block)
    size = get_object_size(block)
    side_positions = []
    side_positions.append(
        get_point_at_distance_and_rotation_from_point(
            pose.position, pose.rotation, size[0], (1, 0, 0)
        )
    )
    side_positions.append(
        get_point_at_distance_and_rotation_from_point(
            pose.position, pose.rotation, size[0], (-1, 0, 0)
        )
    )
    side_positions.append(
        get_point_at_distance_and_rotation_from_point(
            pose.position, pose.rotation, size[1], (0, 1, 0)
        )
    )
    side_positions.append(
        get_point_at_distance_and_rotation_from_point(
            pose.position, pose.rotation, size[1], (0, -1, 0)
        )
    )

    pos = get_closest_point_to_side(side_positions, side)
    return pos
