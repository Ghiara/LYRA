# TASK: build a 3*3*3 cube

blocks = get_objects()
starting_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
build_structure_from_blocks(blocks, (3, 3, 3), starting_pose)