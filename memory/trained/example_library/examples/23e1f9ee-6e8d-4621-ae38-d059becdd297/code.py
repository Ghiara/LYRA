# TASK: put the red block in the center of the workspace, then put the green block on its right side

red_block = get_blocks_by_color(color='red')[0]
green_block = get_blocks_by_color(color='green')[0]
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
red_block_pose = get_object_pose(red_block)
put_first_on_second(red_block_pose, Pose(center_of_workspace, Rotation.identity()))
red_block_size = get_object_size(red_block)
green_block_size = get_object_size(green_block)
right_of_red_block = Point3D(center_of_workspace.x, center_of_workspace.y + red_block_size[1] / 2 + green_block_size[1] / 2 + 0.005, center_of_workspace.z)
green_block_pose = get_object_pose(green_block)
put_first_on_second(green_block_pose, Pose(right_of_red_block, Rotation.identity()))