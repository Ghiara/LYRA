# TASK: stack all the roof tiles on the left side of the workspace

all_objects = get_objects()
workspace = Workspace()
left_side_start = parse_location_description('top-left corner')
roof_tiles = identify_roof_tiles(all_objects)
place_pose = Pose(left_side_start, Rotation.identity())
for roof_tile in roof_tiles:
    put_first_on_second(get_object_pose(roof_tile), place_pose)
    place_pose.position.z += roof_tile.size[2] + 0.005