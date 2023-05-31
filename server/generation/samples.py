import nbformat
from server.generation.jupiter_from_py import create_jupiter
from server.tasks.linear import generate_linear_system_latex
from server.tasks.slae_with_parameter import generate_slae_with_param
from server.tasks.surface import generate_surface_dots


SAMPLE_TEMPLATE = "server/generation/samples/sample_"
RESULT_TEMPLATE = "server/generation/samples/results/sample_"
EXT = ".ipynb"

SAMPLE_SRC = f"{SAMPLE_TEMPLATE}work"
SAMPLE_OUT = f"{RESULT_TEMPLATE}work{EXT}"

SAMPLE_P1 = f"{SAMPLE_TEMPLATE}P1"
RESULT_P1 = f"{RESULT_TEMPLATE}P1{EXT}"

SAMPLE_P2 = f"{SAMPLE_TEMPLATE}P2"
RESULT_P2 = f"{RESULT_TEMPLATE}P2{EXT}"

SAMPLE_P3 = f"{SAMPLE_TEMPLATE}P3"
RESULT_P3 = f"{RESULT_TEMPLATE}P3{EXT}"


def print_sample_base():
    notebook = create_jupiter(SAMPLE_SRC)
    with open(SAMPLE_OUT, "w") as f:
        nbformat.write(notebook, f)


def print_sample_p1():
    notebook = create_jupiter(SAMPLE_P1)

    ind_task = generate_linear_system_latex()
    cell_idx = len(notebook["cells"]) - 2
    notebook["cells"][cell_idx]["source"] += f"\n\n{ind_task}\n"

    with open(RESULT_P1, "w") as f:
        nbformat.write(notebook, f)


def print_sample_p2():
    notebook = create_jupiter(SAMPLE_P2)

    ind_task = generate_slae_with_param()
    cell_idx = len(notebook["cells"]) - 2
    notebook["cells"][cell_idx]["source"] += f"\n\n{ind_task}\n"

    with open(RESULT_P2, "w") as f:
        nbformat.write(notebook, f)


def print_sample_p3():
    notebook = create_jupiter(SAMPLE_P3)

    ind_task = generate_surface_dots()
    cell_idx = len(notebook["cells"]) - 2
    notebook["cells"][cell_idx]["source"] += f"\n\n{ind_task}\n"

    with open(RESULT_P3, "w") as f:
        nbformat.write(notebook, f)


def print_samples():
    print_sample_base()
    print_sample_p1()
    print_sample_p2()
    print_sample_p3()


# print_samples()
