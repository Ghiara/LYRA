# TASK: place the blocks in a circle such that the longer side is pointing towards the center

all_blocks = get_objects()
middle_of_workspace = parse_location_description('middle')
radius = 0.2
arrange_blocks_in_circle(all_blocks, middle_of_workspace, radius)