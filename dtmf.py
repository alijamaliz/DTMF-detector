from scipy.io import wavfile as wav
import pyaudio
import wave
import numpy as np
 
DTMF_TABLE = {
    1: [1209, 697],
    2: [1336, 697],
    3: [1477, 697],
    'A': [1633, 697],

    4: [1209, 770],
    5: [1336, 770],
    6: [1477, 770],
    'B': [1633, 770],

    7: [1209, 852],
    8: [1336, 852],
    9: [1477, 852],
    'C': [1633, 852],

    '*': [1209, 941],
    0: [1336, 941],
    '#': [1477, 941],
    'D': [1633, 941],
} 

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

    # reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    # calculate fourier transform
    complexFourierTransform = np.fft.fft(data)
    absoluteFourierTransforn = []
    for i in range(0, len(complexFourierTransform)):
        absoluteFourierTransforn.append(int(abs(complexFourierTransform[i])))

    sortedAbsoluteFourierTransforn = np.sort(absoluteFourierTransforn)
    # print (len(complexFourierTransform))
    max = sortedAbsoluteFourierTransforn[-1]
    secondMax = sortedAbsoluteFourierTransforn[-3]
    print ("first: {}: {}".format(absoluteFourierTransforn.index(max), max))
    print ("second: {}: {}".format(absoluteFourierTransforn.index(secondMax), secondMax))
    print()
    # print (absoluteFourierTransforn[DTMF_TABLE[1][0]])

audio.terminate()