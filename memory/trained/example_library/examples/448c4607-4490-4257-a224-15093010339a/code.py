# TASK: place the blocks in a circle such that their longer side is rotated towards the center

all_blocks = get_objects()
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
radius = 0.2
arrange_blocks_in_circle(all_blocks, center_of_workspace, radius)