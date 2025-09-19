from agents.model import Skill, InteractionTrace
from agents.memory import SkillManager
import matplotlib.pyplot as plt
import numpy as np
import os
import mplcursors
import pickle
import ast

from utils.cap_utils import get_skill_calls, get_defs


"""
we want to inspect both the interactions themselves, e.g. common user feedback
the number of interaction turns
number of "give-ups"

the number of reuses (by number of traces per skill)
"""


def num_traces_per_skill():
    """direct calls - this is interesting, because indirect calls (i.e. a direct call that makes another direct call)
    is irrelevant for direct llm-code-generation"""
    skill_manager = SkillManager()
    skills = skill_manager.all_skills
    skill_and_num_traces = [(skill.name, len(skill.traces)) for skill in skills]
    skill_and_num_traces.sort(key=lambda x: x[1])
    num_traces = [x[1] for x in skill_and_num_traces]

    sc = plt.scatter(np.arange(len(skills)), num_traces)
    cursor = mplcursors.cursor(sc, hover=True)
    cursor.connect(
        "add",
        lambda sel: sel.annotation.set_text(f"{skill_and_num_traces[sel.index][0]}"),
    )

    plt.show()


def num_interaction_turns_per_trial():
    traces = InteractionTrace.get_all_traces()
    num_interaction_turns = [len(trace.attempts) for trace in traces]
    num_interaction_turns.sort()
    plt.scatter(np.arange(len(traces)), num_interaction_turns)
    plt.show()


def num_successful_traces():
    traces = InteractionTrace.get_all_traces()
    return len(
        [trace for trace in traces if trace.successful_attempt is not None]
    ), len(traces)


# def update_traces_to_include_calls_not_in_defs():
#     """iterate over all successful traces, extract the called functions, and add core primitives
#     special case: call of function defined within current trace (should already be added - should also be easy to filter though...)
#     """
#     traces = InteractionTrace.get_all_traces()

#     for trace in traces:
#         if trace.successful_attempt:
#             attempt = trace.successful_attempt
#             calls = get_skill_calls(attempt.code_string)
#             defs = get_defs(attempt.code_string)
#             calls_not_in_defs = [call for call in calls if call not in defs]
#             for skill_name in calls_not_in_defs:
#                 skill = Skill.retrieve_skill_with_name(skill_name)
#                 print(skill_name)
#                 skill.trace_ids.append(attempt.id)
#                 skill.dump()
#             print("_____________________-")


if __name__ == "__main__":
    print(num_successful_traces())
