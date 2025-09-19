# TASK: assemble the roof in the middle of the workspace

objects_in_workspace = get_objects()
base = identify_roof_base(objects_in_workspace)
roof_beam = identify_beam_block(objects_in_workspace)
roof_tiles = identify_roof_tiles(objects_in_workspace)
if base and roof_beam and (len(roof_tiles) == 6):
    workspace = Workspace()
    center_of_workspace = Point3D((workspace.bounds[0, 0] + workspace.bounds[0, 1]) / 2, (workspace.bounds[1, 0] + workspace.bounds[1, 1]) / 2, base.size[2] / 2)
    overall_pose = Pose(center_of_workspace, Rotation.identity())
    assemble_roof(base, roof_beam, roof_tiles, overall_pose)
else:
    say('Unable to find all necessary components for the roof assembly.')