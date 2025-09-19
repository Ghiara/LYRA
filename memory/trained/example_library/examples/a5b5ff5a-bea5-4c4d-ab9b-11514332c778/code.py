# TASK: build the letter M, starting in the middle of the workspace

workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
initial_pose = Pose(center_of_workspace, Rotation.identity())
all_blocks = get_objects()
build_letter_M(all_blocks, initial_pose)