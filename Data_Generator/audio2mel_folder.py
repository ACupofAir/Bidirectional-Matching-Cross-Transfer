import os
from tqdm import tqdm
from utils import audiofile2specfile

audio_folder_path = "/mnt/e/Datasets/TwoBill/testdata/audio/unknown"
mel_folder_path = "/mnt/e/Datasets/TwoBill/testdata/mel"

if __name__ == "__main__":
    if not os.path.exists(mel_folder_path):
        os.mkdir(mel_folder_path)

    for audio_file_name in tqdm(os.listdir(audio_folder_path)):
        audio_file_path = os.path.join(audio_folder_path, audio_file_name)
        audio_file_basename = audio_file_name.split(".")[0]
        mel_file_path = os.path.join(mel_folder_path, f"{audio_file_basename}.png")
        audiofile2specfile(audio_path=audio_file_path, method='mel', saved_path=mel_file_path)