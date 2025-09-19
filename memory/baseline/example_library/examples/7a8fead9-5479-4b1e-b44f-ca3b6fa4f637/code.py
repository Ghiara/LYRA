# TASK: rotate the blue block by 45 degrees


objects = get_objects()
red_block = next(block for block in objects if block.objectType == "block" and block.color == "blue")
red_block_pose = get_object_pose(red_block)
rotated_pose = Pose(red_block_pose.position, red_block_pose.rotation * Rotation.from_euler('z', 90, degrees=True))
put_first_on_second(red_block_pose, rotated_pose)
