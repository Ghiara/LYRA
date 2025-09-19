def distance_to_workspace_edge(point: Point3D, side: str) -> float:
    """computes the distance from a point to an edge of the work"""
    if side == "front":
        return Workspace.bounds[0][1] - point.x
    elif side == "back":
        return point.x - Workspace.bounds[0][0]
    elif side == "left":
        return point.y - Workspace.bounds[1][0]
    elif side == "right":
        return Workspace.bounds[1][1] - point.y

    raise Exception(f"invalid side {side} specified")