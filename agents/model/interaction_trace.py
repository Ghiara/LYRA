"""
no need to store all the intermediate code strings right?
but the feedback probably... the number of correction rounds
whether in the end it was successful or not...
which skills were ultimately used...
"""

import os
import uuid
import pickle
from datetime import datetime

from agents.model.environment_configuration import EnvironmentConfiguration
from agents.model.example import TaskExample
from dataclasses import dataclass


class InteractionTrace:
    """
    we store this for data analysis purposes (e.g. number of corrections)
    initially we wanted to use this for a less deliberate skill acquisition process (e.g. https://arxiv.org/pdf/2310.08992)
    this was largely unsuccessful, but might still be useful eventually
    """

    def __init__(self, task, initial_config: EnvironmentConfiguration):
        self.id = uuid.uuid4()
        self.task = task
        self.initial_config = initial_config
        self.feedbacks = []
        self.timestamp = datetime.now().strftime("%m-%d-%H-%M-%S")
        self.example = None

    @property
    def is_success(self):
        return self.example is not None

    def add_feedback_round(self, feedback):
        self.feedbacks.append(feedback)

    def success(self, example: TaskExample) -> str:
        self.example = example

    def dump(self, dir):
        with open(f"{dir}/{self.id}.pkl", "wb") as file:
            pickle.dump(self, file)
