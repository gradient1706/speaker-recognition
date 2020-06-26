import nltk
#nltk.download('punkt')
import nltk.data
import pyaudio
import wave
import sys
from pynput import keyboard
import sounddevice as sd
import soundfile as sf
import time
import os


index = 1
username = "Abc"
filename = 'trainingData/'
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

print("Repeatedly record 3 times for speaker-recognition")
print("Press s to start record, q to quit record, esc to exit program")

filename = filename+username
if not os.path.exists(filename):
    os.makedirs(filename)

all = []


def on_press(key):
    global index
    if key == keyboard.Key.esc:
        stream.close()
        p.terminate()
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k in ['s']:
        print('Key pressed: ' + k)
        data = stream.read(chunk) # Record data
        all.append(data)

    if k in ['q']:
        print('Key pressed: ' + k)
        
        data = b''.join(all)
        filewavname = filename +'/'+username+'_'+str(index) + '.wav'
        wf = wave.open(filewavname, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()
        index = index+1
        if index == 4:
            return False


listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys


