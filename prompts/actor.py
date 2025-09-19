from prompts.prompt_utils import get_core_types_text
from agents.model.skill import Skill
from agents.model.example import TaskExample


actor_system_prompt = f"""
You write python code to control a robotic arm in a simulated environment, building on an existing API. 

You will be given:
- a task for the robotic agent to solve
- api functions you may use to solve the task
- if available, examples of codes that solve prior similar tasks

You are supposed to write flat code to solve the task, i.e. do not write any functions. 
DO NOT make any imports.

Adhere to the following basic types:
{get_core_types_text()}
"""

def actor_prompt(task, few_shot_examples: list[TaskExample], api: list[Skill]):
    return f"""
    {get_few_shot_examples_string(few_shot_examples)}
    
    {get_skill_string(api)}
    The task is: {task}

    Write flat code to solve the task.
    """

def actor_iteration_prompt(feedback, examples: list[TaskExample] = []):
    return f"""
    Rewrite the previous code to integrate the feedback: {feedback}.
    {get_few_shot_examples_string(examples)}
    Only make changes that take into account this feedback. 
    """


def get_skill_string(skills: list[Skill]):
    if len(skills) == 0:
        return ""
    return f""" 
    ---------------------------------------------------------------
    The following skills may be useful in your implementation:
    {"\n".join([skill.description for skill in skills])}
    ---------------------------------------------------------------
    """


def get_few_shot_examples_string(examples: list[TaskExample]):
    if len(examples) == 0:
        return ""
    out = "The following examples of previously solved tasks may help:\n"
    for example in examples:
        out += f"TASK: {example.task} \n CODE: {example.code} \n\n"
    return f"""
    ---------------------------------------------------------------
    {out}
    ---------------------------------------------------------------
    """


def bug_fix_prompt(code, traceback):
    return f"""
    The following code contains an error: 
    {code}
    
    The error traceback is: 
    {traceback}
    
    Please fix the error.
    """
