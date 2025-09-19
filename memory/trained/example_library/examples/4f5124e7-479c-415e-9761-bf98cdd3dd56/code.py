# TASK: put the red block in the middle, then line up the blue blocks next to it towards the left of the workspace

red_block = get_blocks_by_color('red')[0]
blue_blocks = get_blocks_by_color('blue')
middle_position = parse_location_description('middle')
pick_and_place_special_object(red_block, Pose(middle_position))
make_line_of_blocks_next_to(blue_blocks, red_block, direction='left')