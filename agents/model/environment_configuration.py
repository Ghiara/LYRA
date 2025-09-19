import numpy as np
import pickle
import uuid

from utils.core_types import TaskObject, Pose, Rotation, Point3D


class EnvironmentConfiguration:
    """stores a list of objects and their poses, s.t. we can reset to environment configurations
    also stores image, s.t. we can choose configs based on images or use image-based retrieval...
    we attempted to implement config equality, but this isn't easy to do in some meaningful way, even if we just consider blocks
    """

    def __init__(
        self,
        objects_with_poses: list[TaskObject, Pose] = [],
        image=None,
        description=None,
    ):
        self.id = uuid.uuid4()
        self.objects_with_poses = objects_with_poses
        self.image = image
        self.description = description

    @classmethod
    def from_path(cls, path) -> "EnvironmentConfiguration":
        with open(path, "rb") as file:
            loaded_config = pickle.load(file)
        return loaded_config

    def dump(self, path):
        with open(path, "wb") as file:
            pickle.dump(self, file)

    def __str__(self):
        ret = ""
        for obj, pose in self.objects_with_poses:
            ret += f"{obj.description}: {pose.position} {pose.rotation} \n"
        return ret

    def __eq__(self, other):
        """we are only working with blocks - we need to account for structural equality, not ids
        means we need to check if in every position where there is a block in one config, there is *also* one in the other config
        """
        if isinstance(other, EnvironmentConfiguration):
            if len(self.objects_with_poses) != len(other.objects_with_poses):
                return False

            """brute-forcey check, but should be fine on runtime... maybe with a 100 objects it'll start getting slow
            would be slightly faster if we remove previously matched blocks from other_objects as we go"""
            for object, pose in self.objects_with_poses:
                found_match = False
                for other_object, otherPose in other.objects_with_poses:
                    symmetry_type = EnvironmentConfiguration.get_symmetry_type(
                        object.size
                    )
                    other_symmetry_type = EnvironmentConfiguration.get_symmetry_type(
                        object.size
                    )
                    if symmetry_type != other_symmetry_type:
                        continue
                    # if EnvironmentConfiguration.is_pose_equal(
                    #     pose, otherPose, symmetry_type
                    # ):
                    if self.is_pose_equal(
                        pose, otherPose, symmetry_type
                    ):  # if self.is_pos_equal(pose.position, otherPose.position):
                        found_match = True
                        break
                if not found_match:
                    return False
            return True
        return False

    def is_pose_equal(self, poseA: Pose, poseB: Pose, symmetry_type):
        return self.is_pos_equal(poseA.position, poseB.position) and self.is_rot_equal(
            poseA.rotation, poseB.rotation, symmetry_type
        )

    def is_pos_equal(self, posA: Point3D, posB: Point3D):
        return np.allclose(posA.np_vec, posB.np_vec, atol=0.01)

    def is_rot_equal(self, rotA: Rotation, rotB: Rotation, symmetry_type):
        canonRotA = EnvironmentConfiguration.canonicalize_rotation(
            rotA, symmetry_type=symmetry_type
        )
        canonRotB = EnvironmentConfiguration.canonicalize_rotation(
            rotB, symmetry_type=symmetry_type
        )

        is_equal = np.allclose(canonRotA, canonRotB, atol=0.01)
        return is_equal

    @staticmethod
    def get_symmetry_type(size: tuple[float, float, float]):
        if np.isclose(size[0], size[1]) and np.isclose(size[1], size[2]):
            return "cube"
        elif (
            np.isclose(size[0], size[1])
            or np.isclose(size[0], size[2])
            or np.isclose(size[1], size[2])
        ):
            return "square_prism"
        else:
            return "rect_prism_diff"

    @staticmethod
    def get_valid_symmetries(symmetry_type):
        identity = np.eye(3)

        if symmetry_type == "cube":
            # For a cube, generate all 24 unique rotations.
            rotations = []
            seen = set()
            for a in [0, 90, 180, 270]:
                for b in [0, 90, 180, 270]:
                    for c in [0, 90, 180, 270]:
                        rot = Rotation.from_euler("xyz", [a, b, c], degrees=True)
                        mat = rot.as_matrix()
                        # Round the entries to avoid floating point issues
                        key = tuple(np.round(mat.flatten(), 5))
                        if key not in seen:
                            seen.add(key)
                            rotations.append(mat)
            return rotations

        elif symmetry_type == "square_prism":
            # For a right square prism (dimensions A x A x B),
            # the symmetry group is D4 (8 rotations).
            rots = []
            for angle in [0, 90, 180, 270]:
                r_z = Rotation.from_euler("z", angle, degrees=True).as_matrix()
                rots.append(r_z)
                # Combine a 180° flip about the x-axis with the z rotation.
                flip = Rotation.from_euler("x", 180, degrees=True).as_matrix()
                rots.append(flip @ r_z)
            return rots

        elif symmetry_type == "rect_prism_diff":
            # For a rectangular prism with three different side lengths,
            # only 180° rotations about each principal axis map the object onto itself.
            return [
                identity,
                Rotation.from_euler("x", 180, degrees=True).as_matrix(),
                Rotation.from_euler("y", 180, degrees=True).as_matrix(),
                Rotation.from_euler("z", 180, degrees=True).as_matrix(),
            ]

        else:
            # No symmetry provided, so only the identity.
            return [identity]

    @staticmethod
    def canonicalize_rotation(rotation: Rotation, symmetry_type="cube") -> Rotation:
        """Finds the canonical quaternion under the given symmetry type."""
        q = rotation.as_quat()
        q = np.array(q) / np.linalg.norm(q)  # Normalize quaternion

        # Generate all valid equivalent rotations
        valid_rotations = EnvironmentConfiguration.get_valid_symmetries(symmetry_type)

        # Convert quaternion to matrix
        q_matrix = Rotation.from_quat(q).as_matrix()

        # Apply each valid transformation and find the lexicographically smallest one
        q_variants = [
            Rotation.from_matrix(rot @ q_matrix).as_quat() for rot in valid_rotations
        ]

        return min(q_variants, key=lambda quat: tuple(np.abs(quat)))
