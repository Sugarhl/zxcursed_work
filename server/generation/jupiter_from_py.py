import nbformat

from server.generation.linear import generate_linear_system_latex


BEGIN_CELL = "BEGIN_CELL"
END_CELL = "# END_CELL\n"
CODE = "CODE"
MARKDOWN = "MD"


def create_jupiter(path_to_src: str):
    # Read the input file
    with open(path_to_src, "r") as f:
        file_contents = f.read()

    cells = file_contents.split(END_CELL)

    notebook = nbformat.v4.new_notebook()

    for cell in cells:
        all_lines = cell.split("\n")

        # Skip empty linew between cells
        i = 0
        while BEGIN_CELL not in all_lines[i]:
            i += 1
            if i >= len(all_lines):
                break
        if i >= len(all_lines):
            break

        begin_line = all_lines[i]
        cell_type = begin_line.split(" ")[2]

        if cell_type == CODE:
            q = i + 1
            cell_lines = all_lines[q:]
            cell_contents = "\n".join(cell_lines).strip()
            cell_obj = nbformat.v4.new_code_cell(cell_contents)

        elif cell_type == MARKDOWN:
            q = i + 2
            cell_lines = all_lines[q:-2]
            cell_contents = "\n".join(cell_lines).strip()
            cell_obj = nbformat.v4.new_markdown_cell(cell_contents)

        notebook.cells.append(cell_obj)

    return notebook


SAMPLE_SRC = "server/generation/samples/sample_work"
SAMPLE_OUT = "server/generation/samples/results/sample.ipynb"

SAMPLE_P1 = "server/generation/samples/sample_P1"
SAMPLE_P1_OUT = "server/generation/samples/results/sample_P1.ipynb"


def print_sample():
    notebook = create_jupiter(SAMPLE_SRC)
    with open(SAMPLE_OUT, "w") as f:
        nbformat.write(notebook, f)

    notebook = create_jupiter(SAMPLE_P1)

    ind_task = generate_linear_system_latex()
    cell_idx = len(notebook["cells"]) - 2
    notebook["cells"][cell_idx]["source"] += f"\n{ind_task}\n"

    with open(SAMPLE_P1_OUT, "w") as f:
        nbformat.write(notebook, f)


print_sample()
