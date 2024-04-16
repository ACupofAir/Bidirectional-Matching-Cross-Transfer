import os
import random
import shutil
from tqdm import tqdm


# * config args
org_img_path = '/mnt/d/workspace/dataset/shipeat/mel/2'
source_path = '/mnt/d/workspace/dataset/shipeat/mel/source/2'
target_path = '/mnt/d/workspace/dataset/shipeat/mel/target/2'
rate = 0.14


def split_folder(org_folder: str, target_main_folder: str, target_sub_folder: str,
                 rate: float) -> None:
    """split a img folder to two image folders

    Args:
        org_folder (str): the folder which will be splited
        target_main_folder (str): the folder store the rate*org_image_folder size
        target_sub_folder (str): the rest of images
        rate(float): the split rate
    """
    if not os.path.isdir(org_folder):
        raise ValueError(f'{org_folder} is not a valid directory')
    if not os.path.isdir(target_main_folder):
        os.mkdir(target_main_folder)
    if not os.path.isdir(target_sub_folder):
        os.mkdir(target_sub_folder)

    all_files = os.listdir(org_folder)
    random.shuffle(all_files)
    org_folder_size = len(all_files)
    main_folder_num = int(org_folder_size * rate)

    for i, file in tqdm(enumerate(all_files)):
        src_file = os.path.join(org_folder, file)
        if i < main_folder_num:
            dst_folder = target_sub_folder
        else:
            dst_folder = target_main_folder
        dst_file = os.path.join(dst_folder, file)
        shutil.copy(src_file, dst_file)

    print('>>>===================Result======================')
    print(f'org folder:\t{org_folder_size}')
    print(f'target main:\t{len(os.listdir(target_main_folder))}')
    print(f'target sub:\t{len(os.listdir(target_sub_folder))}')
    print('======================Result===================<<<')


if __name__ == '__main__':
    split_folder(org_img_path, source_path, target_path, rate)