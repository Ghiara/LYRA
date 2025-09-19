# TASK: build a 3 by 2 block pyramid

blocks = get_objects()
workspace = Workspace()
block_size = get_object_size(blocks[0])
starting_pose = Pose(Point3D((workspace.bounds[0, 1] + workspace.bounds[0, 0]) / 2, (workspace.bounds[1, 1] + workspace.bounds[1, 0]) / 2, block_size[2] / 2), Rotation.identity())
build_block_pyramid(blocks, (3, 2), starting_pose)