# TASK: put the block in the middle of the workspace

block = get_objects()[0]
block_pose = get_object_pose(block)
middle_position = parse_location_description('middle')
put_first_on_second(block_pose, Pose(middle_position, Rotation.identity()))