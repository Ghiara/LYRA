# TASK: build a zigzag tower with 6 blocks, stacking 3 blocks in one direction and 3 in the other

blocks = get_objects()
workspace_middle = Workspace.middle
base_pose = Pose(workspace_middle, Rotation.identity())
zigzag_angle = 45
build_zigzag_tower(blocks, base_pose, zigzag_angle)