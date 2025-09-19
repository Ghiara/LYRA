import argparse
from LYRA import LYRA


parser = argparse.ArgumentParser()
# initialises an agent at a specific memory directory (in memory/)
# if no agent exists, a new one is created at the given directory with the base set of skills and examples
parser.add_argument("--memory_dir", type=str, default="baseline")

# if a task identifier is provided, this is used for task initialisation, otherwise we default to generated task setup
parser.add_argument("--task", type=str, default=None)

# debug mode means LLM responses (i.e. code) are printed to console
parser.add_argument("--debug", type=bool, default=False)

# the basic CLI allows for the user to run the baseline or trained agents on a given task
# beyond this, the user should use the interactive CLI

args = parser.parse_args()

agent = LYRA(memory_dir=args.memory_dir, debug=args.debug)

if args.task is not None:
    agent.env_agent.initialise_predefined_task(args.task)
    agent.attempt_task()
else:
    agent.run()
