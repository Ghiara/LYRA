def compute_bbox(pose: Pose, size: tuple[float, float, float]) -> AABBBoundingBox:
    """
    compute the axis-aligned bounding box of an object given its pose and size
    """
    w, h, d = size

    corners = np.array(
        [
            [dx, dy, dz]
            for dx in [-w / 2, w / 2]
            for dy in [-h / 2, h / 2]
            for dz in [-d / 2, d / 2]
        ]
    )

    rotated_corners = pose.rotation.apply(corners) + pose.position.np_vec

    aabb_min = np.min(rotated_corners, axis=0)
    aabb_max = np.max(rotated_corners, axis=0)

    return AABBBoundingBox(Point3D.from_xyz(aabb_min), Point3D.from_xyz(aabb_max))
