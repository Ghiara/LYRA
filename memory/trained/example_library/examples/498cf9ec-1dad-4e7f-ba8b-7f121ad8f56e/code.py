# TASK: pick up the roof base

objects_in_workspace = get_objects()
roof_base = identify_roof_base(objects_in_workspace)
if roof_base:
    pick(roof_base)
else:
    say('Roof base not found.')