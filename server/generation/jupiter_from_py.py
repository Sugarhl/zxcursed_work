import nbformat


BEGIN_CELL = "BEGIN_CELL"
END_CELL = "# END_CELL\n"
CODE = "CODE"
MARKDOWN = "MD"


def create_jupiter(path_to_src: str, path_to_out: str):
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
        cell_lines = all_lines[i:]
        cell_contents = "\n".join(cell_lines[1:]).strip()

        if cell_type == CODE:
            cell_obj = nbformat.v4.new_code_cell(cell_contents)
        elif cell_type == MARKDOWN:
            cell_obj = nbformat.v4.new_markdown_cell(cell_contents)

        notebook.cells.append(cell_obj)

    with open(path_to_out, "w") as f:
        nbformat.write(notebook, f)


# create_jupiter(
#     "server/generation/samples/sample_work.py", "server/generation/samples/sample.ipynb"
# )
