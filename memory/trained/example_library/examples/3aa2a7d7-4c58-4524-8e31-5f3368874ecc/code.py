# TASK: build a single layer of a jenga tower in the zone

blocks = get_blocks_by_color()
zones = get_zones()
zone_pose = get_object_pose(zones[0])
spacing = 0.005
build_jenga_layer(blocks, zone_pose, spacing)