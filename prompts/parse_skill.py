from prompts.prompt_utils import get_core_types_text
from agents.model import Skill
from pydantic import BaseModel


generate_function_header_system_prompt = f"""
We are working in the context of controlling a robotic arm with python code. 
The user proposes a certain skill they would like the robot to learn.
To enable this, you are supposed to translate this skill into a python function, 
i.e. choose a clear, descriptive name for the function, choose appropriate arguments, and write a clear, descriptive docstring.

For example:
USER: "place one block on top of the other"
RESPONSE:
def place_block_on_other_block(block: TaskObject, otherBlock: TaskObject):
    \"\"\" Places one block on top of the other block  \"\"\"
    pass
    
Do not try to implement the function yet, that happens later.
    
You should adhere to the following types:
{get_core_types_text()}

The functions don't need Workspace as an argument, since there is only one.
"""


def generate_skill_prompt(prompt, similar_skills: list[Skill]):
    return f"""
    you may use the following function headers as examples of what you are trying to generate:
    {"\n".join([skill.description for skill in similar_skills])}
    --------------------------------------------------
    write a function header for the prompt: {prompt}.
    """


def refine_function_header_prompt(function_code, refinement):
    return f"""
    Your role is to refine an existing python function, for example by adding a function argument or changing the name.
    If the function is implemented (i.e. not just "pass"), you should also alter the implementation accordingly, making as little changes and assumptions as possible.
    Revise the following python function according to the user instructions:
    {function_code}
    Refinement prompt:
    {refinement}
    Do not make any assumptions.
    """


## ----------------------------------
## used to parse hints


class ParsedList(BaseModel):
    parsed_list: list[str]


def parse_hint_to_list_prompt(hint):
    return f"""
    The user provided a list of tasks that are similar to the one you are currently trying to solve, in a single string.
    Retrieve each of the task descriptions from this string, and return them as a list.
    This is the string: {hint}
    """
