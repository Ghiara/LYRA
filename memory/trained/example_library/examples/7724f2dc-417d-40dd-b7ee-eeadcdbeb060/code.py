# TASK: remove all blocks from the zone

workspace = Workspace()
all_blocks = get_objects()
zones = get_zones()
if zones:
    target_zone = zones[0]
    target_zone_bbox = get_bbox(target_zone)
    clear_blocks_from_area(all_blocks, target_zone_bbox)
else:
    say('No zones found in the workspace!')