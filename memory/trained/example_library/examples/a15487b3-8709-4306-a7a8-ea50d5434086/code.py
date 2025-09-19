# TASK: move the end effector to the top left corner of the workspace

workspace = Workspace()
top_left_corner = parse_location_description('top-left corner')
end_effector_target_pose = Pose(top_left_corner, Rotation.identity())
move_end_effector_to(end_effector_target_pose)