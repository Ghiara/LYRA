def get_blocks_by_color(color: str = None) -> list[TaskObject]:
    """
    Retrieves all block objects in the workspace. 
    If a specific color is provided, only blocks of that color are retrieved.
    Args:
    color (str, optional): The color of the blocks to retrieve. 
                           If not specified, retrieves all blocks regardless of their color.
    Returns:
    list[TaskObject]: A list of TaskObject instances representing the blocks in the workspace.
    """
    all_objects = get_objects()
    if color:
        return [obj for obj in all_objects if obj.objectType == 'block' and obj.color == color]
    else:
        return [obj for obj in all_objects if obj.objectType == 'block']