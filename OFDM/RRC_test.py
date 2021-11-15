
import numpy as np
from scipy import signal, fftpack
import matplotlib.pyplot as plt
import functions
import modem
import random

fs = int(30e5)                  #采样频率 3.6G
ts = 1e-3                       #采样时间
df = int(15e3)                  #子载波间隔15kHz
symbol_per_frame = 15           #符号数
Ts = ts / symbol_per_frame      #符号长度66.67us
Rs = 1 / Ts                     #符号速率:15*2*600/0.001=18Mbps
code_sample_count = int(fs / Rs)#符号采样数
t = np.arange(0, ts, 1 / fs)    #时间函数
N = len(t)                      #FTT点数

f_carrier = 900000000           #载波频率 900M
wct = 2 * np.pi * f_carrier * t #载波 wct
St = [0] * len(t)               #初始化I路信号
alpha = 0.22

for i in range(int(Rs * ts)):
    temp = random.randint(0, 1)
    print(temp)
    for j in range(code_sample_count):
        St[i * code_sample_count + j] = temp



functions.plot(t, St, 1)

x, y = functions.fft_analysis(St, N, fs)

functions.plot(x, y, 2)

t_idx, gt = modem.RRC_filter(N, alpha, Ts, fs)

St_RRC = signal.convolve(St, gt)


functions.plot(np.arange(0, len(St_RRC)/fs, 1/fs), St_RRC, 3)

x, y = functions.fft_analysis(St_RRC, len(St_RRC), fs)

functions.plot(x, y, 4)

s = int(N / 2)
e = int(len(St_RRC) - (N / 2) + 1)

print(s)
print(e)

St_RRC = St_RRC[s:e]

functions.plot(t, St_RRC, 5)

x, y = functions.fft_analysis(St_RRC, N, fs)

functions.plot(x, y, 6)

functions.plot_show()

