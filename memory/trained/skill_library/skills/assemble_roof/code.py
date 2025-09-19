def assemble_roof(base: TaskObject, roof_beam: TaskObject, roof_tiles: list[TaskObject], overall_pose: Pose):
    """
    Assembles a roof structure using a designated base, a roof beam, and a list of roof tiles, starting from a given overall pose.
    The base acts as the foundation while the roof beam provides structural support and the roof tiles are placed on top to complete the structure.
    Args:
    - base (TaskObject): The TaskObject representing the base upon which the roof is built.
    - roof_beam (TaskObject): The TaskObject representing the beam supporting the roof tiles between the base and the tiles.
    - roof_tiles (list[TaskObject]): A list of TaskObjects representing the roof tiles to be placed on the beam.
    - overall_pose (Pose): The Pose indicating the overall position and orientation for the roof assembly.
    """
    # Place base in the middle of the workspace
    put_first_on_second(get_object_pose(base), overall_pose)
    # Compute the pose for the roof beam
    base_pose = get_object_pose(base)
    beam_pose = Pose(
        Point3D(
            base_pose.position.x, 
            base_pose.position.y, 
            base_pose.position.z + (base.size[2] / 2) + (roof_beam.size[2] / 2)
        ),
        base_pose.rotation
    )
    # Place beam on the base
    put_first_on_second(get_object_pose(roof_beam), beam_pose)
    # Compute the pose for the roof tiles on top of the beam
    beam_pose = get_object_pose(roof_beam)
    roof_tiles_pose = Pose(
        Point3D(
            beam_pose.position.x, 
            beam_pose.position.y, 
            beam_pose.position.z + roof_beam.size[2] / 2 + 0.01
        ),
        beam_pose.rotation
    )
    # Place roof tiles
    place_roof_tiles(roof_tiles, roof_tiles_pose)