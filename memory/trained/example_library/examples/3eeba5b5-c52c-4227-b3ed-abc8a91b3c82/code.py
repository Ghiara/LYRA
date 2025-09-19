# TASK: build a 4*2*2 structure in the top-left corner of the workspace

blocks = get_objects()
workspace = Workspace()
top_left_corner = parse_location_description('top-left corner')
block_size = get_object_size(blocks[0])
start_pose = Pose(Point3D(workspace.bounds[0, 0] + block_size[0] / 2, workspace.bounds[1, 0] + block_size[1] / 2, block_size[2] / 2), Rotation.identity())
build_structure_from_blocks(blocks, (4, 2, 2), start_pose)