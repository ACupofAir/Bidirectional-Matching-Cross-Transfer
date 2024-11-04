import os
from tqdm import tqdm
from utils import audiofile2specfile
from multiprocessing import Pool
from process_audio2mel import process_audio2mel

audio_folder_path = r"E:\AirFTP\Datasets\DeepShip-Enh\audio-2.5\Cargo"
mel_folder_path = r"E:\AirFTP\Datasets\DeepShip-Enh\mel-2.5\Cargo"
process_num = 8

if __name__ == "__main__":
    if not os.path.exists(mel_folder_path):
        os.makedirs(mel_folder_path)

    audio_files = os.listdir(audio_folder_path)
    chunk_size = len(audio_files) // process_num

    chunks = [
        audio_files[i : i + chunk_size] for i in range(0, len(audio_files), chunk_size)
    ]

    chunks = [(chunk, audio_folder_path, mel_folder_path) for chunk in chunks]

    with Pool(process_num) as pool:
        pool.map(process_audio2mel, chunks)
