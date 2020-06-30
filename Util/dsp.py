import scipy
import scipy.signal
import scipy.fftpack
import numpy as np
from .array_operation import *
import matplotlib.pylab as plt

def sin(f,fs,time,theta=0):
    x = np.linspace(0, 2*np.pi*f*time, int(fs*time))
    return np.sin(x+theta)

def wave(f,fs,time,mode='sin'):
    f,fs,time = float(f),float(fs),float(time)
    if mode == 'sin':
        return sin(f,fs,time,theta=0)
    elif mode == 'square':
        half_T_num = int(time*f)*2 + 1
        half_T_point = int(fs/f/2)
        x = np.zeros(int(fs*time)+2*half_T_point)
        for i in range(half_T_num):
            if i%2 == 0:
                x[i*half_T_point:(i+1)*half_T_point] = -1
            else:
                x[i*half_T_point:(i+1)*half_T_point] = 1
        return x[:int(fs*time)]
    elif mode == 'triangle':
        half_T_num = int(time*f)*2 + 1
        half_T_point = int(fs/f/2)
        up = np.linspace(-1, 1, half_T_point)
        down = np.linspace(1, -1, half_T_point)
        x = np.zeros(int(fs*time)+2*half_T_point)
        for i in range(half_T_num):
            if i%2 == 0:
                x[i*half_T_point:(i+1)*half_T_point] = up.copy()
            else:
                x[i*half_T_point:(i+1)*half_T_point] = down.copy()
        return x[:int(fs*time)]

def downsample(signal,fs1=0,fs2=0,alpha=0,mod = 'just_down'):
    if alpha ==0:
        alpha = int(fs1/fs2)
    if mod == 'just_down':
        return signal[::alpha]
    elif mod == 'avg':
        result = np.zeros(int(len(signal)/alpha))
        for i in range(int(len(signal)/alpha)):
            result[i] = np.mean(signal[i*alpha:(i+1)*alpha])
        return result       

def medfilt(signal,x):
    return scipy.signal.medfilt(signal,x)

def cleanoffset(signal):
    return signal - np.mean(signal)

def bpf(signal, fs, fc1, fc2, numtaps=3, mode='iir'):
    if mode == 'iir':
        b,a = scipy.signal.iirfilter(numtaps, [fc1,fc2], fs=fs)
    elif mode == 'fir':
        b = scipy.signal.firwin(numtaps, [fc1, fc2], pass_zero=False,fs=fs)
        a = 1       
    return scipy.signal.lfilter(b, a, signal)

def fft_filter(signal,fs,fc=[],type = 'bandpass'):
    '''
    signal: Signal
    fs: Sampling frequency
    fc: [fc1,fc2...] Cut-off frequency 
    type: bandpass | bandstop
    '''
    k = []
    N=len(signal)#get N

    for i in range(len(fc)):
        k.append(int(fc[i]*N/fs))

    #FFT
    signal_fft=scipy.fftpack.fft(signal)
    #Frequency truncation

    if type == 'bandpass':
        a = np.zeros(N)
        for i in range(int(len(fc)/2)):
            a[k[2*i]:k[2*i+1]] = 1
            a[N-k[2*i+1]:N-k[2*i]] = 1
    elif type == 'bandstop':
        a = np.ones(N)
        for i in range(int(len(fc)/2)):
            a[k[2*i]:k[2*i+1]] = 0
            a[N-k[2*i+1]:N-k[2*i]] = 0
    signal_fft = a*signal_fft
    signal_ifft=scipy.fftpack.ifft(signal_fft)
    result = signal_ifft.real
    return result

def basefreq(signal,fs,fc=0):
    if fc==0:
        kc = int(len(signal)/2)
    else:   
        kc = int(len(signal)/fs*fc)
    length = len(signal)
    signal_fft = np.abs(scipy.fftpack.fft(signal))[:kc]
    _sum = np.sum(signal_fft)/2
    tmp_sum = 0
    for i in range(kc):
        tmp_sum += signal_fft[i]
        if tmp_sum > _sum:
            return i/(length/fs)

def showfreq(signal,fs,fc=0):
    """
    return f,fft
    """
    if fc==0:
        kc = int(len(signal)/2)
    else:   
        kc = int(len(signal)/fs*fc)
    signal_fft = np.abs(scipy.fftpack.fft(signal))
    f = np.linspace(0,fs/2,num=int(len(signal_fft)/2))
    return f[:kc],signal_fft[0:int(len(signal_fft)/2)][:kc]

def rms(signal):
    signal = signal.astype('float64')
    return np.mean((signal*signal))**0.5

def energy(signal,kernel_size,stride,padding = 0):
    _signal = np.zeros(len(signal)+padding)
    _signal[0:len(signal)] = signal
    signal = _signal
    out_len = int((len(signal)+1-kernel_size)/stride)
    energy = np.zeros(out_len)
    for i in range(out_len):
        energy[i] = rms(signal[i*stride:i*stride+kernel_size]) 
    return energy

def envelope_demodulation(signal,kernel_size,alpha = 0.9,mod='max'):
    out_len = int(len(signal)/kernel_size)
    envelope = np.zeros(out_len)
    for i in range(out_len):
        # envelope[i] = np.max(signal[i*kernel_size:(i+1)*kernel_size])
        envelope[i] = np.sort(signal[i*kernel_size:(i+1)*kernel_size])[int(alpha*kernel_size)]
    return envelope

def main():
    print(downsample(piano,alpha=9))
if __name__ == '__main__':
    main()

