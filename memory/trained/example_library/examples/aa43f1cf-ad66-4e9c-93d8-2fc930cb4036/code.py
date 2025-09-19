# TASK: put the red block in the middle, rotated at 30 degrees, then put the blue block on its right side

red_block = get_blocks_by_color(color='red')[0]
blue_block = get_blocks_by_color(color='blue')[0]
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
red_block_pose = get_object_pose(red_block)
rotation_30_degrees = Rotation.from_euler('z', 30, degrees=True)
put_first_on_second(red_block_pose, Pose(center_of_workspace, rotation_30_degrees))
move_block_next_to_reference(blue_block, red_block, axis='y', gap=0.005)