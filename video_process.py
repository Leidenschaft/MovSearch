# -*- coding:utf-8  -*-
import wave
#import pylab as pl
import numpy as np
#from scipy.io import wavfile
#import datetime
import sys
#ffmpeg -i test.avi -vn -y -acodec pcm_s16le -ss 0 -t 30 auto2.wav
##ffmpeg -i a_0.wav -ss 0 -t 30 -f s16le -acodec pcm_s16le -b:a 16 -ar 8000
# -ac 2 out.wav

#ffmpeg -i a_0.wav -ss 0 -t 30 -acodec pcm_s16le -ar 8000 -ac 2 out.wav
#ffmpeg -i All_0.mp4 -ss 0 -t 30 -acodec pcm_s16le -ar 8000 -ac 2 out.wav
def read_wav(filename):
    # 打开WAV文档
    f = wave.open(filename, "rb")
    # f, snd = wavfile.read(filename)
    # print snd.shape
    # 读取格式信息
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    frames = ((int)(nframes / framerate)) * framerate - framerate
    str_data = f.readframes(frames)
    f.close()
    # 将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    #print "wave_data:", wave_data, " shape:", wave_data.shape
    wave_data.shape = -1, 2
    #wave_data = wave_data[0]
    wave_data = np.abs(np.mean(wave_data, axis=1))
    wave_data = wave_data.T
    # for i in wave_data:
    #     if np.isnan(i) or np.isinf(i):
    #         print i
    #print "READ WAV OK"
    return np.abs(wave_data), nframes

def get_fft(signal_list, N):
    #print "BEGIN FFT"
    wave_fft = np.fft.rfft(np.abs(signal_list))
    #wave_fft = np.abs(signal_list)
    #print "DO FFT OK: Shape:", wave_fft.shape
    return wave_fft

def read_fft(filename):
    count = 0
    fft_list = list()
    with open(filename, "rb") as f:
        while True:
            s = f.read()
            if s == None:
                return
            count += 1
            if count >= 1:
                break
def save_fft(fft_list, filename):
    count = 0
    with open(filename, "wb") as f:
        for data in fft_list:
            #print(data)
            f.write(data)
            count += 1
            # if count >= 10:
            #     break

import sys

def sound_parse(f_name):

    wave, nframe = read_wav(f_name)

    fft_len = int(nframe)
    wave_fft = get_fft(wave, fft_len)
    fft_len = wave_fft.shape[0]

    buck_num = 100
    buck_size = int(fft_len / buck_num)
    buckets = list()
    total = 0.0
    for i in range(buck_num):
        energy = 0.0
        for j in range(buck_size):
            energy += abs(wave_fft[i*buck_size + j])
            total += abs(wave_fft[i*buck_size + j])
        buckets.append(energy)
    for i in range(buck_num):
        buckets[i] =abs(buckets[i]/total)
    time = np.array(range(0, fft_len))*(2*np.pi / fft_len)
    save_fft(buckets, f_name.replace('.wav','.fft3'))
    # pl.plot(range(0,buck_num), buckets, c="r")
    # pl.xlabel("fre")
    # pl.show()
