# TASK: pick up the blocks that are suitable for jenga

blocks = get_objects()
workspace_middle = parse_location_description('middle')
suitable_blocks = [block for block in blocks if verify_suitability_for_jenga_tower(block)]
for block in suitable_blocks:
    block_pose = get_object_pose(block)
    place_pose = Pose(Point3D(workspace_middle.x, workspace_middle.y, block_pose.position.z), Rotation.identity())
    put_first_on_second(block_pose, place_pose)