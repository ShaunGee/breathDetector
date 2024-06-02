'''
Author: Shaun Gumbaketi
Project: Nail Bite Ring

Description:
This Python script captures the sound of breathing using a microphone.

Dependencies (install via 'pip install pyaudio numpy'):
- PyAudio 
- NumPy

Usage (install dependencies first):
1. plug mic in.
2. Run the script via terminal/cmd "python3 /path/to/file.py" or use IDE
3. Should say 'Listening for breath...' 
4. Breathe into mic. Output should read 'Breath detected!' if positive detection
5. ctrl + c to kill script.
6. Adjust if needed..

Note: Adjust values in '---ADJUST----' below to further configure script. Anything
      between LOWRANGE and HIGHRANGE will be picked up as breath.
'''

import pyaudio
import numpy as np

# ---ADJUST----
TEST = False # Set to True to test mic input then adjust lowrange and highrange below
HIGHRANGE = .41
LOWRANGE = .37


# Constants
CHUNK = (1024 * 2)  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (samples per second)

def detect_breath(stream):
    try:
        while True:
            # Read audio data from the stream
            data = stream.read(CHUNK)
            
            # Convert binary data to numpy array
            audio_np = np.frombuffer(data, dtype=np.int16)
            
            # Calculate the root mean square (RMS) as volume level
            if len(audio_np) == 0:
                continue
            # Normalize audio data to range [-1, 1]
            audio_normalized = audio_np / np.max(np.abs(audio_np))            
            rms = np.sqrt(np.mean(np.square(audio_normalized)))

            #If TEST is true then rms will show in terminal. Use to test mic input
            if TEST:    
                print(rms)
                
            if rms > LOWRANGE and rms < HIGHRANGE:
                print("Breath detected!")
                # -- On 'breath detected' code goes here -- 
                

    except KeyboardInterrupt:
        pass
    except Exception as e:
	    print("Error: ", e)
     
def main():
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # Open a stream to capture audio from the microphone
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Listening for breath...")
    detect_breath(stream)
    # Close stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()