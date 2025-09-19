# TASK: put the red block next to the blue block, on its right side

red_block = get_blocks_by_color(color='red')[0]
blue_block = get_blocks_by_color(color='blue')[0]
move_block_next_to_reference(red_block, blue_block, axis='y', gap=0.005)