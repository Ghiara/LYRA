# TASK: build a single layer of a jenga tower by aligning three rectangular blocks such that their longer sides are touching each other

blocks = get_blocks_by_color()
base_pose = Pose(Point3D(0.3, 0.0, 0.05), Rotation.identity())
spacing = 0.005
build_jenga_layer(blocks, base_pose, spacing)