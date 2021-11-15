import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt


def fft_analysis(f, N, fs):
    F = fftpack.fft(f, N)
    f_freq = fftpack.fftfreq(N, 1 / fs)
    fft_shift = fftpack.fftshift(F)
    fft_freq_shift = fftpack.fftshift(f_freq)

    return fft_freq_shift, abs(fft_shift) * 2 / N


def plot(x, y, num, title=None):
    row = 3
    col = 4

    plt.subplot(row, col, num)
    if title:
        plt.title(title)
    plt.plot(x, y)


def plot_show():
    plt.show()
