# TASK: put the block in the bottom right corner

block = get_objects()[0]
block_pose = get_object_pose(block)
bottom_right_corner_position = parse_location_description('bottom right corner')
put_first_on_second(block_pose, Pose(bottom_right_corner_position, Rotation.identity()))