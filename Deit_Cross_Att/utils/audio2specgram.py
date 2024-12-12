import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os


def audio2spectrogram(audio_data: np.array, sr: int, method: str = 'mel') -> None:
    """convert audio data to spectrogram use different methods

    Args:
        audio_data (np.array): Input audio numpy array.
        sr (int): Sample rate of the audio.
        method (str, optional): _description_. Defaults to 'mel'.
    """

    if method == 'mel':
        spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr)
        librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max),
                                 y_axis='mel',
                                 x_axis='time')
        plt.colorbar(format='%+2.0f dB')
    plt.title(f'sample_dots: {len(audio_data)}, sample_rate: {sr}')


def audiofile2specfile(audio_path: str, method='mel', saved_path='', show_legend=False):
    """convert audio file to spectrogram use different methods, and save the spectrogram file to 
    `saved_path`

    Args:
        audio_path (str): The wav, mps file path.
        saved_path (str): The output spectrogram file path, if passed var is None, the spectrogram
            will be saved in the runtime directory with input_filename's basename.
        method (str, optional): The method used for generate spectrogram. Defaults to 'mel'..
    """

    if not os.path.isfile(audio_path):
        raise ValueError(f"{audio_path} is unavailable")

    y, sr = librosa.load(audio_path)

    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    if show_legend:
        librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max),
                                    y_axis='mel',
                                    x_axis='time')
        plt.colorbar(format='%+2.0f dB')
    else:
        librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max))
    if not saved_path:
        audio_file_name = os.path.basename(audio_path)
        saved_path = os.path.splitext(audio_file_name)[0] + ".png"
    plt.savefig(saved_path, bbox_inches='tight', pad_inches=0)


def audio2specfile(audio_data: np.array, sr: int, method: str = 'mel', saved_path='') -> None:
    """convert audio data to spectrogram use different methods and save to saved_path

    Args:
        audio_data (np.array): Input audio numpy array.
        sr (int): Sample rate of the audio.
        method (str, optional): _description_. Defaults to 'mel'.
        saved_path (str): The output spectrogram file path, if passed var is None, the spectrogram
            will be saved in the runtime directory with input_filename's basename.
    """

    if method == 'mel':
        spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr)
        librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max))

        if not saved_path:
            saved_path = f"{method}.png"
        plt.savefig(saved_path, bbox_inches='tight', pad_inches=0)