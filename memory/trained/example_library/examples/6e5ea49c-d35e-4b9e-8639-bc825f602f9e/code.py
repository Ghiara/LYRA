# TASK: put the red block in the middle, then align the blue blocks towards the right of the workspace

red_blocks = get_blocks_by_color(color='red')
blue_blocks = get_blocks_by_color(color='blue')
red_block = red_blocks[0]
middle_position = parse_location_description('middle')
pick_and_place_special_object(red_block, Pose(middle_position))
make_line_of_blocks_next_to(blue_blocks, red_block, 'right', gap=0.005)