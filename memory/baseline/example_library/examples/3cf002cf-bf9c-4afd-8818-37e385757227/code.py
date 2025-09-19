# TASK: put the red block in the middle of the workspace


objects = get_objects()
red_block = next(block for block in objects if block.objectType == "block" and block.color == "red")
middle_pose = Pose(position=Workspace.middle, rotation=Rotation.identity())
put_first_on_second(red_block, middle_pose)
