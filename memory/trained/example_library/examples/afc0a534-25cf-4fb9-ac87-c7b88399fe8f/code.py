# TASK: put the block in the top left corner

block = get_objects()[0]
block_pose = get_object_pose(block)
top_left_corner_position = parse_location_description('top left corner')
put_first_on_second(block_pose, Pose(top_left_corner_position, Rotation.identity()))