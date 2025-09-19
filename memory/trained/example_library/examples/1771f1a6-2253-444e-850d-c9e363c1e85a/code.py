# TASK: pick up the special block and put it in the middle of the workspace

all_blocks = get_objects()
special_block = next((block for block in all_blocks if is_special_block(block)), None)
if special_block:
    special_block_pose = get_object_pose(special_block)
    workspace_middle = parse_location_description('middle')
    put_first_on_second(special_block_pose, Pose(workspace_middle, Rotation.identity()))
else:
    say('No special block found in the workspace.')