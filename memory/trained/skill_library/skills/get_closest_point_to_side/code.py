def get_closest_point_to_side(points: list[Point3D], side: str) -> Point3D:
    """gets the point from a list of points that is closest to the given edge of the workspace"""
    min_point = points[0]
    min_dist_to_side = distance_to_workspace_edge(points[0], side)
    for point in points[1:]:
        dist = distance_to_workspace_edge(point, side)
        if dist < min_dist_to_side:
            min_point = point
            min_dist_to_side = dist

    return min_point