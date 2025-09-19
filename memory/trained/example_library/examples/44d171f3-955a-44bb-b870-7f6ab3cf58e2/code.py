# TASK: align the blocks on the left side of the workspace

all_objects = get_objects()
workspace = Workspace()
blocks = [obj for obj in all_objects if obj.category == 'rigid']
clear_workspace(blocks)