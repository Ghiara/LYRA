# TASK: put the red block in the middle of the workspace, then line up the blue blocks next to it, towards the back of the workspace

red_block = get_blocks_by_color(color='red')[0]
blue_blocks = get_blocks_by_color(color='blue')
middle_point = parse_location_description('middle')
red_block_pose = Pose(middle_point, Rotation.identity())
put_first_on_second(get_object_pose(red_block), red_block_pose)
make_line_of_blocks_next_to(blue_blocks, red_block, direction='back', gap=0.005)