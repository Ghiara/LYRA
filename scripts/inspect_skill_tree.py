import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

from agents.model import Skill
from agents.memory import MemoryManager
import io
from PIL import Image


def make_house_tree():
    memory_manager = MemoryManager()

    # all_skills = memory_manager.skill_manager.all_skills
    build_house = memory_manager.skill_manager.retrieve_skill_with_name("build_house")
    all_skills = memory_manager.skill_manager.resolve_dependencies(build_house.code)
    all_skills.append(build_house)

    for skill in all_skills:
        print(len(memory_manager.skill_task_examples(skill)))

    skills_with_deps = {}
    for skill in all_skills:
        deps = memory_manager.skill_manager.get_skill_calls(skill.code, func_names=True)
        deps = [
            dep
            for dep in deps
            if dep
            not in [
                "get_point_at_distance_and_rotation_from_point",
                "parse_location_description",
            ]
        ]
        if skill.name in [
            "identify_beam_block",
            "identify_roof_base",
            "identify_roof_tiles",
        ]:
            deps.extend(["get_object_color", "get_object_size"])
        skills_with_deps[skill.name] = deps

    G = nx.DiGraph()
    for parent, children in skills_with_deps.items():
        for child in children:
            G.add_edge(parent, child)

    A = to_agraph(G)
    for node in A.nodes():
        node.attr["shape"] = "rect"  # use 'rect' or 'box'
        if node.name in [
            "get_object_size",
            "get_object_pose",
            "get_object_color",
            "get_bbox",
            "put_first_on_second",
            "get_objects",
        ]:
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "#CAD8E0"
        elif node.name not in [
            "place_roof_tiles",
            "assemble_roof",
            "identify_beam_block",
            "identify_roof_base",
            "identify_roof_tiles",
            "build_house_base",
            "build_house",
            "make_line_of_blocks_next_to",
        ]:
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "#E4B4AE"
        else:
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "#F2F2F2"

    A.layout(prog="dot")

    # buf = io.BytesIO()
    # A.draw(buf, format='png')
    # buf.seek(0)
    # img = Image.open(buf)

    A.draw("scripts/graph.png")

    # Display with matplotlib (optional)
    img = plt.imread("scripts/graph.png")

    # Load image with PIL and show with matplotlib
    plt.imshow(img)
    plt.axis("off")

    plt.show()


def make_line_tree():
    skills_with_deps = {
        "make_line_with_blocks": ["move_block_next_to_reference"],
        "move_block_next_to_reference": [
            "put_first_on_second",
            "get_object_size",
            "get_object_pose",
        ],
    }
    G = nx.DiGraph()
    for parent, children in skills_with_deps.items():
        for child in children:
            G.add_edge(parent, child)

    A = to_agraph(G)
    for node in A.nodes():
        node.attr["shape"] = "rect"  # use 'rect' or 'box'
        if node.name in [
            "get_object_size",
            "get_object_pose",
            "get_object_color",
            "get_bbox",
            "put_first_on_second",
            "get_objects",
        ]:
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "#CAD8E0"
        else:
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "#F2F2F2"

    A.layout(prog="dot")

    save_dir = "scripts/line_tree.png"
    A.draw(save_dir)
    img = plt.imread(save_dir)

    # Load image with PIL and show with matplotlib
    plt.imshow(img)
    plt.axis("off")

    plt.show()


make_house_tree()

# core_primitives = [skill.name for skill in all_skills if skill.is_core_primitive]
# node_colors = [
#     "lightcoral" if node in core_primitives else "grey" for node in G.nodes()
# ]

# plt.figure(figsize=(8, 6))
# pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")  # Tree layout
# nx.draw(
#     G,
#     pos,
#     with_labels=True,
#     arrows=True,
#     node_color=node_colors,
#     edge_color="gray",
#     node_size=2000,
#     font_size=10,
# )
# plt.show()
