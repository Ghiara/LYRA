# TASK: place the roof tiles on the roof base

objects_in_workspace = get_objects()
roof_tiles = identify_roof_tiles(objects_in_workspace)
roof_base = identify_roof_base(objects_in_workspace)
if roof_base:
    workspace = Workspace()
    center_of_workspace = Point3D((workspace.bounds[0, 0] + workspace.bounds[0, 1]) / 2, (workspace.bounds[1, 0] + workspace.bounds[1, 1]) / 2, roof_base.size[2] / 2)
    roof_base_pose = get_object_pose(roof_base)
    forward_rotation = Rotation.from_euler('z', 0, degrees=True)
    center_pose = Pose(center_of_workspace, forward_rotation)
    put_first_on_second(roof_base_pose, center_pose)
if roof_base and len(roof_tiles) == 6:
    roof_base_pose = get_object_pose(roof_base)
    specific_pose = Pose(Point3D(roof_base_pose.position.x, roof_base_pose.position.y, roof_base_pose.position.z + roof_base.size[2] + 0.01), roof_base_pose.rotation)
    place_roof_tiles(roof_tiles, specific_pose)
else:
    say('Unable to find the roof base or incorrect number of roof tiles.')