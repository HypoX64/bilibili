import time
import numpy as np
import scipy.fftpack
from .array_operation import *
from .dsp import *
from .util import *
import librosa
from scipy.io import wavfile
import os
import matplotlib.pylab as plt

piano = np.array([0,27.5,29.1,30.9,32.7,34.6,36.7,38.9,41.2,
                43.7,46.2,49.0,51.9,55.0,58.3,61.7,65.4,69.3,
                73.4,77.8,82.4,87.3,92.5,98.0,103.8,110.0,116.5,
                123.5,130.8,138.6,146.8,155.6,164.8,174.6,185.0,
                196.0,207.7,220.0,233.1,246.9,261.6,277.2,293.7,
                311.1,329.6,349.2,370.0,392.0,415.3,440.0,466.2,
                493.9,523.3,554.4,587.3,622.3,659.3,698.5,740.0,
                784.0,830.6,880.0,932.3,987.8,1047,1109,1175,1245,
                1319,1397,1480,1568,1661,1760,1865,1976,2093,2217,
                2349,2489,2637,2794,2960,3136,3322,3520,3729,3951,4186,4400])

piano_10 = np.array([0,73.4,207.7,349.2,587.3,987.8,1245,1661,2093,2794,4400])

#------------------------------IO------------------------------
def numpy2voice(npdata):
    voice = np.zeros((len(npdata),2))
    voice[:,0] = npdata
    voice[:,1] = npdata
    return voice

def load(path,ch = 0):
    freq,audio = wavfile.read(path)
    if ch == 0:
        audio = audio[:,0]
    elif ch == 1:
        audio = audio[:,1]
    return freq,audio.astype(np.float64)

def write(npdata,path='./tmp/test_output.wav',freq = 44100):
    voice = numpy2voice(npdata)
    wavfile.write(path, freq, voice.astype(np.int16))

def play(path):
    os.system("paplay "+path)

def playtest(npdata,freq = 44100):
    time.sleep(0.5)
    makedirs('./tmp/')
    voice = numpy2voice(npdata)
    wavfile.write('./tmp/test_output.wav', freq, voice.astype(np.int16))
    play('./tmp/test_output.wav')


#------------------------------DSP------------------------------

def filter(audio,fc=[],fs=44100,win_length = 4096):
    for i in range(len(audio)//win_length):
        audio[i*win_length:(i+1)*win_length] = fft_filter(audio[i*win_length:(i+1)*win_length], fs=fs, fc=fc)
    
    return audio

# def freq_correct(src,dst,fs=44100,alpha = 0.05,fc=3000):
#     src_freq = basefreq(src, 44100,3000)
#     dst_freq = basefreq(dst, 44100,3000)
#     offset = int((src_freq-dst_freq)/(src_freq*0.05))
#     out = librosa.effects.pitch_shift(dst.astype(np.float64), 44100, n_steps=offset)
#     #print('freqloss:',round((basefreq(out, 44100,3000)-basefreq(src, 44100,3000))/basefreq(src, 44100,3000),3))
#     return out.astype(np.int16)

def freq_correct(src,dst,fs=44100,fc=3000,mode = 'normal',win_length = 1024, alpha = 1):
    
    out = np.zeros_like(src)
    try:
        if mode == 'normal':
            src_oct = librosa.hz_to_octs(basefreq(src, fs, fc))
            dst_oct = librosa.hz_to_octs(basefreq(dst, fs, fc))
            offset = (dst_oct-src_oct)*12*alpha
            out = librosa.effects.pitch_shift(src, 44100, n_steps=offset)
        elif mode == 'track':
            length = min([len(src),len(dst)])
            for i in range(length//win_length):
                src_oct = librosa.hz_to_octs(basefreq(src[i*win_length:(i+1)*win_length], fs, fc))
                dst_oct = librosa.hz_to_octs(basefreq(dst[i*win_length:(i+1)*win_length], fs, fc))
                
                offset = (dst_oct-src_oct)*12*alpha
                out[i*win_length:(i+1)*win_length] = librosa.effects.pitch_shift(src[i*win_length:(i+1)*win_length], 44100, n_steps=offset)
        return out
    except Exception as e:
        return src

    #print('freqloss:',round((basefreq(out, 44100,3000)-basefreq(src, 44100,3000))/basefreq(src, 44100,3000),3))
    

def energy_correct(src,dst,mode = 'normal',win_length = 512,alpha=1):
    """
    mode: normal | track
    """
    out = np.zeros_like(src)
    if mode == 'normal':
        src_rms = rms(src)
        dst_rms = rms(dst)
        out = src*(dst_rms/src_rms)*alpha
    elif mode == 'track':
        length = min([len(src),len(dst)])
        tracks = []
        for i in range(length//win_length):
            src_rms = np.clip(rms(src[i*win_length:(i+1)*win_length]),1e-6,np.inf)
            dst_rms = rms(dst[i*win_length:(i+1)*win_length])
            tracks.append((dst_rms/src_rms)*alpha)
        tracks = np.clip(np.array(tracks),0.1,10)
        tracks = interp(tracks, length)
        out = src*tracks

    return np.clip(out,-32760,32760)

def time_correct(src,dst,_min=0.25):
    src_time = len(src)
    dst_time = len(dst)
    rate = np.clip(src_time/dst_time,_min,100)
    out = librosa.effects.time_stretch(src,rate)
    return out

def freqfeatures(signal,fs):
    signal = normliaze(signal,mode = '5_95',truncated=100)
    signal_fft = np.abs(scipy.fftpack.fft(signal))
    length = len(signal)
    features = []
    for i in range(len(piano_10)-1):
        k1 = int(length/fs*piano_10[i])
        k2 = int(length/fs*piano_10[i+1])
        features.append(np.mean(signal_fft[k1:k2]))
    return np.array(features)



def main():
    xp = [1, 2, 3]
    fp = [3, 2, 0]
    x = [0, 1, 1.5, 2.72, 3.14]
    print(np.interp(x, xp, fp))

if __name__ == '__main__':
    main()