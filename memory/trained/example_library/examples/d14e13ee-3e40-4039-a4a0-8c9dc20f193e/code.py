# TASK: move the end effector from the middle of the right side to the middle of the left side

workspace = Workspace()
middle_of_right_side = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, workspace.bounds[1][1], 0)
middle_of_left_side = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, workspace.bounds[1][0], 0)
start_pose = Pose(middle_of_right_side, Rotation.identity())
end_pose = Pose(middle_of_left_side, Rotation.identity())
move_end_effector_in_straight_line(start_pose, end_pose, speed=0.0001)