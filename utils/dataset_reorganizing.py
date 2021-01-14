import os
import shutil
import random
import pandas as pd

# establishing the main files/directories paths
project_dir_path = os.path.abspath(os.pardir)
unlabeled_data_dir = 'dataset'
labeled_data_dir = 'labeled_dataset'
unlabeled_data_dir_path = os.path.join(project_dir_path, unlabeled_data_dir)
labeled_data_dir_path = os.path.join(project_dir_path, labeled_data_dir)

# loading the labeling infos
labels_df = pd.read_csv(os.path.join(unlabeled_data_dir_path,
                        'CLIN_DIA.csv'),
                        index_col='id')

# if the destination directory already existing with 
# images in it, recursively remove it
if os.path.exists(labeled_data_dir_path):
    shutil.rmtree(labeled_data_dir_path)
os.mkdir(labeled_data_dir_path)

# fixing of the subdirectory names based on classes
malignant_dir = 'malignant'
benign_dir = 'benign'

# creation of the subdirectories
malignant_class_path = os.path.join(labeled_data_dir_path, malignant_dir)
benign_class_path = os.path.join(labeled_data_dir_path, benign_dir)
os.mkdir(malignant_class_path)
os.mkdir(benign_class_path)

# names of original data subdirectories
unlabeled_data_subdirs = ['SET_D', 'SET_E', 'SET_F']

# copying the pictures from original subdirectories
# into new ones based on malignant/benign classes
for subdir in unlabeled_data_subdirs:
    subdir_path = os.path.join(unlabeled_data_dir_path, subdir)
    image_names = os.listdir(subdir_path)
    for image_name in image_names:
        if(image_name.endswith('.BMP')):
            image_prefix = image_name[:-4].lower()
            if(labels_df.loc[image_prefix, 'kat.Diagnose']=='2'
               or labels_df.loc[image_prefix, 'kat.Diagnose']=='3'):
                image_copy_name = 'm_' + image_prefix + '.bmp'
                image_path = os.path.join(subdir_path, image_name)
                image_copy_path = os.path.join(malignant_class_path, image_copy_name)
                shutil.copy2(image_path, image_copy_path)
            elif(labels_df.loc[image_prefix, 'kat.Diagnose']=='1'):
                image_copy_name = 'b_' + image_prefix + '.bmp'
                image_path = os.path.join(subdir_path, image_name)
                image_copy_path = os.path.join(benign_class_path, image_copy_name)
                shutil.copy2(image_path, image_copy_path)


# we don't want malignant/benign subdirs
# we want train/valid/test subdirs, 
# themselves subdivided into malignant/benign
# first let's create this hierarchy
for subdir in ['train', 'valid', 'test']:
    malignant_subpath = os.path.join(labeled_data_dir_path, subdir, malignant_dir)
    benign_subpath = os.path.join(labeled_data_dir_path, subdir, benign_dir)
    os.makedirs(malignant_subpath)
    os.makedirs(benign_subpath)


# we create a list where we're going to randomly pick
# train/valid/test images for each class malignant/benign
malignant_images = os.listdir(os.path.join(labeled_data_dir_path, malignant_dir))
benign_images = os.listdir(os.path.join(labeled_data_dir_path, benign_dir))

# we randomly shuffle these lists, which is equivalent to randomly pick elements
random.seed(4444)
random.shuffle(malignant_images)
random.shuffle(benign_images)

# we devide into subsets according to some fixed ratio
valid_ratio = 0.15
test_ratio = 0.10

malignant_valid_set_len = int(valid_ratio * len(malignant_images))
malignant_test_set_len = int(test_ratio * len(malignant_images))
benign_valid_set_len = int(valid_ratio * len(benign_images))
benign_test_set_len = int(test_ratio * len(benign_images))

malignant_valid_set = malignant_images[-malignant_valid_set_len:]
malignant_images = malignant_images[:-malignant_valid_set_len]
malignant_test_set = malignant_images[-malignant_test_set_len:]
malignant_train_set = malignant_images[:-malignant_test_set_len]

benign_valid_set = benign_images[-benign_valid_set_len:]
benign_images = benign_images[:-benign_valid_set_len]
benign_test_set = benign_images[-benign_test_set_len:]
benign_train_set = benign_images[:-benign_test_set_len]

# now we can move all the images in the new hierarchy
#  malignant
image_to_move_base_path = os.path.join(labeled_data_dir_path, malignant_dir)
#       / validation set
for image in malignant_valid_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'valid', malignant_dir, image)
    shutil.move(image_to_move_path, destination_path)

#       / test set
for image in malignant_test_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'test', malignant_dir, image)
    shutil.move(image_to_move_path, destination_path)

# #       / training set
for image in malignant_train_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'train', malignant_dir, image)
    shutil.move(image_to_move_path, destination_path)

# benign 
image_to_move_base_path = os.path.join(labeled_data_dir_path, benign_dir)
#       / validation set
for image in benign_valid_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'valid', benign_dir, image)
    shutil.move(image_to_move_path, destination_path)

#       / test set
for image in benign_test_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'test', benign_dir, image)
    shutil.move(image_to_move_path, destination_path)

# #       / training set
for image in benign_train_set:
    image_to_move_path = os.path.join(image_to_move_base_path, image)
    destination_path = os.path.join(labeled_data_dir_path, 'train', benign_dir, image)
    shutil.move(image_to_move_path, destination_path)

# we remove the old hierarchy
shutil.rmtree(malignant_class_path)
shutil.rmtree(benign_class_path)
