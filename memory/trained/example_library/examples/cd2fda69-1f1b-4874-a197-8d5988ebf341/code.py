# TASK: build a jenga tower in the middle of the workspace

blocks = get_objects()
workspace_middle = parse_location_description('middle')
block_size = get_object_size(blocks[0])
base_pose = Pose(Point3D(workspace_middle.x - (block_size[0] * 1.5 + 0.005) / 2, workspace_middle.y, block_size[2] / 2), Rotation.identity())
build_jenga_tower(blocks, base_pose)