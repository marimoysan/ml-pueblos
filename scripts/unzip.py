import zipfile
import glob

path_to_zip_file = "../resources/*"

zip_files = glob.glob(path_to_zip_file)
for path_to_zip_file in zip_files:
    with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
        zip_ref.extractall("../data/raw")
