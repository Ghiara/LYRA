# TASK: line up all the blocks from the red block - don't move the red block, just move all the other blocks so they are in one line with it

red_block = get_blocks_by_color(color='red')[0]
red_block_pose = get_object_pose(red_block)
spacing_between_blocks = 0.05
start_position = get_point_at_distance_and_rotation_from_point(red_block_pose.position, red_block_pose.rotation, spacing_between_blocks)
start_rotation = red_block_pose.rotation
all_blocks = get_objects()
blocks_to_line_up = [block for block in all_blocks if block.id != red_block.id]
make_line_with_blocks(blocks_to_line_up, Pose(start_position, start_rotation), spacing_between_blocks)