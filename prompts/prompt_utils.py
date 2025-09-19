import inspect
import ast


def get_core_types_text():
    with open("utils/core_types.py", "r") as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    class_defs = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Keep only function headers and docstrings
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    subnode.body = [
                        stmt
                        for stmt in subnode.body
                        if isinstance(stmt, ast.Expr)
                        and isinstance(stmt.value, ast.Str)
                    ]
            class_defs.append(node)

    api_str = "\n\n".join([ast.unparse(node) for node in class_defs])
    return api_str


def get_core_primitives_text():
    functions = extract_functions("utils/core_primitives.py")
    api_string = "The basic environment API is as follows:\n"
    for func in functions:
        args_string = (", ").join(
            [f"{arg["name"]}: {arg["annotation"]}" for arg in func["args"]]
        )
        returns_string = f" -> {func["returns"]}" if func["returns"] is not None else ""
        func_string = (
            f"{func["name"]}({args_string}){returns_string}:\n {func["docstring"]}"
        )

        api_string += func_string + "\n" + "-" * 20 + "\n"

    return api_string


def extract_functions(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read(), filename=filepath)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            func_info = {
                "name": node.name,
                "args": [],
                "returns": ast.unparse(node.returns) if node.returns else None,
                "docstring": ast.get_docstring(node),
            }

            for arg in node.args.args:
                if arg.arg != "self":
                    func_info["args"].append(
                        {
                            "name": arg.arg,
                            "annotation": (
                                ast.unparse(arg.annotation) if arg.annotation else None
                            ),
                        }
                    )

            functions.append(func_info)

    return functions


if __name__ == "__main__":
    # print(get_core_primitives_text())
    print("___________________")
    print(get_core_types_text())
