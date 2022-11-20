import os
import shutil

def delete_dataset_files(dataset_root_dir):
    if os.path.isdir(dataset_root_dir):
        shutil.rmtree(dataset_root_dir)
    else:
        raise ValueError(f'Path {dataset_root_dir} is not a directory')