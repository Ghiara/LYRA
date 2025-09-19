# TASK: build the letter T, starting in the middle of the workspace, using 8 blocks

blocks = get_objects()
center_of_workspace_pose = Pose(Point3D((0.25 + 0.75) / 2, 0, 0), Rotation.identity())
build_letter_T(blocks[:8], center_of_workspace_pose)