# TASK: move the smallest block 10cm to the left


objects = get_objects()
smallest_block = min(objects, key=lambda x: x.size[0])
smallest_block_pose = get_object_pose(smallest_block)
translated_pose = Pose(smallest_block_pose.position.translate(Point3D(0, -0.1, 0)), smallest_block_pose.rotation)
put_first_on_second(smallest_block_pose, translated_pose)
