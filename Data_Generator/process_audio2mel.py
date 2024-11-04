import os
from tqdm import tqdm
from utils import audiofile2specfile
from multiprocessing import Pool

# audio_folder_path = r"E:\AirFTP\Datasets\DeepShip-Enh\audio-3\Propeller"
# mel_folder_path = r"E:\AirFTP\Datasets\DeepShip-Enh\mel-3\Propeller"


def process_audio2mel(chunk):
    print('======================DEBUG START: chunk======================')
    print(chunk)
    print('======================DEBUG  END : chunk======================')
    audio_files, audio_folder_path, mel_folder_path = chunk
    for audio_file_name in audio_files:
        audio_file_path = os.path.join(audio_folder_path, audio_file_name)
        audio_file_basename = audio_file_name.split(".")[0]
        mel_file_path = os.path.join(mel_folder_path, f"{audio_file_basename}.png")
        audiofile2specfile(
            audio_path=audio_file_path, method="mel", saved_path=mel_file_path
        )

