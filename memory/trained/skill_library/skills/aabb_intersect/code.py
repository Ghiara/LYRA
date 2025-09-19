def aabb_intersect(a: AABBBoundingBox, b: AABBBoundingBox) -> bool:
    """
    Check if two 3D AABBs intersect.
    """
    x_min1, y_min1, z_min1 = a.minPoint.np_vec
    x_max1, y_max1, z_max1 = a.maxPoint.np_vec
    x_min2, y_min2, z_min2 = b.minPoint.np_vec
    x_max2, y_max2, z_max2 = b.maxPoint.np_vec

    return not (
        x_max1 <= x_min2 or x_max2 <= x_min1 or y_max1 <= y_min2 or y_max2 <= y_min1
    )
