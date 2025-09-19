import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import pickle
from agents.model import TaskExample, EnvironmentConfiguration

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
)


class ConfigManager:
    """stores configs for retrieval for initialisation of downstream tasks"""

    def __init__(self):
        self.CONFIG_LIBRARY_DIR = "task/config_library"
        self.vector_db_dir = os.path.join(self.CONFIG_LIBRARY_DIR, "vector_db")
        self.configs_dir = os.path.join(self.CONFIG_LIBRARY_DIR, "configs")
        os.makedirs(self.configs_dir, exist_ok=True)
        os.makedirs(self.vector_db_dir, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=self.vector_db_dir)
        self.vector_db = chroma_client.get_or_create_collection(
            name="configs", embedding_function=openai_ef
        )

    def store_final_config(self, task_example: TaskExample):
        """store in vector db for retrieval and write to config list"""
        description = self.generate_final_config_description(task_example.task)
        config = task_example.final_config
        config.description = description

        self.vector_db.upsert(
            documents=[description],
            ids=[str(config.id)],
        )

        with open(f"{self.CONFIG_LIBRARY_DIR}/configs.txt", "a") as file:
            file.write(f"{description}\n")

        config.dump(f"{self.configs_dir}/{config.id}.pkl")

    def retrieve_configs(
        self, config_prompt, num_results=5
    ) -> list[EnvironmentConfiguration]:
        num_results = min(num_results, self.vector_db.count())
        if num_results == 0:
            return []

        results = self.vector_db.query(
            query_texts=[config_prompt],
            n_results=num_results,
        )
        ids = results["ids"][0]
        configs = [self.retrieve_config_with_id(id) for id in ids]
        return [config for config in configs if config is not None]

    def generate_final_config_description(self, task):
        """e.g. build a jenga tower"""
        # from prompts.config import generate_config_description

        # messages = [{"role": "user", "content": generate_config_description(task)}]
        # description = query_llm(messages)
        # THIS DIDN'T WORK AT ALL - just ask the user...
        description = input("give a description of the config to be stored...")
        return description

    def retrieve_config_with_id(self, id) -> EnvironmentConfiguration:
        if f"{id}.pkl" not in os.listdir(self.configs_dir):
            return None

        with open(f"{self.configs_dir}/{id}.pkl", "rb") as file:
            config = pickle.load(file)

        return config
