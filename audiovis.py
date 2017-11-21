#!/usr/python
import sys, os
from matplotlib.mlab import specgram
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import numpy as np

# Receiving the inputs
try:
    sound_file = sys.argv[1]
except:
    print "ERROR: Please check your input file"

try:
    visualisation = sys.argv[2]
except:
    print "ERROR: Wrong name of visualisation"

# "wavred" function from sms-tools
INT16_FAC = (2**15)-1
INT32_FAC = (2**31)-1
INT64_FAC = (2**63)-1
norm_fact = {'int16':INT16_FAC, 'int32':INT32_FAC, 'int64':INT64_FAC,'float32':1.0,'float64':1.0}

def openSound(filename):
    """
    Read a sound file and convert it to a normalized floating point array
    filename: name of file to read
    returns fs: sampling rate of file, x: floating point array
    """

    if (os.path.isfile(filename) == False):                  # raise error if wrong input file
        raise ValueError("Input file is wrong")

    fs, x = read(filename)

    if (len(x.shape) !=1):                                   # raise error if more than one channel
        raise ValueError("Audio file should be mono")

    if (fs !=44100):                                         # raise error if more than one channel
        raise ValueError("Sampling rate of input sound should be 44100")

    #scale down and convert audio into floating point number in range of -1 to 1
    x = np.float32(x)/norm_fact[x.dtype.name]
    return fs, x

# Generate frames
def genFrames(sound_file):
    # Function to generate random signal (test)
    # dt = 0.0005
    # t = np.arange(0.0, 20.0, dt)
    # nse = 0.01*np.random.random(size=len(t))
    dt = 0.0005
    NFFT = 1024 # the length of the windowing segment

    (fs, x) = openSound(sound_file)
    sound_size_in_samples = len(x)
    # t = np.arange(0.0, sound_size_in_samples, dt)

    samples_window = 0
    t_temp = 0

    for i in range(0,len(x)):
        temp_file = "sample_" + str(i) + ".png"
        
        x_temp = x[samples_window:samples_window+1024]
        samples_window = samples_window + 1024
        t_temp = np.arange(samples_window, 1024, 1)
        
        plt.plot(t_temp, x_temp)
        Pxx, freqs, bins, im = plt.specgram(x_temp, NFFT=NFFT, Fs=1024, noverlap=900)
        plt.axis('off')
        plt.savefig(temp_file, bbox_inches='tight')
    return 0

# Join frames
def joinFrames():
    # ffmpeg -r 1/5 -i img%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4
    return 0

# Join frames with audio
def audiovis():
    return 0

genFrames(sound_file)