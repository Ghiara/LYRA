# TASK: put the block in the top right corner

block = get_objects()[0]
block_pose = get_object_pose(block)
top_right_corner_position = parse_location_description('top right corner')
put_first_on_second(block_pose, Pose(top_right_corner_position, Rotation.identity()))