# TASK: build the front wall of a house, with a door in the middle

blocks = get_objects()
starting_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
construct_front_wall_with_door(blocks, starting_pose)