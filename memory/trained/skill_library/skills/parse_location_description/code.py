def parse_location_description(description: str) -> Point3D:
    """Parses a textual description of a location within a workspace and returns the corresponding Point3D representation."""
    description = description.lower().strip()
    workspace = Workspace()
    if description == "middle":
        # Assuming the middle means the center of the workspace
        return Point3D(
            (workspace.bounds[0][0] + workspace.bounds[0][1]) / 2,
            (workspace.bounds[1][0] + workspace.bounds[1][1]) / 2,
            workspace.bounds[2][0],  # Assuming we want to work on the ground level
        )
    elif description in ["top left corner", "top-left corner"]:
        # Return top-left corner of the workspace
        return Point3D(
            workspace.back_left.x,
            workspace.back_left.y,
            workspace.bounds[2][0],  # Assuming we want to work on the ground level
        )
    elif description == "top right corner":
        # Return top-right corner of the workspace
        return Point3D(
            workspace.back_right.x,
            workspace.back_right.y,
            workspace.bounds[2][0],  # Assuming we want to work on the ground level
        )
    elif description == "bottom left corner":
        # Return bottom-left corner of the workspace
        return Point3D(
            workspace.front_left.x,
            workspace.front_left.y,
            workspace.bounds[2][0],  # Assuming we want to work on the ground level
        )
    elif description == "bottom right corner":
        # Return bottom-right corner of the workspace
        return Point3D(
            workspace.front_right.x,
            workspace.front_right.y,
            workspace.bounds[2][0],  # Assuming we want to work on the ground level
        )
    else:
        raise ValueError(f"Unknown location description: {description}")
