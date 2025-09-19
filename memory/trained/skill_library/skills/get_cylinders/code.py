def get_cylinders() -> list[TaskObject]:
    """Retrieve all cylinder TaskObjects available in the workspace.
    Returns:
        list[TaskObject]: A list of TaskObject instances representing the cylinders in the workspace.
    """
    objects = get_objects()
    cylinders = [obj for obj in objects if obj.objectType == 'cylinder']
    return cylinders