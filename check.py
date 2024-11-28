import os
from pydub import AudioSegment

def calculate_volume(wav_file_path):
    """Calculate the volume (dBFS) of a .wav file."""
    audio = AudioSegment.from_wav(wav_file_path)
    return audio.dBFS

def adjust_volume(wav_file_path, target_dBFS):
    """Adjust the volume of a .wav file to match the target dBFS."""
    audio = AudioSegment.from_wav(wav_file_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    adjusted_audio = audio.apply_gain(change_in_dBFS)
    return adjusted_audio

def compare_volumes(folder1, folder2):
    """Compare volumes of .wav files in two folders."""
    folder1_files = [f for f in os.listdir(folder1) if f.endswith('.wav')]
    folder2_files = [f for f in os.listdir(folder2) if f.endswith('.wav')]
    
    common_files = set(folder1_files).intersection(folder2_files)
    
    if not common_files:
        print("No common .wav files found in the provided folders.")
        return
    
    for filename in common_files:
        file1_path = os.path.join(folder1, filename)
        file2_path = os.path.join(folder2, filename)
        
        volume1 = calculate_volume(file1_path)
        volume2 = calculate_volume(file2_path)
        
        print(f"Comparing {filename}:")
        print(f"Volume in {folder1}: {volume1} dBFS")
        print(f"Volume in {folder2}: {volume2} dBFS")
        print(f"Difference: {volume1 - volume2} dB\n")

# Example usage
folder1 = "speeches\\0000"
folder2 = "speeches\\aamckie"
compare_volumes(folder1, folder2)
