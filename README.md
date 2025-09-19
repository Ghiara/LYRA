# Growing with Your Embodied Agent: A Human-in-the-Loop Lifelong Code Generation Framework for Long-Horizon Manipulation Skills

[![Python 3.6+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3127/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-orange.svg)](https://www.apache.org/licenses/LICENSE-2.0)

Official implementation of **LYRA**: A **L**ifelong learning code s**Y**nthesis framework with human-in-the-loop for **R**obotic long-horizon skill **A**cquisition

- [LYRA](#cap-options-todo)
  - [1. Introduction](#1-introduction)
  - [2. Installation](#2-installation)
  - [3. Overview](#3-overview)
  - [4. Run the code with interaction](#4-run-the-code-with-interaction)
    - [4.1 Interact in the terminal](#41-interact-in-the-terminal)
    - [4.2 Test pre-trained agent](#42-test-pre-trained-agent)
    - [4.3 Teach your robot](#43-teach-your-robot)
  - [Repository Structure](#repository-structure)
  - [Known Weaknesses](#known-weaknesses)
  - [Acknowledgements](#acknowledgements)
  - [clis](#clis)

## 1. Abstract

Large language models (LLMs) have been widely applied in robotic manipulation for their commonsense knowledge and semantic understanding. 
Prior methods use LLMs for task decomposition with pre-trained policies or end-to-end pretraining, but they struggle with perturbations, data sparsity, and high computational costs. 
More recently, LLM-based **code generation** has shown promise by directly translating human instructions into executable code, yet current methods remain noisy, limited by fixed primitives and context windows, and ineffective for long-horizon tasks. 
While corrections have been explored, improper representation restricts generalization and causes catastrophic forgetting, highlighting the need to learn reusable **skills**. 
We propose a **human-in-the-loop** framework that encodes corrections into skills, supported by external memory and **Retrieval-Augmented Generation** (RAG) with a hint mechanism for dynamic reuse. 
Experiments across Ravens, Franka Kitchen, and MetaWorld, as well as real-world deployment on a Franka FR3, demonstrate that our framework achieves a 0.93 success rate (up to 27\% higher than baselines) and a 42\% efficiency improvement in correction rounds. 
To the best of our knowledge, our framework is the first to robustly solve the extremely long-horizon task ``build a house``.

## 2. Installation

- 2.1 Clone the repository:

```bash
git clone https://github.com/Ghiara/LYRA.git
```

Create the conda environment with Python 3.12 (we recommend using mamba, creating the env with conda failed for us).

```bash
cd LYRA
mamba env create -n lyra -f environment.yml

conda activate lyra
```

- 2.2 Add an OpenAI API key as a python environment variable to run experiments.
For example, you can add the following line to .bashrc, .zshrc, or .bash_profile.

```bash
export OPENAI_API_KEY=<your_key_here>
```


## 3. Overview

A [**skill**](agents/model/skill.py) is a python function, which the agent calls when writing code to solve a [**task**](task/task_and_store.py). An [**example**](agents/model/example.py) is a pair of a natural language instruction and the python code (which calls different skills) used to successfully respond to the instruction. When presented with a new instruction, the agent is more likely to be able to respond to it correctly if it has examples of similar instructions. A skill represents the part of the behaviour which the agent should not vary in downstream tasks, whereas the example code demonstrates _how_ and _when_ to call a skill (i.e. how to parameterise it, how to use its returns, what other functions are often called around it, ...).

As the number of skills and examples (i.e. number of behaviours the robot is capable of) grows, it becomes less feasible to put them into a single fixed prompt, necessitating some form of instruction-specific retrieval of skills and examples. Even when they all fit into a prompt, too many skills and examples crowd out the useful information.

Core to our approach is an interactive skill _teaching_ mechanism, by which we first describe to the agent the skill we want it to learn, and then provide tasks which test whether this skill _does what we want it to do_, for each of which we may provide corrective feedback to help it get there: "If the skill can be used to successfully solve all these tasks, then we've successfully learned this skill." In this way, we subsume many of the tasks of the RL engineer: the user interactively determines what the agent is capable of, proposes _reasonably_ difficult tasks, and provides feedback to alter the agents behaviour. The goal was to create a natural language UI for _teaching_ robots new behaviours, ultimately for Teleoperation or End-user programming.

## 4. Run the code with interactive Terminal

### 4.1 Interact in the terminal

We provide a simple CLI to run the code, for example you can run the agent with inital database named ``baseline``:

```bash
python main.py --memory_dir "baseline"
# [1] Learn a new skill || [2] Attempt a task || [3] Run past example

# After select [2] in the terminal:
    [1] Generate new task
    [2] Use stored environment state
    [3] Use predefined task
    # After select [3] + typing: stack-blocks
    # The LLM agent will infer the task and execute the code
    # You will see how the agent performs the task from real-time rendering window
    # After task execution accomplished, You can select:
        [1] Success
        [2] Give up
        [3] Re-run (old code)
        [4] Try again (new code)
        [5] Apply hint
        [6] Feedback & iterate 
```

> [!NOTE]
> This will interactively take you through _teaching_ the agent. `--memory_dir` determines the directory in [memory](memory) which contains the agents memory, and as such determines what the agent is capable of. 
You can use the [baseline](memory/baseline/) or [trained](memory/trained) (larger library of skills and examples) agents, or you can initialise a new one by providing the name of the directory.



### 4.2 (optional) Test agent with pre-trained skill library
Alternatively, you can test the pretrained agent capabilities on some [predefined tasks](task/__init__.py) by running:

```bash
python main.py --memory_dir "trained" --task "construct-smiley-face"
```

All CLIs for agent with trained skill database are listed here:
```bash
python main.py --memory_dir "trained" --task "place-green-next-to-yellow"
python main.py --memory_dir "trained" --task "build-house"
python main.py --memory_dir "trained" --task "place-blocks-diagonally"
python main.py --memory_dir "trained" --task "stack-blocks"
python main.py --memory_dir "trained" --task "stack-blocks-big-to-small"
python main.py --memory_dir "trained" --task "stack-blocks-induce-failure"
python main.py --memory_dir "trained" --task "build-cube"
python main.py --memory_dir "trained" --task "build-block-pyramid"
python main.py --memory_dir "trained" --task "build-jenga-layer"
python main.py --memory_dir "trained" --task "build-jenga-tower"
python main.py --memory_dir "trained" --task "build-jenga-tower-long-description"
python main.py --memory_dir "trained" --task "construct-smiley-face"
python main.py --memory_dir "trained" --task "construct-smiley-face-long-description"
python main.py --memory_dir "trained" --task "build-zigzag-tower"
python main.py --memory_dir "trained" --task "build-zigzag-tower-long-description"
python main.py --memory_dir "trained" --task "place-blue-blocks-around-red-block"
```

>[!NOTE]
> A task provides the initial environment setup and the description of what you want the agent to do. Determining whether or not the agent was successful is left up to the user. [task/**init**.py](task/__init__.py) lists the valid task identifiers, and you can find the tasks (and add new ones) in [task/tasks.py](task/tasks.py). You can also generate one from a prompt (e.g. "6 big red blocks and 2 small green ones") in the interactive CLI.


### 4.3 Example Tutorial: Teach your robot

1. A good example to get an understanding of skill learning is to teach the agent to build a "zigzag tower". First, see what a zigzag tower is by running:

```bash
python main.py --memory_dir "trained" --task "build-zigzag-tower"
```

2. Then see what the untrained agent does in response to the same instruction.

```bash
python main.py --memory_dir "baseline" --task "build-zigzag-tower"
```

3. Now enter the interactive CLI with the untrained agent, so you can teach it how to do it right.

```bash
python main.py --memory_dir "baseline"
```

4. First you need to declare that you want to "learn a skill". Then you provide a description of the skill you want to learn (which generates a python function header, i.e. the skill spec). Then you set up the task using the identifier `"build-zigzag-tower"`, and then you provide feedback on what the agent is doing until it looks the way you want it to look (which can be whatever you want). Once you have done this, you can test the agent on the same task, to observe the updated behaviour.

```bash
python main.py --memory_dir "baseline" --task "build-zigzag-tower" --debug True
```

5. You could now learn another skill on top of this one, for example building a "zigzag wall", by placing multiple zigzag towers next to one another. The point is that the agent now performs this behaviour the way you expect it to, doesn't lose this ability as you teach it more behaviours (as it might with handcrafted prompts), and that this can be achieved interactively.

>[!NOTE]
> [data](data) contains some examples of learned behaviours. We included some [videos of failure modes on the simple task of stacking blocks](data/stack_blocks) with the baseline agent, which you can reproduce by running
>```bash
>python main.py --memory_dir "baseline" --task "stack-blocks"
>python main.py --memory_dir "baseline" --task "stack-blocks-induce-failure"
>```
>Sometimes it gets it right too, and if we altered the prompt to give it more information from the outset this would solve the problem as well. Run it a few times to get a sense of how noisy LLM code generation can be. Then run the same tasks with the trained agent to see the corrected (consistent) behaviour. The point is that you can get from "baseline" to "trained" purely via natural language interaction, and interactive task solving.
>
> You can run examples in the simulator by selecting "Run past examples" in the interactive CLI. Put in a task, and it will retrieve the most similar experiences the agent has stored, which can then be rolled out in the environment. (DISCLAIMER: some of these may not run properly, for a variety of reasons. If you generate new ones, this will work properly.) This is useful for inspecting the agents memory.




## Repository Structure

- [agents] contains the LLM agent modules for [generating robot policy code](agents/action), for [setting up the environment](agents/environment), and for [skill parsing](agents/skill) (i.e. mapping natural language skill descriptions to python function headers). [agents/memory](agents/memory) contains all the memory related modules, which rely on [ChromaDB](https://www.trychroma.com), used for managing the skill and example libraries (as well as storing environment configs). [agents/model](agents/model) contains the relevant data classes (Skill, TaskExample, EnvironmentConfiguration, and InteractionTrace), for pickling and basic convenience functions.

- [environments](environments) contains all the environment-related code. This could be simplified substantially, or ideally replaced with something better. This repository builds on the [Cliport](https://github.com/cliport/cliport) repo, primarily for the accompanying Ravens benchmark, though there is a lot of unused code leftover from it (mostly in this [environments](environments) folder and [utils/general_utils]([utils/general_utils])).

- [memory](memory) contains the memories of agents trained based on our approach, storing skill and example libraries, as well as interaction traces. Each subfolder (e.g. [memory/baseline]) corresponds with a single agent. You can inspect the skill libraries (skills are saved in a readable manner) and manually delete, add or edit skills. This might be useful if you want to simply test the agents abilities with a larger number of core primitives, or to remove mistakenly saved skills. Examples are also readable, though they are a bit harder to inspect since we're not giving them meaningful names right now.

- [data](data) contains some examples of learned behaviours.

- [prompts](prompts) contains all the prompts we used, modelled as python fstrings.

- [scripts](scripts) contains some attempts at interpreting the agent memories, as well as an attempt at automatically testing whether an environment configuration is equal to another one (though this is more difficult than you might think – would also require some "softer" semantic approach, e.g. based on a VLM-verifier).

- [utils](utils) contains a number of necessary supporting functions.

- The main agent code is in [LYRA.py](LYRA.py), and [main.py](main.py) is the entrypoint for the app.



## Acknowledgements

- [Cliport](https://github.com/cliport/cliport) – for the basic Ravens benchmark setup
- [Code-as-Policies](https://github.com/google-research/google-research/tree/master/code_as_policies) - code-generation for robotics
- [VOYAGER](https://github.com/MineDojo/Voyager), [Expel](https://github.com/LeapLabTHU/ExpeL), [DROC](https://github.com/Stanford-ILIAD/droc) - provided the inspiration for our code base, and the concept of LLM-Agent -_learning_ by reading and writing to memory based on experience
