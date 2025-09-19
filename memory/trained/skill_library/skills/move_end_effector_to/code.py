def move_end_effector_to(pose: Pose, speed=0.001):
    """moves the end effector from its current Pose to a given new Pose"""
    max_steps = 100
    step = 0
    while (
        not np.allclose(pose.position.np_vec, ee_pose.position.np_vec, atol=1e-3)
        or not np.allclose(
            pose.rotation.as_matrix(), ee_pose.rotation.as_matrix(), atol=1e-3
        )
    ) and step < max_steps:
        env.movep(_to_pybullet_pose(pose), speed=speed)
        env.step_simulation()
        ee_pose = get_end_effector_pose()
        step += 1
