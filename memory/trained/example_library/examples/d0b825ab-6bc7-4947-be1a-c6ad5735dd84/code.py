# TASK: move the end effector to the middle of the right side

workspace = Workspace()
middle_of_right_side = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, workspace.bounds[1][1], 0)
end_effector_target_pose = Pose(middle_of_right_side, Rotation.identity())
move_end_effector_to(end_effector_target_pose)