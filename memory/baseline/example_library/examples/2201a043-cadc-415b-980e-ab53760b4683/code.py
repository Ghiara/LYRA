# TASK: put one block on top of another block


objects = get_objects()
blocks = [block for block in objects if block.objectType == "block"]
pose0 = get_object_pose(blocks[0])
pose1 = get_object_pose(blocks[1])
put_first_on_second(pose0, pose1)
