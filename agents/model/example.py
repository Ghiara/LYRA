import uuid, os, pickle, ast, re
from agents.model.environment_configuration import EnvironmentConfiguration
from utils.llm_utils import print_code


class TaskExample:
    """stores the (task-string, successful-code) pairs, as well as initial and final config,
    and optionally skill-code, if the example was generated while learning a skill"""

    def __init__(
        self,
        task: str,
        code: str,
        initial_config: EnvironmentConfiguration = None,
        final_config: EnvironmentConfiguration = None,
        skill_code: str = None,
    ):
        self.id = uuid.uuid4()
        self.task = task
        # code should only be non-function, i.e. flat code
        self.code = code
        self.initial_config = initial_config
        self.final_config = final_config

        # optionally also attach the code for the function that was learned with this task
        self.skill_code = skill_code

    def dump(self, dir):
        os.makedirs(dir, exist_ok=True)
        with open(f"{dir}/code.py", "w") as file:
            file.write(f"# TASK: {self.task}\n\n{self.code}")
        with open(f"{dir}/example.pkl", "wb") as file:
            pickle.dump(self, file)

    def get_skill_headers(self):
        tree = ast.parse(self.code)
        func_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        funcs = [ast.get_source_segment(self.code, func) for func in func_defs]
        return funcs

    @staticmethod
    def parse_code_file(file):
        with open(file, "r") as file:
            code = file.read()

        match = re.search(r"#TASK:\s*(.*?)(?=\n\S|$)", code, re.DOTALL)

        if match:
            task_text = match.group(1).strip()
            rest_of_file = code[: match.start()] + code[match.end() :]
        else:
            task_text = None
            rest_of_file = code

        example = TaskExample(task=task_text, code=rest_of_file)

        return example


if __name__ == "__main__":
    example = TaskExample.parse_code_file("example.py")
    example.dump("example")
    print(example.get_skill_headers())
