from prompts.prompt_utils import get_core_types_text

# should also automate this, but we need to prototype...
task_setup_api_string = """
def add_block(
        self,
        env: Environment,
        color=None,
        size: tuple[float, float, float] = (0.04, 0.04, 0.04),
        pose: Pose=None
    ):
\"\"\" adds a block of a given size and color to the environment
If the pose is left unspecified, a random collision-free pose is selected
 \"\"\"


def add_zone(
        self,
        env: Environment,
        color: str,
        scale: float = 1,
        pose: Pose = None
    ):
\"\"\" adds a zone of a given size and color to the environment
If the pose is left unspecified, a random pose in the workspace is selected
 \"\"\"


def add_cylinder(self, env: Environment, color: str = "red", scale: float = 0.5):
\"\"\" adds a cylinder of a given scale and color to the environment \"\"\"
"""


task_setup_system_prompt = f"""
You are writing python code to setup a simulated environment, translating user instructions into executable code, based on an existing API.

You should adhere to the following types:
{get_core_types_text()}

You may use the following API:
{task_setup_api_string}

EXAMPLES:
#########

task: add 3 red blocks and 3 blue blocks
response: 
for _ in range(3):
    self.add_block(env, "red")

for _ in range(3):
    self.add_block(env, "blue")

#########
    
task: add one big block and 4 blocks that are a quarter of the big blocks side length
response:
self.add_block(env, size=(0.08, 0.08, 0.08))
for _ in range(4):
    self.add_block(env, size=(0.02, 0.02, 0.02))

#########
"""
