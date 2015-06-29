import numpy
import pyaudio
import analyse
import math

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 2 is a USB microphone, your number may differ.
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = 2,
    input = True)

last_pitch = -100
last_loudness = -100

def getNote():
    global last_pitch, last_loudness
    while True:
        try:
            # Read raw microphone data
            rawsamps = stream.read(1024)
            # Convert raw data to NumPy array
            samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            # Show the volume and pitch
            loudness = analyse.loudness(samps)
            #pitch = analyse.musical_detect_pitch(samps)
            pitch = analyse.musical_detect_pitch(samps)
        except:
            continue
        if not pitch:
            continue

        level = (pitch - 60.018)/ 1.0

        if pitch and last_pitch:
            pitch_diff = pitch - last_pitch
        else:
            pitch_diff = 100
        loudness_diff = loudness - last_loudness
        #print 'pitch:', math.floor(level), 'pitch_diff:', pitch_diff, 'loudness_diff:', loudness_diff

        last_pitch = pitch
        last_loudness = loudness
        if loudness_diff < 0 and pitch_diff > 2.0:
            continue

        print 'OK', round(level), pitch
        last_returned = level
        return level

if __name__ == '__main__':
    while True:
        getNote()
