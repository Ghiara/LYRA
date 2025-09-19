# TASK: build the letter T, starting in the middle of the workspace

all_blocks = get_blocks_by_color()
start_position = Point3D(0.5, 0, 0.02)
start_rotation = Rotation.identity()
starting_pose = Pose(start_position, start_rotation)
assert len(all_blocks) >= 6, "Not enough blocks to form the letter 'T'"
build_letter_T(all_blocks, starting_pose)