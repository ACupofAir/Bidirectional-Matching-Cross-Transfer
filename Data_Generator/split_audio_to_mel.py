# %%
import os
import sys
from tqdm import tqdm
from colorama import Fore
import json

from utils import audio2specfile, split_frame_by_file

# * get all need split file name
# ! [FIXME]: change to the name you needed which should be a key value in data_config.json
data_config_path = r"C:\Users\june\Workspace\Bidirectional-matching-cross-transfer\Data_Generator\data_config.json"
dataset_name = "DeepShip"
with open(data_config_path, "r") as json_file:
    data = json.load(json_file)
dataset_directory = data[dataset_name]["directory"]
dataset_audio_directory = data[dataset_name]["audio_path"]
method = "mel"
frame_size = 2.5

audio_class_names = os.listdir(dataset_audio_directory)

dataset_img_dir = os.path.join(dataset_directory, method + "-" + str(frame_size))
if not os.path.exists(dataset_img_dir):
    os.mkdir(dataset_img_dir)
# %%
# * split audio and convert it to spec store it in the shipeat_img_dir
with tqdm(
    total=len(audio_class_names),
    desc=f"Audio Class Convert to Spec:",
    bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET),
) as audio_cls_bar:
    for class_name in audio_class_names:
        #  create directory to store convert image
        class_img_dir = os.path.join(dataset_img_dir, class_name)
        if not os.path.exists(class_img_dir):
            os.mkdir(class_img_dir)

        audio_class_path = os.path.join(dataset_audio_directory, class_name)
        frame_idx = 0

        class_folder_list = os.listdir(audio_class_path)
        with tqdm(
            total=len(class_folder_list),
            desc=f"{class_name} split to frames:",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET),
        ) as cls_folder_bar:
            # split a wav file to multi frames
            for file_name in class_folder_list:
                split_num = 0
                audio_file_path = os.path.join(audio_class_path, file_name)
                splited_frames, sr = split_frame_by_file(
                    frame_size=frame_size,
                    frame_shift=frame_size / 2,
                    audio_file=audio_file_path,
                )
                with tqdm(
                    total=len(splited_frames),
                    desc=f"convert {class_name}/{file_name} frames to spec:",
                    bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.WHITE, Fore.RESET),
                ) as frame_bar:
                    # convert each frame to spec
                    for frame in splited_frames:
                        saved_path = os.path.join(
                            dataset_img_dir, class_name, str(frame_idx) + ".png"
                        )
                        frame_idx += 1

                        audio2specfile(audio_data=frame, sr=sr, saved_path=saved_path)
                        frame_bar.update(1)

                cls_folder_bar.update(1)
        audio_cls_bar.update(1)
