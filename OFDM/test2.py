import numpy as np
import functions
import modem
import random

fs = 3600000000  # 采样频率 3.6G
N = 2048
t = np.arange(0, 0.0001, 1 / fs)  # 采样时间
symbol_count = 384  # 符号数
f_carrier = 900000000  # 载波频率 900M
wct = 2 * np.pi * f_carrier * t  # 载波 wct
St_I = [0] * len(t)  # 初始化I路信号
St_Q = [0] * len(t)  # 初始化Q路信号
code_rate = int(len(t) / symbol_count)  # 符号长度
print(code_rate)

# fx = np.cos(2 * np.pi * 32 * t)
fc = np.cos(2 * np.pi * f_carrier * t)

org_I = []
org_Q = []

for i in range(symbol_count):
    temp_x = random.randint(0, 1)
    temp_y = random.randint(0, 1)
    org_I.append(temp_x)
    org_Q.append(temp_y)
    for j in range(code_rate):
        St_I[i * code_rate + j] = temp_x
        St_Q[i * code_rate + j] = temp_y

functions.plot(t, St_I, 1, 'Org_st_i')

x, y = functions.fft_analysis(St_I, N, fs)

functions.plot(x, y, 2, 'FFT_org_i')

functions.plot(t, St_Q, 3, 'Org_st_q')

x, y = functions.fft_analysis(St_Q, N, fs)

functions.plot(x, y, 4, 'FFT_org_q')

f_RF = modem.IQ_modulation(St_I, St_Q, wct)

functions.plot(t, f_RF, 5, 'IQ_modulation')

x, y = functions.fft_analysis(f_RF, N, fs)

functions.plot(x, y, 6, 'IQ_FFT')

f_RF_noise = modem.awgn(f_RF, 5)

functions.plot(t, f_RF_noise, 7, 'add noise')

x, y = functions.fft_analysis(f_RF_noise, N, fs)

functions.plot(x, y, 8, 'add noise FFT')

f_RF_band_filted = modem.band_pass_filter(f_RF_noise, 850000000, 950000000, fs)

functions.plot(t, f_RF_band_filted, 9, 'band_filted')

x, y = functions.fft_analysis(f_RF_band_filted, N, fs)

functions.plot(x, y, 10, 'band_filted_FFT')

fx_BB, fy_BB = modem.IQ_demodulation(f_RF_band_filted, wct, fs)

massage_I = modem.judgment_2ask(fx_BB, symbol_count)
massage_Q = modem.judgment_2ask(fy_BB, symbol_count)

crc_x = True
crc_y = True
for i in range(len(org_I)):

    if org_I[i] == massage_I[i]:
        crc_x = crc_x and True
    else:
        crc_x = crc_x and False
        break

    if org_Q[i] == massage_Q[i]:
        crc_y = crc_y and True
    else:
        crc_y = crc_y and False
        break

print(crc_x, crc_y)

functions.plot_show()
