from utils.llm_utils import print_code
from agents.model import TaskExample

BOLD = "\033[1m"
RESET = "\033[0m"


def choice_from_input_items(
    items: list[str],
    prompt: str = "Please select an option:",
    is_vertical: bool = True,
    allow_none=False,
) -> int:
    """
    Prompt the user to select an option from a list of items.

    Args:
        items (list[str]): A list of items to choose from.
        prompt (str): The prompt message to display to the user.
        default (int): The default index to select if the user presses Enter.

    Returns:
        int: The index of the selected item.
    """
    print(prompt)
    print("\n")
    if is_vertical:
        for i, item in enumerate(items):
            print(f"[{i + 1}] {item}")
    else:
        print(f" || ".join([f"[{i + 1}] {item}" for i, item in enumerate(items)]))

    print("\n")

    while True:
        try:
            choice = input(
                f"Select an option by typing the number {"or 'none'" if allow_none else ""} \n{user_response_arrow()}"
            )
            if choice == "none" and allow_none:
                return None
            choice = int(choice)
            if choice <= 0 or choice > len(items):
                raise ValueError
            return choice
        except ValueError:
            print(
                "Invalid input. Please enter a valid number corresponding to your choice."
            )


def print_list(items: list[str], title: str = "List of Items"):
    """Prints a list of items in a formatted way"""
    print(f"\n{title}\n")
    print("\n".join([f"{i + 1}. {item}" for i, item in enumerate(items)]))
    print("\n")


def system_cli_message(
    message: str,
):
    """Adds standardised formatting to a system output message (i.e. step update)"""

    line = "=" * 80
    print(f"\n{line}\n{message.upper()}\n{line}\n")


def simple_user_prompt(question: str) -> str:
    """adds standardised formatting to a question"""
    answer = input(f"\n{question}\n{user_response_arrow()}")
    return answer


def debug_message(message: str, title: str):
    """Prints a debug message with a title"""
    print(f"\n{BOLD}{title}{RESET}\n")
    print_code(message)


def print_examples(examples: list[TaskExample]):
    print("-" * 40)
    for example in examples:
        print(f"Task: {example.task}")
        print_code(example.code)
        print("\n")


def user_response_arrow():
    """returns an arrow to indicate user should input"""
    return "====> "


if __name__ == "__main__":
    system_cli_message("This is a test message")

    choice = choice_from_input_items(
        ["Option 1", "Option 2", "Option 3"],
        prompt="Please select an option:",
    )
