# TASK: build the letter U, starting in the middle of the workspace, using 9 blocks

blocks = get_blocks_by_color()
starting_pose = Pose(Point3D(0.5, 0.0, 0.02), Rotation.identity())
build_letter_U(blocks, starting_pose)