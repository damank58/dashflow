import os


def create_py_functions(directory, filename, content: zip):
    """
    Creates a new .py file in the specified directory.

    Args:
        directory (str): The path to the directory where the file should be created.
        filename (str): The name of the file to be created (including the .py extension).
        content (zip): The content to write to the file. Defaults to an empty list.
    """
    filepath = os.path.join(directory, filename)

    # Create the directory if it doesn't exist

    os.makedirs(directory, exist_ok=True)

    try:
        with open(filepath, "w") as file:
            # file.write(''.join('{0}\n'.format(lib) for lib in imports))
            for s in content:
                file.write(f'#{s[0]}\n\n') # question commented
                file.write(f'{s[1]}\n\n')  # code
        print(f"Python functions successfully written to '{filename}' created successfully in '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_streamlit_script(filename, columns: int, page_code: list, directory='pages'):
    file_index = len(os.listdir(directory))
    file = '[{}]_{}.py'.format(file_index, filename.replace(" ", "_"))
    filepath = os.path.join(directory, file)

    if not os.path.isdir(directory):
        os.mkdir(directory)

    try:
        print(page_code)
        with open(filepath, "w") as f:
            f.write('import streamlit as st\n\n\n')
            f.write(f'st.title("{filename}")\n\n')
            for code in page_code:
                f.write('# {}\n\n'.format(code['chart_type']))
                f.write('# {}\n\n'.format(code['question']))
                f.write('{}\n\n'.format(code['code_ls']))
            f.write(f'columns = {columns}\n')

            indicator_functions = [code['function_name'] for code in page_code if code['chart_type'].lower() == 'indicator']
            indicator_col = len(indicator_functions)
            for i in range(0, len(indicator_functions), indicator_col):
                col_string = ''
                function_string = ''
                for j in range(i, indicator_col+i):
                    col_string += f'col{j + 1}, '
                    if j < len(indicator_functions):
                        function_string += f'with col{j + 1}:\n\t{indicator_functions[j]}()\n'
                col_string = col_string.strip('').strip(',')
                f.write(f'{col_string} = st.columns({indicator_col})\n')
                f.write(function_string)

            chart_functions = [code['function_name'] for code in page_code if code['chart_type'].lower() != 'indicator']
            for i in range(0, len(chart_functions), columns):
                col_string = ''
                function_string = ''
                for j in range(i, columns + i):
                    col_string += f'col{j + 1}, '
                    if j < len(chart_functions):
                        function_string += f'with col{j + 1}:\n\t{chart_functions[j]}()\n'
                col_string = col_string.strip('').strip(',')
                f.write(f'{col_string} = st.columns(columns)\n')
                f.write(function_string)

        print(f"Output successfully written to '{filename}' created successfully in '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

