# TASK: pick the block a little bit, don't drop it, and then rotate it by 45 degrees

all_blocks = get_objects()
block_to_pick = all_blocks[0]
pick(block_to_pick)
end_effector_pose = get_end_effector_pose()
lifted_position = Point3D(end_effector_pose.position.x, end_effector_pose.position.y, end_effector_pose.position.z + 0.1)
lifted_pose = Pose(lifted_position, end_effector_pose.rotation)
move_end_effector_to(lifted_pose)
rotation_45_degrees_xy = Rotation.from_euler('z', 45, degrees=True).as_matrix()
new_rotation = end_effector_pose.rotation.as_matrix()
new_rotation[:2, :2] = rotation_45_degrees_xy[:2, :2]
rotated_pose = Pose(lifted_position, Rotation.from_matrix(new_rotation))
move_end_effector_to(rotated_pose)