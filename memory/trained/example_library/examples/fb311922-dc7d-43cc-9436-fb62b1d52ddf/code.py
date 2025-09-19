# TASK: line up the 4 blocks

blocks = get_blocks_by_color()
starting_pose = Pose(Point3D(0.3, 0, 0), Rotation.identity())
spacing_between_blocks = 0.05
make_line_with_blocks(blocks, starting_pose, spacing_between_blocks)