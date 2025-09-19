# TASK: put the red block in the middle, then put the green block to the back-right of it

red_block = get_blocks_by_color(color='red')[0]
green_block = get_blocks_by_color(color='green')[0]
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
red_block_pose = get_object_pose(red_block)
put_first_on_second(red_block_pose, Pose(center_of_workspace, Rotation.identity()))
place_block_diagonally_next_to(green_block, red_block, direction='back-right')