def check_grasp() -> bool:
    """checks whether the gripper is currently holding an object"""
    return env.ee.check_grasp()
