# TASK: put the special object in the top-left corner of the workspace

all_objects = get_objects()
special_object = next((obj for obj in all_objects if is_special_block(obj)), None)
if special_object:
    top_left_corner_point = parse_location_description('top-left corner')
    place_pose = Pose(top_left_corner_point, Rotation.identity())
    pick_and_place_special_object(special_object, place_pose)
else:
    say('No special object found in the workspace.')