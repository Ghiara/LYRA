# TASK: place one blue block on each side of the red block

red_block = get_blocks_by_color(color='red')[0]
blue_blocks = get_blocks_by_color(color='blue')
red_block_pose = get_object_pose(red_block)
red_block_size = get_object_size(red_block)
move_block_next_to_reference(blue_blocks[0], red_block, axis='-y', gap=0.005)
move_block_next_to_reference(blue_blocks[1], red_block, axis='y', gap=0.005)
move_block_next_to_reference(blue_blocks[2], red_block, axis='x', gap=0.005)
move_block_next_to_reference(blue_blocks[3], red_block, axis='-x', gap=0.005)