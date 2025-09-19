# TASK: place the red block next to the green block

red_block = get_blocks_by_color(color='red')[0]
green_block = get_blocks_by_color(color='green')[0]
move_block_next_to_reference(red_block, green_block, axis='y', gap=0.005)