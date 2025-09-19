def identify_roof_tiles(objects: list[TaskObject]) -> list[TaskObject]:
    """Identifies and returns a list of TaskObjects that are categorized as roof tiles from a given list of objects.
    A roof tile is characterized by having one dimension smaller than 0.02 and being red in color.
    Args:
    - objects (list[TaskObject]): A list of TaskObjects to be analyzed for identification of roof tiles.
    Returns:
    - list[TaskObject]: A list of TaskObjects that are identified as roof tiles, based on the specified characteristics.
    """
    roof_tiles = []

    for obj in objects:
        if obj.color.lower() == "red" and any(dim < 0.02 for dim in obj.size):
            roof_tiles.append(obj)
    return roof_tiles
