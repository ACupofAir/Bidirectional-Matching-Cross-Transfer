import librosa
import numpy as np


def split_frame_by_data(frame_size: any, frame_shift: any, audio_data: np.array,
                        sr: int) -> np.array:
    """split frame by audio data(np.array)

    Args:
        frame_size (number): frame size can be int or float, it is the number of the samples of a 
            frame
        frame_shift (number): it is the frame start position between any two frames
        audio_data (np.array): audio np.array
        sr (int): sample rate

    Returns:
        np.array: return a np.array of audio frames
    """
    frames = librosa.util.frame(audio_data,
                                frame_length=int(frame_size * sr),
                                hop_length=int(frame_shift * sr))
    frames = frames.transpose()
    return frames


def split_frame_by_file(frame_size, frame_shift, audio_file: str) -> np.array:
    """split a audio file like *.wav to many frames type with np.array

    Args:
        frame_size (number): frame size can be int or float, it is the number of the samples of a 
            frame
        frame_shift (number): it is the frame start position between any two frames
        audio_file (str): the path of input audio file

    Returns:
        np.array: return a np.array of audio frames
        sr: the sample rate used to split frame
    """
    audio_data, sr = librosa.load(audio_file)
    return split_frame_by_data(frame_size, frame_shift, audio_data, sr), sr
