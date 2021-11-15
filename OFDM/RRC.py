
import numpy as np
from scipy import signal, fftpack
import matplotlib.pyplot as plt
import functions
import modem
import random

fs = 1000                 #采样频率 3.6G
N = 1000
t = np.arange(-0.5, 0.5, 1 / fs)#采样时间
symbol_count = 384              #符号数
f_carrier = 900000000           #载波频率 900M
wct = 2 * np.pi * f_carrier * t #载波 wct
St = [0] * len(t)             #初始化I路信号
alpha = 0

Ts = 250 / fs
Rs = 1 / Ts

code_rate = int(len(t)/symbol_count)  #符号长度

for i in range(len(t)):
    if abs(i - 1000) > 1000 :
        St[i] = 0
    else:
        St[i] = 1

functions.plot(t, St, 1)

x, y = functions.fft_analysis(St, N, fs)

functions.plot(x, y, 2)

gt = np.sinc(t/Ts) * (np.cos(np.pi * alpha * t / Ts) / (1 - (2 * alpha * t / Ts) ** 2))

St_RRC = signal.convolve(St, gt)

functions.plot(range(len(St_RRC)), St_RRC, 3)

x, y = functions.fft_analysis(St_RRC, N, fs)

functions.plot(x, y, 4)

functions.plot(t, gt, 5)

x, y = functions.fft_analysis(gt, N, fs)

functions.plot(x, y, 6)

functions.plot_show()
