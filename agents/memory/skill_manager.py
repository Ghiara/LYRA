import os
import shutil

import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from utils.llm_utils import query_llm
from utils.cap_utils import get_calls, get_defs

import ast
import pickle
import inspect

from agents.model import Skill, TaskExample, InteractionTrace, EnvironmentConfiguration

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
)


class SkillManager:
    """stores skills by their function header (i.e. function signature + docstring)
    alternatively we could have generated descriptions of the functions and retrieved them by that,
    but the docstring should contain the necessary information

    skills can also be added/edited manually in the python files in the corresponding skill directory,
    since retrieval only gets the skill IDs, and these are then mapped to the stored code strings
    """

    def __init__(self, MEMORY_DIR):
        self.SKILL_LIBRARY_DIR = f"{MEMORY_DIR}/skill_library/"
        self.SKILL_DIR = f"{self.SKILL_LIBRARY_DIR}/skills"
        self.vector_db_dir = os.path.join(self.SKILL_LIBRARY_DIR, "vector_db")

        os.makedirs(self.vector_db_dir, exist_ok=True)
        os.makedirs(self.SKILL_LIBRARY_DIR, exist_ok=True)
        os.makedirs(self.SKILL_DIR, exist_ok=True)

        chroma_client = chromadb.PersistentClient(path=self.vector_db_dir)
        self.vector_db = chroma_client.get_or_create_collection(
            name="skill_library", embedding_function=openai_ef
        )

        self.remove_deleted_skills()
        self.add_manually_added_skills()

    def remove_deleted_skills(self):
        all_skills = os.listdir(self.SKILL_DIR)
        stored_skills = self.vector_db.get()["ids"]
        # check if there are any deleted skills, and if so, remove them from the vector db
        for skill_name in stored_skills:
            if skill_name not in all_skills:
                print(f"deleting {skill_name}")
                self.vector_db.delete(ids=[skill_name])

    def add_manually_added_skills(self):
        all_skills = os.listdir(self.SKILL_DIR)
        stored_skills = self.vector_db.get()["ids"]
        # check if there are any skills which have not been added to the vector db and if so add them (to enable manual adding of skills)
        for skill_name in all_skills:
            if skill_name not in stored_skills and not skill_name.startswith("."):
                with open(f"{self.SKILL_DIR}/{skill_name}/code.py", "r") as file:
                    code = file.read()
                skill = Skill.parse_function_string(code)
                self.add_skill_to_library(skill)

    def add_core_primitives_to_library(self):
        # only for retrieval purposes... functions are still actually called from core_primitives module
        from utils import core_primitives

        functions = inspect.getmembers(core_primitives, inspect.isfunction)
        for name, func in functions:
            if name not in core_primitives.__all__:
                continue

            path = f"{self.SKILL_DIR}/{name}"
            # delete if primitive was previously stored already...
            if name in os.listdir(self.SKILL_DIR):
                print("was in there already")
                self.vector_db.delete(ids=[name])
                shutil.rmtree(path)
            skill = Skill(
                name=name,
                code=inspect.getsource(func),
                is_core_primitive=True,
            )
            self.add_skill_to_library(skill)

    @property
    def all_skills(self) -> list[Skill]:
        all_keys = self.vector_db.get()["ids"]
        skills = [self.retrieve_skill_with_name(name) for name in all_keys]
        return skills

    @property
    def num_skills(self):
        return self.vector_db.count()

    def save_dir(self, skill_name):
        """returns the directory at which a skill with a given name is saved"""
        return f"{self.SKILL_DIR}/{skill_name}"

    def retrieve_skill_with_name(self, name) -> "Skill":
        # with open(f"{SKILL_DIR}/{name}/code.py", "r") as file:
        #     skill_code = file.read()
        with open(f"{self.SKILL_DIR}/{name}/skill.pkl", "rb") as file:
            skill = pickle.load(file)
        with open(f"{self.SKILL_DIR}/{name}/code.py", "r") as file:
            skill.code = file.read()

        return skill

    def delete_skill(self, name: str):
        if name in os.listdir(self.SKILL_DIR):
            print(f"deleting {name}")
            skill_dir = os.path.join(self.SKILL_DIR, name)
            shutil.rmtree(skill_dir)
            self.vector_db.delete(ids=[name])

    def add_skill_to_library(self, skill: Skill):
        """adds the skill to the vector database, and stores it in the memory directory in a readable form"""
        self.vector_db.upsert(
            documents=[skill.docstring],
            ids=[skill.name],
            metadatas=[{"is_core_primitive": skill.is_core_primitive}],
        )

        skill.dump(self.save_dir(skill.name))

    def retrieve_skills(
        self, query, only_core_primitives=False, no_core_primitives=False, num_results=5
    ) -> list[Skill]:
        """simplest retrieval tactic: query is a task"""

        num_results = min(num_results, self.vector_db.count())

        # if only_core_primitives:
        #     results = self.vector_db.query(
        #         query_texts=[query],
        #         n_results=num_results,
        #         where={"is_core_primitive": True},
        #     )
        # else:
        #     results = self.vector_db.query(query_texts=[query], n_results=num_results)

        results = self.vector_db.query(
            query_texts=[query],
            n_results=num_results,
            where={
                "is_core_primitive": (
                    True
                    if only_core_primitives
                    else (False if no_core_primitives else True or False)
                )
            },
        )

        names = results["ids"][0]
        # get skill objects matching with the retrieved docs
        skills = [self.retrieve_skill_with_name(name) for name in names]
        # filter out None values and return
        return [skill for skill in skills if skill is not None]

    def get_all_skill_embeddings(self):
        results = self.vector_db.get(
            include=["embeddings"],
            where={
                "is_core_primitive": False
            },  # we don't want to cluster/rewrite core primitives - they are simply given...
        )

        return (results["ids"], results["embeddings"])

    def resolve_dependencies(self, code_str):
        """
        collects the entire dependency tree needed to run the code string
        """

        dependencies = []
        skill_dependencies = []
        new_dependencies = list(get_calls(code_str))

        all_skills = os.listdir(self.SKILL_DIR)

        while len(new_dependencies) > 0:
            skill_name = new_dependencies.pop(0)
            if skill_name not in dependencies and skill_name in all_skills:
                skill = self.retrieve_skill_with_name(skill_name)
                if not skill.is_core_primitive:
                    dependencies.append(skill.name)
                    skill_dependencies.append(skill)
                deps = list(get_calls(skill.code))
                new_dependencies.extend(deps)

        print(dependencies)
        return skill_dependencies

    def outside_calls(self, code_str):
        calls = self.get_skill_calls(code_str)
        defs = get_defs(code_str)
        calls_not_in_defs = [call for call in calls if call not in defs]
        return calls_not_in_defs

    def get_skill_calls(self, code_str, func_names: bool = False):
        calls = get_calls(code_str)
        skills = self.all_skills
        skill_names = [skill.name for skill in skills]
        skill_calls = [call for call in calls if call in skill_names]
        if func_names:
            return skill_calls
        called_skills = [self.retrieve_skill_with_name(name) for name in skill_calls]
        return called_skills


if __name__ == "__main__":
    skill_manager = SkillManager(MEMORY_DIR="memory/trained")
    skills = skill_manager.retrieve_skills(
        "parse_location_description", no_core_primitives=True, num_results=5
    )
    Skill.print_skills(skills)
