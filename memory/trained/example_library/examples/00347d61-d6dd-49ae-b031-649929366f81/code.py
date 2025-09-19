# TASK: put the block in the bottom left corner

block = get_objects()[0]
block_pose = get_object_pose(block)
bottom_left_corner_position = parse_location_description('bottom left corner')
put_first_on_second(block_pose, Pose(bottom_left_corner_position, Rotation.identity()))