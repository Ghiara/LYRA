# TASK: move the end effector to the middle of the right side, then move it in a straight line to the middle of the left side

workspace = Workspace()
middle_of_right_side = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, workspace.bounds[1][1], 0)
end_effector_target_pose = Pose(middle_of_right_side, Rotation.identity())
move_end_effector_to(end_effector_target_pose, speed=0.0001)
middle_of_left_side = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, workspace.bounds[1][0], 0)
num_waypoints = 10
waypoints = [Point3D((1 - t) * middle_of_right_side.x + t * middle_of_left_side.x, (1 - t) * middle_of_right_side.y + t * middle_of_left_side.y, (1 - t) * middle_of_right_side.z + t * middle_of_left_side.z) for t in np.linspace(0, 1, num_waypoints)]
for waypoint in waypoints:
    waypoint_pose = Pose(waypoint, Rotation.identity())
    move_end_effector_to(waypoint_pose, speed=0.0001)
end_effector_target_pose = Pose(middle_of_left_side, Rotation.identity())
move_end_effector_to(end_effector_target_pose, speed=0.0001)