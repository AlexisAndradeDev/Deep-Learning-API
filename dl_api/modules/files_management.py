import os
import shutil

def delete_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    else:
        raise ValueError(f'Path {dir_path} is not a directory')