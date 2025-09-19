def get_zones() -> list[TaskObject]:
    """Retrieve all zone TaskObjects available in the workspace.
    Returns:
        list[TaskObject]: A list of TaskObjects representing the zones.
    """
    objects = get_objects()
    zones = [obj for obj in objects if obj.objectType == 'zone']
    return zones