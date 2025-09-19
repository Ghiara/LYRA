# TASK: build the letter U, starting in the middle of the workspace

blocks = get_objects()
starting_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
build_letter_U(blocks, starting_pose)