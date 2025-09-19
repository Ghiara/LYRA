# TASK: build a 2*2*2 cube made of the blocks

blocks = get_blocks_by_color()
starting_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
build_structure_from_blocks(blocks, (2, 2, 2), starting_pose)