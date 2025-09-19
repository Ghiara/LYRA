# TASK: build a 2*2*2 cube, rotated by 45 degrees

blocks = get_blocks_by_color()
starting_position = Point3D(0.3, 0.0, 0.05)
rotation_45_degrees = Rotation.from_euler("z", 45, degrees=True)
starting_pose = Pose(starting_position, rotation_45_degrees)
build_structure_from_blocks(blocks, (2, 2, 2), starting_pose)
