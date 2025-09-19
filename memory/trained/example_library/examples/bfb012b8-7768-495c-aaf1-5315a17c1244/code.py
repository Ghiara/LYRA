# TASK: stack the blocks in the middle of the workspace (i.e. Point3D(x=0.5, y=0, z=0))

blocks = get_objects()
workspace = Workspace()
center_of_workspace = workspace.middle
start_pose = Pose(center_of_workspace, Rotation.identity())
stack_blocks(blocks, start_pose)