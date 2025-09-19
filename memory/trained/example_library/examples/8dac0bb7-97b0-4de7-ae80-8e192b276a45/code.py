# TASK: place the blocks in a smiley face arrangement: use one cylinder for each eye, and the block for the mouth

objects = get_objects()
cylinders = [obj for obj in objects if obj.objectType == 'cylinder']
blocks = [obj for obj in objects if obj.objectType != 'cylinder']
smiley_center_pose = Pose(Point3D(0.5, 0, 0.05), Rotation.identity())
place_smiley_face_features(cylinders[0], cylinders[1], blocks[0], smiley_center_pose)