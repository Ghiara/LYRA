def build_jenga_tower(blocks: list[TaskObject], base_pose: Pose):
    """ 
    Arranges a list of blocks into a Jenga tower formation.
    The tower begins at the specified base pose, with blocks stacked 
    three at a time per layer, alternating the direction of each layer 
    between parallel and perpendicular to the one below.
    Args:
    - blocks: A list of TaskObject representing the Jenga blocks to be used.
    - base_pose: A Pose indicating the starting position and orientation
      for the bottom center of the Jenga tower.
    """
    num_layers = len(blocks) // 3
    spacing = 0.005
    # Calculate block size from the first block
    block_size = get_object_size(blocks[0])
    offset = block_size[0] + spacing
    # Clear the workspace area where the tower will be built
    # Create an AABB around the base_pose to clear the area
    target_area_min = Point3D(base_pose.position.x - block_size[0] * 1.5, base_pose.position.y - block_size[1] * 1.5, 0)
    target_area_max = Point3D(base_pose.position.x + block_size[0] * 1.5, base_pose.position.y + block_size[1] * 1.5, block_size[2] * num_layers)
    target_area = AABBBoundingBox(minPoint=target_area_min, maxPoint=target_area_max)
    clear_blocks_from_area(blocks, target_area)
    for i in range(num_layers):
        layer_blocks = blocks[i*3:(i*3)+3]
        # Adjust the pose to alternate direction every layer
        if i % 2 == 0:
            layer_pose = Pose(Point3D(base_pose.position.x, base_pose.position.y, base_pose.position.z + i * block_size[2]), base_pose.rotation)
        else:
            new_rotation = base_pose.rotation * Rotation.from_euler('z', 90, degrees=True)
            layer_pose = Pose(Point3D(base_pose.position.x, base_pose.position.y, base_pose.position.z + i * block_size[2]), new_rotation)
        build_jenga_layer(layer_blocks, layer_pose, spacing)