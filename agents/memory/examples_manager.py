import os
import shutil

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

import pickle

from agents.model import TaskExample
from agents.memory import ConfigManager

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
)


class ExamplesManager:
    """stores task examples indexed by their task string"""

    def __init__(self, MEMORY_DIR):
        self.EXAMPLE_LIBRARY_DIR = f"{MEMORY_DIR}/example_library"
        self.EXAMPLE_DIR = f"{self.EXAMPLE_LIBRARY_DIR}/examples"
        self.vector_db_dir = os.path.join(self.EXAMPLE_LIBRARY_DIR, "vector_db")

        os.makedirs(self.vector_db_dir, exist_ok=True)
        os.makedirs(self.EXAMPLE_LIBRARY_DIR, exist_ok=True)
        os.makedirs(self.EXAMPLE_DIR, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=self.vector_db_dir)
        self.vector_db = chroma_client.get_or_create_collection(
            name="examples", embedding_function=openai_ef
        )

    def add_unstored_examples_to_library(self):
        """if we manually added few-shot examples (as code pieces in to_be_added), call this function to add them to the skill library"""
        add_dir = f"{self.EXAMPLE_LIBRARY_DIR}/add"
        examples = os.listdir(add_dir)
        for example in examples:
            task_example = TaskExample.parse_code_file(f"{add_dir}/example")
            self.add_example_to_library(task_example)

    @property
    def all_examples(self) -> list[TaskExample]:
        ids = self.vector_db.get()["ids"]
        examples = [self.retrieve_task_with_id(id) for id in ids]
        examples = [example for example in examples if example is not None]
        return examples

    def add_example_to_library(self, example: TaskExample):
        task_example_description = f"{example.task}"
        self.vector_db.upsert(
            documents=[task_example_description], ids=[str(example.id)]
        )
        example.dump(self.save_dir(example.id))

    def retrieve_similar_examples(self, task, num_results=5) -> TaskExample:
        num_results = min(num_results, self.vector_db.count())
        if num_results == 0:
            return []

        results = self.vector_db.query(
            query_texts=[task],
            n_results=num_results,
        )
        ids = results["ids"][0]
        task_examples = [self.retrieve_task_with_id(id) for id in ids]
        return [example for example in task_examples if example is not None]

    def delete_example(self, example: TaskExample):
        if str(example.id) in os.listdir(self.EXAMPLE_DIR):
            print(f"deleting {example.task}")
            example_dir = os.path.join(self.EXAMPLE_DIR, str(example.id))
            shutil.rmtree(example_dir)
            self.vector_db.delete(ids=[str(example.id)])

    def delete_examples_wo_file(self):
        ids = self.vector_db.get()["ids"]
        for id in ids:
            if self.retrieve_task_with_id(id) is None:
                print("deleting")
                self.vector_db.delete([id])

    def save_dir(self, example_id):
        return f"{self.EXAMPLE_DIR}/{example_id}"

    def retrieve_task_with_id(self, id) -> TaskExample:
        pkl_path = f"{self.EXAMPLE_DIR}/{id}/example.pkl"
        if not os.path.exists(pkl_path):
            return None

        with open(pkl_path, "rb") as file:
            example = pickle.load(file)

        return example
