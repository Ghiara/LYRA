def move_block_next_to_reference(
    block: TaskObject, referenceBlock: TaskObject, axis: str = "x", gap: float = 0.005
):
    """Moves the block next to the referenceBlock such that their edges are aligned along the specified axis with a small gap.
    Args:
        block (TaskObject): The block object to be moved and aligned.
        referenceBlock (TaskObject): The block object that remains stationary and serves as the reference.
        axis (str): The axis along which to align the blocks. Should be 'x', '-x', 'y', or '-y'.
        gap (float, optional): The small gap to leave between the blocks. Defaults to 0.005 meters.
    Raises:
        ValueError: If the specified axis is not 'x', '-x', 'y', or '-y'.
    """
    if axis not in ["x", "-x", "y", "-y"]:
        raise ValueError("Axis must be either 'x', '-x', 'y', or '-y'.")
    # Get the pose and size of the blocks
    block_pose = get_object_pose(block)
    reference_pose = get_object_pose(referenceBlock)
    reference_size = get_object_size(referenceBlock)
    block_size = get_object_size(block)
    # Determine the offset distance based on the axis
    if axis == "x":
        offset = (reference_size[0] + block_size[0]) / 2 + gap
        direction = np.array([1, 0, 0])  # positive x-axis direction
    elif axis == "-x":
        offset = (reference_size[0] + block_size[0]) / 2 + gap
        direction = np.array([-1, 0, 0])  # negative x-axis direction
    elif axis == "y":
        offset = (reference_size[1] + block_size[1]) / 2 + gap
        direction = np.array([0, 1, 0])  # positive y-axis direction
    elif axis == "-y":
        offset = (reference_size[1] + block_size[1]) / 2 + gap
        direction = np.array([0, -1, 0])  # negative y-axis direction

    rotated_direction = reference_pose.rotation.apply(direction)
    new_position = reference_pose.position.np_vec + offset * rotated_direction
    new_position = Point3D.from_xyz(new_position)
    # New pose for the block with the same rotation as the reference
    new_pose = Pose(position=new_position, rotation=reference_pose.rotation)
    # Move the block
    put_first_on_second(block_pose, new_pose)
