import os, pickle, ast

from agents.model.example import TaskExample


class Skill:
    """the basic skill class, along with convenience functions"""
    def __init__(
        self,
        name,
        code,
        task_examples=[],
        is_core_primitive=False,
    ):
        self.name = name
        self.code = code
        self._task_examples = task_examples
        self.is_core_primitive = is_core_primitive

    def __str__(self):
        # return self.description
        return self.code if not self.is_core_primitive else self.description

    def __eq__(self, other) -> bool:
        if isinstance(other, Skill):
            return self.name == other.name
        return False

    @property
    def description(self):
        return f"{self.function_signature}\n{self.docstring}"

    def dump(self, dir):
        """store the skill in some readable way so we can inspect it..."""
        os.makedirs(dir, exist_ok=True)
        with open(f"{dir}/code.py", "w") as file:
            file.write(self.code)
        with open(f"{dir}/skill.pkl", "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def parse_function_string(code_string: str) -> "Skill":
        # we assume that the string only contains a single function
        # generates a partially initialised skill without a description
        tree = ast.parse(code_string)
        func_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if len(func_defs) != 1:
            print(
                f"not exactly one ({len(func_defs)} - {func_defs}) function defined in code string:\n{code_string}"
            )

        func = func_defs[0]
        func_name = func.name
        func_source = ast.get_source_segment(code_string, func)

        return Skill(func_name, func_source)

    @property
    def function_signature(self):
        lines = self.code.splitlines()
        signature = ""

        for line in lines:
            line = line.strip()
            if line.startswith("def "):  # Start capturing from function definition
                signature += line
            elif signature:  # If already capturing, continue appending
                signature += " " + line.strip()
            if '"""' in line:  # Stop once the docstring starts
                break

        return signature.split('"""', 1)[0]  # Return everything up to the colon

    @property
    def docstring(self):
        tree = ast.parse(self.code)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):  # Ensure it's a function definition
                return ast.get_docstring(node)
        return None

    def add_task_example(self, task_example: TaskExample):
        if task_example.id not in self._task_examples:
            self._task_examples.append(str(task_example.id))

    def remove_task_example(self, task_example: TaskExample):
        self._task_examples.remove(str(task_example.id))

    @staticmethod
    def print_skills(skills: list["Skill"]):
        print("\n".join([skill.name for skill in skills]))
