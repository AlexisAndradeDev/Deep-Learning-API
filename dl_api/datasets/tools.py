import os

def create_dataset_class(dataset_classes, dataset_path, class_name):
    dataset_classes[class_name] = {'subsets': {}}
    # Create class dir
    class_dir = dataset_path + f'/{class_name}'
    os.mkdir(class_dir)
