import os
import sys
import random
import time
import numpy as np
import matplotlib.pylab as plt

sys.path.append("..")
from Util import util,ffmpeg,dsp,sound
from Util import array_operation as arrop


"""音调对应的频率
* C大调中就是1=C中C唱做do,而在1=D中D要唱作do
* C D E F G A B -> do re mi fa so la xi
* 暂时不支持C# D# F# A#
"""
NOTES = ['C','D','E','F','G','A','B']
base_pitch = [16.352,18.354,20.602,21.827,24.500,27.500,30.868]
#Frequency in hertz (semitones above or below middle C)
OPS = np.zeros(7*10) 
for i in range(10):
    for j in range(7):
        OPS[i*7+j] = base_pitch[j]*(2**i)

def getfreq(note,PN):
    if note[0] == '-':
        return 0
    index = 4*7-1 + NOTES.index(PN) + int(note[0]) #1 = C or D.....
    if '+' in note:
        index += (len(note)-1)*7
    elif '-' in note:
        index -= (len(note)-1)*7
    freq = OPS[index]
    return freq

def wave(f, fs, time, mode='sin'):
    length = int(fs*time)
    signal = dsp.wave(f, fs, time, mode)
    weight = np.zeros(length)
    weight[0:length//10] = np.hanning(length//10*2)[0:length//10]
    weight[length//10:] = np.hanning(int(length*0.9*2))[int(length*0.9):]
    return signal*weight


"""拍子强度
strengths = {'2/4':['++',''],
             '3/4':['++','',''],
             '4/4':['++','','+',''],
             '3/8':['++','',''],
             '6/8':['++','','','+','','']}
"""

def getstrength(i,BN,x):
    if int(BN[0]) == 2:
        if i%2 == 0:
            x = x*1.25
    elif int(BN[0]) == 3:
        if i%3 == 0:
            x = x*1.25
    elif int(BN[0]) == 4:
        if i%4 == 0:
            x = x*1.25
        elif i%4 == 2:
            x = x*1.125
    return x

def readscore(path):
    notations = {}
    notations['data'] =[]
    for i,line in enumerate(open(path),0):
        line = line.strip('\n')
        if i==0:
            notations['PN'] = line
        elif i == 1:
            notations['BN'] = line
        elif i == 2:
            notations['BPM'] = float(line)
        elif i == 3:
            notations['PNLT'] = float(line)
        else:
            notations['data'].append(line.split(','))
    return notations


def notations2music(notations, mode = 'sin', isplot = False):
    BPM = notations['BPM']
    BN = notations['BN']
    PNLT = notations['PNLT']
    interval = 60.0/BPM 
    fs = 44100
    time = 0

    music = np.zeros(int(fs*(len(notations['data'])+2)*interval))

    for i in range(len(notations['data'])):
        for j in range(len(notations['data'][i])//2):
            freq = getfreq(notations['data'][i][j*2],notations['PN'])
            if freq != 0:
                music[int(time*fs):int(time*fs)+int(PNLT*fs)] += getstrength(i,BN,wave(freq, fs, PNLT, mode = mode))
            
            if isplot:
                plot_data = music[int(time*fs):int(time*fs)+int(PNLT*fs)]
                plt.clf()
                plt.subplot(221)
                plt.plot(np.linspace(0, len(plot_data)/fs,len(plot_data)),plot_data)
                plt.title('Current audio waveform')
                plt.xlabel('Time')
                plt.ylim((-1.5,1.5))

                plt.subplot(222)
                _plot_data = plot_data[int(len(plot_data)*0.2):int(len(plot_data)*0.25)]
                plt.plot(np.linspace(0, len(_plot_data)/fs,len(_plot_data)),_plot_data)
                plt.title('Partial audio waveform')
                plt.xlabel('Time')
                plt.ylim((-1.5,1.5))

                plt.subplot(223)
                f,k = dsp.showfreq(plot_data, 44100, 2000)
                plt.plot(f,k)
                plt.title('FFT')
                plt.xlabel('Hz')
                plt.ylim((-1000,10000))
                plt.pause(interval-0.125)

            time += float(notations['data'][i][j*2+1])*interval

    return (arrop.sigmoid(music)-0.5)*65536

notations = readscore('./music/SchoolBell.txt')
print(notations)
# sin triangle square
music = notations2music(notations,mode='sin',isplot=False)
import threading
t=threading.Thread(target=sound.playtest,args=(music,))
t.start()
music = notations2music(notations,mode='sin',isplot=True)
