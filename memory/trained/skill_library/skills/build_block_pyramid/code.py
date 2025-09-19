from utils.core_types import *


def build_block_pyramid(
    blocks: list[TaskObject], base_dimension: tuple[int, int], pose: Pose
):
    """builds a pyramid of blocks with the given base dimension and pose
    for each layer, reduce the base_dimension by 1 along each axis
    """
    # Determine the bounding box for the clearing area
    block_size = get_object_size(blocks[0])

    # Initialize current pose and dimensions
    current_pose = pose
    current_dimensions = base_dimension
    start_index = 0
    while current_dimensions[0] > 0 and current_dimensions[1] > 0:
        # Use a different set of blocks for each layer
        layer_blocks = blocks[
            start_index : start_index + current_dimensions[0] * current_dimensions[1]
        ]
        build_structure_from_blocks(
            layer_blocks,
            (current_dimensions[0], current_dimensions[1], 1),
            current_pose,
        )
        # Adjust indices for the next layer
        start_index += current_dimensions[0] * current_dimensions[1]
        # For the next layer, reduce dimensions by 1
        current_dimensions = (current_dimensions[0] - 1, current_dimensions[1] - 1)
        # Move pose upwards and towards the center of the current layer to start new layer
        offset = Point3D(block_size[0] / 2, block_size[1] / 2, block_size[2])
        current_pose = Pose(
            Point3D(
                current_pose.position.x + offset.x,
                current_pose.position.y + offset.y,
                current_pose.position.z + offset.z,
            ),
            current_pose.rotation,
        )
