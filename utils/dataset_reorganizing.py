import os
import shutil

import pandas as pd

# establishing the main files/directories paths

project_dir_path = os.path.abspath(os.pardir)
unlabeled_data_dir = 'dataset'
labeled_data_dir = 'labeled_dataset'
unlabeled_data_dir_path = os.path.join(project_dir_path, unlabeled_data_dir)
labeled_data_dir_path = os.path.join(project_dir_path, labeled_data_dir)

# loading the labeling infos
labels_df = pd.read_csv(os.path.join(unlabeled_data_dir_path, 'CLIN_DIA.csv'),
                        index_col='id')

# if the destination directory already existing with 
# images in it, recursively remove it
if os.path.exists(labeled_data_dir_path):
    shutil.rmtree(labeled_data_dir_path)
os.mkdir(labeled_data_dir_path)

# fixing of the subdirectory names based on classes
danger_dir = 'class_d'
safety_dir = 'class_s'

# creation of the subdirectories
danger_class_path = os.path.join(labeled_data_dir_path, danger_dir)
safe_class_path = os.path.join(labeled_data_dir_path, safety_dir)
os.mkdir(danger_class_path)
os.mkdir(safe_class_path)

# names of original data subdirectories
unlabeled_data_subdirs = ['SET_D', 'SET_E', 'SET_F']

# copying the pictures from original subdirectories
# into new ones based on dangerous/safe classes
for subdir in unlabeled_data_subdirs:
    subdir_path = os.path.join(unlabeled_data_dir_path, subdir)
    image_names = os.listdir(subdir_path)
    for image_name in image_names:
        if(image_name.endswith('.BMP')):
            image_prefix = image_name[:-4].lower()
            if(labels_df.loc[image_prefix, 'kat.Diagnose']=='2'
               or labels_df.loc[image_prefix, 'kat.Diagnose']=='3'):
                image_copy_name = 'd_' + image_prefix + '.bmp'
                image_path = os.path.join(subdir_path, image_name)
                image_copy_path = os.path.join(danger_class_path, image_copy_name)
                shutil.copy2(image_path, image_copy_path)
            elif(labels_df.loc[image_prefix, 'kat.Diagnose']=='1'):
                image_copy_name = 's_' + image_prefix + '.bmp'
                image_path = os.path.join(subdir_path, image_name)
                image_copy_path = os.path.join(safe_class_path, image_copy_name)
                shutil.copy2(image_path, image_copy_path)
