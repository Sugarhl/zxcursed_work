import nbformat


def create_jupiter(path_to_src: str, path_to_out: str):

    # Read the input file
    with open(path_to_src, 'r') as f:
        file_contents = f.read()

    # Split the file into cells based on the delimiter
    cells = file_contents.split('# END_CELL\n')

    # Create a new Jupyter Notebook
    notebook = nbformat.v4.new_notebook()

    # Loop through the cells and add them to the notebook
    for cell in cells:
        all_lines = cell.split('\n')

        i = 0
        while (not 'BEGIN_CELL' in all_lines[i]):
            i += 1
            if i >= len(all_lines):
                break
        if i >= len(all_lines):
            break
        begin_line = all_lines[i]
        print(begin_line)
        cell_type = begin_line.split(' ')[2]
        print(cell_type)

        cell_lines = all_lines[i:]

        # Parse the cell contents
        cell_contents = '\n'.join(cell_lines[1:]).strip()

        # Create a new cell object
        if cell_type == 'CODE':
            cell_obj = nbformat.v4.new_code_cell(cell_contents)
        else:
            cell_obj = nbformat.v4.new_markdown_cell(cell_contents)

        # Add the cell to the notebook
        notebook.cells.append(cell_obj)

    # Save the notebook to a file
    with open(path_to_out, 'w') as f:
        nbformat.write(notebook, f)


create_jupiter('../../sample_work.py', '../../sample.ipynb')
