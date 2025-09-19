# TASK: put the red block in the middle of the workspace, then place the green block to the left of it

red_block = get_blocks_by_color(color='red')[0]
green_block = get_blocks_by_color(color='green')[0]
workspace = Workspace()
center_of_workspace = parse_location_description('middle')
red_block_pose = get_object_pose(red_block)
put_first_on_second(red_block_pose, Pose(center_of_workspace, Rotation.identity()))
move_block_next_to_reference(green_block, red_block, axis='-y', gap=0.005)