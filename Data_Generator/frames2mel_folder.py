import os
from tqdm import tqdm
from utils import audiofile2specfile
from multiprocessing import Pool
from process_audio2mel import process_audio2mel

frame_size = 10
process_num = 8
class_name = ["Cargo", "Passengership", "Propeller", "Tanker", "Tug"]
audio_folder_path = f"E:\\AirFTP\\Datasets\\DeepShip-Enh\\audio-{frame_size}"
mel_folder_path = f"E:\\AirFTP\\Datasets\\DeepShip-Enh\\mel-{frame_size}"


def audio2mel_folder(audio_folder_path, mel_folder_path, process_num):
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


if __name__ == "__main__":
    for cls in class_name:
        audio2mel_folder(
            os.path.join(audio_folder_path, cls),
            os.path.join(mel_folder_path, cls),
            process_num,
        )
