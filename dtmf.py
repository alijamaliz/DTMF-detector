from scipy.io import wavfile as wav
import pyaudio
import wave
import numpy as np
 
FORMAT = pyaudio.paInt16 # format of sampling 16 bit int
CHANNELS = 1 # number of channels it means number of sample in every sampling
RATE = 44100 # number of sample in 1 second sampling
CHUNK = 1024 # length of every chunk
RECORD_SECONDS = 0.1 # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav" # file name
 
audio = pyaudio.PyAudio()
 
while (True):
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    #reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    print (len(data))
    print (data)

audio.terminate()