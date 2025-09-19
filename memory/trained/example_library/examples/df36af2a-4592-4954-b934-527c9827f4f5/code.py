# TASK: write the letter x in the middle of the workspace

center_of_workspace = parse_location_description('middle')
starting_pose = Pose(center_of_workspace, Rotation.identity())
letter = 'X'
blocks = get_objects()
write_letter_with_blocks(letter, starting_pose, blocks)