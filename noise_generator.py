import os
import numpy as np
from scipy.signal import butter, lfilter
from pydub import AudioSegment
from pydub.playback import play

# Function to apply a low-pass Butterworth filter
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

# Audio settings
duration = 60          # Duration in seconds
fs = 44100             # Sampling rate (samples per second)
cutoff_freq = 3000     # Cutoff frequency to remove high frequencies
output_file = "soft_noise.wav"

# Generate white noise
white_noise = np.random.normal(0, 1, int(duration * fs))

# Apply low-pass filter to make the noise softer
filtered_noise = butter_lowpass_filter(white_noise, cutoff_freq, fs)

# Convert filtered data to audio format
audio_data = (filtered_noise * 32767).astype(np.int16)
audio_segment = AudioSegment(
    audio_data.tobytes(),
    frame_rate=fs,
    sample_width=2,
    channels=1
)

# Play the generated sound with error handling
try:
    play(audio_segment)
except Exception as e:
    print(f"Error while playing sound: {e}")

# Export the sound to a .wav file with error handling
try:
    audio_segment.export(output_file, format="wav")
    print(f"File successfully saved: {output_file}")
except Exception as e:
    print(f"Error while saving the file: {e}")
