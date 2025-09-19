# TASK: build a tilting tower with 3 blocks in the middle of the workspace

blocks = get_objects()
middle_of_workspace = Workspace.middle
base_pose = Pose(middle_of_workspace, Rotation.identity())
tilt_offset = 0.015
build_leaning_tower(blocks, base_pose, tilt_offset)