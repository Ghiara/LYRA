# TASK: build the front wall, 4 blocks wide, in the middle of the workspace

blocks = get_objects()
center_of_workspace = parse_location_description('middle')
starting_pose = Pose(center_of_workspace.translate(Point3D(-0.06, -0.06, 0)), Rotation.identity())
construct_front_wall_with_door(blocks, starting_pose)