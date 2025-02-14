import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def run_all_notebooks(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                print(f"Running notebook: {notebook_path}")
                run_notebook(notebook_path)


def run_notebook(notebook_path):
    with open(notebook_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": os.path.dirname(notebook_path)}})
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)


if __name__ == "__main__":
    folder_path = "notebooks"
    run_all_notebooks(folder_path)