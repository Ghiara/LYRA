# TASK: place the roof tiles in the middle of the workspace

all_objects = get_objects()
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0, 0] + workspace.bounds[0, 1]) / 2, (workspace.bounds[1, 0] + workspace.bounds[1, 1]) / 2, 0)
roof_tiles = identify_roof_tiles(all_objects)
specific_pose = Pose(center_of_workspace, Rotation.identity())
place_roof_tiles(roof_tiles, specific_pose)