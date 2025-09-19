# TASK: clear the blocks from the area

workspace = Workspace()
blocks = get_objects()
target_area = AABBBoundingBox(workspace.back_left, workspace.front_right)
clear_blocks_from_area(blocks, target_area)