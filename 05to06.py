import os
from pydub import AudioSegment

def adjust_volume(wav_file_path, ratio):
    """Adjust the volume of a .wav file by applying the given ratio."""
    audio = AudioSegment.from_wav(wav_file_path)
    adjusted_audio = audio + ratio
    return adjusted_audio

def adjust_volume_in_directory(directory, ratio):
    """Adjust volume of all .wav files in a directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                adjusted_audio = adjust_volume(file_path, ratio)
                adjusted_audio.export(file_path, format="wav")
                print(f"Volume adjusted for {file_path}.")

# Example usage
directory = "speeches06"
volume_ratio = -7.3  # Adjust this value as needed
adjust_volume_in_directory(directory, volume_ratio)
