def build_house_base(blocks: list[TaskObject], pose: Pose):
    """Constructs the base of a house in the workspace using a list of block TaskObjects starting from a specified pose.
    Args:
    blocks (list[TaskObject]): A list of blocks to use in forming the base of a house. Each block should have uniform attributes such as size and color.
    startingPose (Pose): The starting position and orientation in the workspace from which to begin constructing the base of the house.
    """

    block_width = get_object_size(blocks[0])[0]
    startingPose = Pose(
        pose.position.translate(Point3D(1.5 * block_width, -block_width, 0)),
        pose.rotation,
    )

    # make the front left corner of the house
    stack_blocks(blocks[0:2], startingPose)

    # leave a gap of one block width
    next_stack_position = get_point_at_distance_and_rotation_from_point(
        startingPose.position,
        startingPose.rotation,
        block_width * 2,
        direction=(0, 1, 0),
    )
    stack_blocks(blocks[2:4], Pose(next_stack_position, startingPose.rotation))

    # make lines towards the back of the workspace from each of the stacks
    make_line_of_blocks_next_to(blocks[4:6], blocks[0], "back")
    make_line_of_blocks_next_to(blocks[6:8], blocks[3], "back")

    # make the back wall of the house
    back_wall_start_pos = get_point_at_distance_and_rotation_from_point(
        get_object_pose(blocks[5]).position,
        startingPose.rotation,
        block_width + 0.005,
        direction=(-1, 0, 0),
    )

    build_structure_from_blocks(
        blocks[8:14], (1, 3, 2), Pose(back_wall_start_pos, startingPose.rotation)
    )
