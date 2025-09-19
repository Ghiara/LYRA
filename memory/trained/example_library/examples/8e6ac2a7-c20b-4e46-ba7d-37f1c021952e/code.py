# TASK: build a 3*2 block pyramid, rotated by 45 degrees in the middle of the workspace

blocks = get_objects()
workspace = Workspace()
block_size = get_object_size(blocks[0])
middle_position = Point3D((workspace.bounds[0, 1] + workspace.bounds[0, 0]) / 2, (workspace.bounds[1, 1] + workspace.bounds[1, 0]) / 2, block_size[2] / 2)
starting_pose = Pose(middle_position, Rotation.identity())
build_block_pyramid(blocks, (3, 2), starting_pose)