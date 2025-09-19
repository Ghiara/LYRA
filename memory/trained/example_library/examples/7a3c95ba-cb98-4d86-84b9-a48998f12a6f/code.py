# TASK: stack the blocks in the middle of the workspace

blocks = get_objects()
center_of_workspace = parse_location_description('middle')
start_pose = Pose(center_of_workspace, Rotation.identity())
stack_blocks(blocks, start_pose)