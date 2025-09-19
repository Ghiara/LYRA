# TASK: line up all the blocks along the left side of the workspace, starting in the top-left corner

all_blocks = get_objects()
workspace = Workspace()
left_side_start = parse_location_description('top-left corner')
spacing_between_blocks = 0.05
blocks = [obj for obj in all_blocks if obj.category == 'rigid']
make_line_with_blocks(blocks, Pose(left_side_start, Rotation.identity()), spacing_between_blocks)