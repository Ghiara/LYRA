# TASK: move the end effector so it touches the middle of the workspace

workspace = Workspace()
middle_of_surface = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, workspace.bounds[2][0] - 0.1)
end_effector_target_pose = Pose(middle_of_surface, Rotation.identity())
move_end_effector_to(end_effector_target_pose)