# TASK: construct the front wall of a house, 3 blocks wide

blocks = get_objects()
starting_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
construct_front_wall_with_door(blocks, starting_pose)