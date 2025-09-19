def place_roof_tiles(roof_tiles: list[TaskObject], specific_pose: Pose):
    """
    Places exactly six roof tiles starting from a specific pose.
    Arranges the roof tiles evenly from the specified starting position and orientation.
    Ensures that the list of roof tiles has exactly six elements before proceeding.
    Args:
    - roof_tiles (list[TaskObject]): A list of TaskObjects identified as roof tiles. Must contain exactly six tiles.
    - specific_pose (Pose): The Pose representing the starting position and orientation for tile placement.
    """
    if len(roof_tiles) != 6:
        raise ValueError("There must be exactly six roof tiles")
    tile_width = roof_tiles[0].size[0]

    # Rotate the tiles by 90 degrees relative to the starting pose
    relative_rotation = specific_pose.rotation * Rotation.from_euler('z', 90, degrees=True)
    adjusted_pose_left = Pose(
        Point3D(specific_pose.position.x, specific_pose.position.y - tile_width / 2, specific_pose.position.z),
        relative_rotation
    )
    put_first_on_second(get_object_pose(roof_tiles[0]), adjusted_pose_left)
    # Place one block on either side of the first block on the left
    move_block_next_to_reference(roof_tiles[1], roof_tiles[0], axis='-y', gap=0.005)
    move_block_next_to_reference(roof_tiles[2], roof_tiles[0], axis='y', gap=0.005)
    # Place the first block of the second set to the right (x direction) of the first block of the first set
    move_block_next_to_reference(roof_tiles[3], roof_tiles[0], axis='x', gap=0.005)
    # Place one block on either side of the first block of the second set
    move_block_next_to_reference(roof_tiles[4], roof_tiles[3], axis='-y', gap=0.005)
    move_block_next_to_reference(roof_tiles[5], roof_tiles[3], axis='y', gap=0.005)