# TASK: build a block pyramid with a 4 by 4 base in the middle of the workspace

blocks = get_objects()
workspace = Workspace()
block_size = get_object_size(blocks[0])
middle_pose = Pose(Point3D((workspace.bounds[0, 1] + workspace.bounds[0, 0]) / 2, (workspace.bounds[1, 1] + workspace.bounds[1, 0]) / 2, block_size[2] / 2), Rotation.identity())
build_block_pyramid(blocks, (4, 4), middle_pose)