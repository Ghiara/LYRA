from utils.core_types import *


def build_structure_from_blocks(
    blocks: list[TaskObject],
    dimensions: tuple[int, int, int],
    pose: Pose,
    gap: float = 0.005,
):
    """
    Assembles a structure using individual block TaskObjects based on the specified dimensions and the given pose.
    The blocks should be positioned to form the desired structure starting from the given pose, which specifies the position and orientation of the first block placed.
    Assumes that the list 'blocks' contains enough block TaskObjects to construct the specified structure.
    Assumes the blocks are homogeneous in size.
    Arranges the blocks to form a 3D structure of the given dimensions.
    """
    if len(dimensions) != 3:
        raise ValueError("Dimensions should be a tuple of three integers.")

    block_size = get_object_size(blocks[0])
    block_index = 0

    for z in range(dimensions[2]):
        layer_blocks = blocks[block_index : block_index + dimensions[0] * dimensions[1]]
        layer_start_position = get_point_at_distance_and_rotation_from_point(
            pose.position,
            pose.rotation,
            (block_size[2] + gap) * z,
            direction=np.array([0, 0, 1]),
        )
        layer_start_pose = Pose(layer_start_position, pose.rotation)
        for y in range(dimensions[1]):
            row_blocks = layer_blocks[y * dimensions[0] : (y + 1) * dimensions[0]]
            row_start_position = get_point_at_distance_and_rotation_from_point(
                layer_start_pose.position,
                layer_start_pose.rotation,
                (block_size[1] + gap) * y,
                direction=np.array([0, 1, 0]),
            )
            row_start_pose = Pose(row_start_position, layer_start_pose.rotation)
            make_line_with_blocks(row_blocks, row_start_pose, gap=gap)
        block_index += dimensions[0] * dimensions[1]
