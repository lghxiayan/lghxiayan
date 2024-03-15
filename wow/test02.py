import numpy as np
import sounddevice as sd
from scipy.io import wavfile

fs = 44100  # Hz
f = 440  # Hz
length = 5  # s
sd.default.device[0] = 6

recording = sd.rec(frames=fs * length, samplerate=fs, blocking=True, channels=1)
wavfile.write('recording.wav', fs, recording)
myarray = np.arange(fs * length)
myarray = np.sin(2 * np.pi * f / fs * myarray)

sd.play(myarray, fs)
