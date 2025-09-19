def move_end_effector_in_straight_line(start_pose: Pose, end_pose: Pose, speed: float = 0.001):
    """Moves the end effector from the starting Pose to the ending Pose in a straight line at the specified speed."""
    # Use a fixed number of waypoints for simplicity
    num_waypoints = 5
    # Create waypoints for a smooth transition
    waypoints = [Point3D((1 - t) * start_pose.position.x + t * end_pose.position.x,
                         (1 - t) * start_pose.position.y + t * end_pose.position.y,
                         (1 - t) * start_pose.position.z + t * end_pose.position.z)
                 for t in np.linspace(0, 1, num_waypoints)]
    # Move end effector through each waypoint
    for waypoint in waypoints:
        waypoint_pose = Pose(waypoint, Rotation.identity())
        move_end_effector_to(waypoint_pose, speed=speed)