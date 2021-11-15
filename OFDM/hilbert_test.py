from scipy import signal
import numpy as np
import functions
import modem
import random

fs = 3600000000
N = 2048
t = np.arange(0, 0.0001, 1 / fs)
symbol_len = 384
f_carrier = 900000000
wct = 2 * np.pi * f_carrier * t
fx = [0] * len(t)
code_rate = int(len(t)/symbol_len)


fx = np.cos(2 * np.pi * 3840000 * t)
fy = np.cos(2 * np.pi * 1920000 * t)
fc = np.cos(2 * np.pi * f_carrier * t)

functions.plot(t, fx, 1)
x, y = functions.fft_analysis(fx, 2048, fs)
functions.plot(x, y, 2)

f_RF = modem.modulation(fx, fc)
functions.plot(t, f_RF, 3)
x, y = functions.fft_analysis(f_RF, N, fs)
functions.plot(x, y, 4)

f_RF = modem.SSB_modulation(fx, wct)
functions.plot(t, f_RF, 5)
x, y = functions.fft_analysis(f_RF, N, fs)
functions.plot(x, y, 6)

f_RF = modem.IQ_modulation(fx, fy, wct)
functions.plot(t, f_RF, 7)
x, y = functions.fft_analysis(f_RF, N, fs)
functions.plot(x, y, 8)

functions.plot_show()