# TASK: build the base of the house in the middle of the workspace

blocks = get_objects()
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0, 1] + workspace.bounds[0, 0]) / 2, (workspace.bounds[1, 1] + workspace.bounds[1, 0]) / 2, 0)
clear_area_size = 0.5
half_clear_area = clear_area_size / 2
clear_area = AABBBoundingBox(minPoint=Point3D(center_of_workspace.x - half_clear_area, center_of_workspace.y - half_clear_area, 0), maxPoint=Point3D(center_of_workspace.x + half_clear_area, center_of_workspace.y + half_clear_area, 0.3))
clear_blocks_from_area(blocks, clear_area)
starting_pose = Pose(center_of_workspace, Rotation.identity())
build_house_base(blocks, starting_pose)