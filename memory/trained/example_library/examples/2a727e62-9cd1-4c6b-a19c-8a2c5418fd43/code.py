# TASK: pick up the beam block

all_blocks = get_objects()
beam_block = identify_beam_block(all_blocks)
if beam_block:
    pick(beam_block)
else:
    say('No beam block found.')