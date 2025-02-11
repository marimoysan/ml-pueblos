import zipfile

path_to_zip_file = "../data.zip"

with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
    zip_ref.extractall("../data/raw")
