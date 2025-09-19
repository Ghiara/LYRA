# TASK: arrange the blocks in a circle around the center of the workspace

from scipy.spatial.transform import Rotation
import numpy as np
all_blocks = get_objects()
workspace = Workspace()
center_of_workspace = Point3D((workspace.bounds[0][0] + workspace.bounds[0][1]) / 2, (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2, 0)
radius = 0.2
arrange_blocks_in_circle(all_blocks, center_of_workspace, radius)