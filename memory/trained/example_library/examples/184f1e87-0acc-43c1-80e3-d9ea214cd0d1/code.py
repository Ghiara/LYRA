# TASK: put the red block in the middle of the workspace, then put the green block to the front-right of it

red_block = get_blocks_by_color(color='red')[0]
green_block = get_blocks_by_color(color='green')[0]
workspace = Workspace()
center_of_workspace = parse_location_description('middle')
red_block_pose = get_object_pose(red_block)
put_first_on_second(red_block_pose, Pose(center_of_workspace, Rotation.identity()))
place_block_diagonally_next_to(green_block, red_block, direction='front-right')