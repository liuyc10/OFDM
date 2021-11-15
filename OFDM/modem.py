from scipy import signal, fftpack
import numpy as np


def modulation(f, fc):
    f_RF = f * fc
    return f_RF


def SSB_modulation(f, wct):
    f_ssb = signal.hilbert(f)
    fh_real = f_ssb.real
    fh_imag = f_ssb.imag

    f_RF = fh_real * np.cos(wct) - fh_imag * np.sin(wct)
    return f_RF


def IQ_modulation(St_I, St_Q, wct):
    f_RF = St_I * np.cos(wct) - St_Q * np.sin(wct)
    return f_RF


def demodulation(f_RF_filted, fc, fs):
    f_demodulation = f_RF_filted * fc * 2
    f_BB = low_pass_filter(f_demodulation, 100000000, fs)
    return f_BB


def IQ_demodulation(f_RF_filted, wct, fs):
    fx_demodulation = f_RF_filted * np.cos(wct) * 2
    fy_demodulation = f_RF_filted * (- np.sin(wct)) * 2
    St_I_BB = low_pass_filter(fx_demodulation, 100000000, fs)
    St_Q_BB = low_pass_filter(fy_demodulation, 100000000, fs)
    return St_I_BB, St_Q_BB


def low_pass_filter(input, f_cutoff, fs):
    Wn = 2 * f_cutoff / fs

    b, a = signal.butter(5, Wn, 'lowpass')

    output = signal.filtfilt(b, a, input)

    return output


def band_pass_filter(input, f_i, f_e, fs):
    Wn = [2 * f_i / fs, 2 * f_e / fs]
    b, a = signal.butter(5, Wn, 'bandpass')

    output = signal.filtfilt(b, a, input)
    return output


def RRC_filter(N, alpha, Ts, fs):
    T_delta = 1 / float(fs)
    time_idx = ((np.arange(N) - N / 2)) * T_delta
    sample_num = np.arange(N)
    RRC_impulse_response = np.zeros(N, dtype=float)

    for i in sample_num:
        t = (i - N / 2) * T_delta
        if t == 0.0:
            RRC_impulse_response[i] = 1.0 - alpha + (4 * alpha / np.pi)
        elif alpha != 0 and t == Ts / (4 * alpha):
            RRC_impulse_response[i] = (alpha / np.sqrt(2)) * (((1 + 2 / np.pi) * (np.sin(np.pi / (4 * alpha)))) + (
                        (1 - 2 / np.pi) * (np.cos(np.pi / (4 * alpha)))))
        elif alpha != 0 and t == -Ts / (4 * alpha):
            RRC_impulse_response[i] = (alpha / np.sqrt(2)) * (((1 + 2 / np.pi) * (np.sin(np.pi / (4 * alpha)))) + (
                        (1 - 2 / np.pi) * (np.cos(np.pi / (4 * alpha)))))
        else:
            RRC_impulse_response[i] = (np.sin(np.pi * t * (1 - alpha) / Ts) + 4 * alpha * (t / Ts) * np.cos(
                np.pi * t * (1 + alpha) / Ts)) / (np.pi * t * (1 - (4 * alpha * t / Ts) * (4 * alpha * t / Ts)) / Ts)

    return time_idx, RRC_impulse_response


# 定义加性高斯白噪声
def awgn(y, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(y ** 2) / len(y)
    npower = xpower / snr
    f_RF_noise = np.random.randn(len(y)) * np.sqrt(npower) + y
    return f_RF_noise


def judgment_2ask(input, symbol_count):
    massage = []
    symbol_period = len(input) / symbol_count

    for i in range(symbol_count):
        sum = 0
        centre = int((i + 0.5) * symbol_period)
        for j in range(-5, 5, 1):
            if input[centre + j] > 0.5:
                sum = sum + 1
            else:
                sum = sum + 0
        if sum >= 5:
            massage.append(1)
        else:
            massage.append(0)
    return massage

# def judgment_16QAM(input, symbol_len):
