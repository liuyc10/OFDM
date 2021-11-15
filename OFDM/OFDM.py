import numpy as np
import random
import pylab as plt
import encoding

n = 2000  # 生成二进制数的数量
_db_ = 17  # 信噪比db
bit_list = []
for i in range(n):
    bit_list.append(random.randint(0, 1))

input = np.array(bit_list)
reshaped_input = np.reshape(input, (int(n / 4), 4))

print(reshaped_input)


def _trans_(_a, _b, _c, _d):
    return 8 * _a + 4 * _b + 2 * _c + _d


_map_ = dict([('0', (3, 3)), ('1', (1, 3)), ('2', (-3, 3)), ('3', (-1, 3)),
              ('7', (-1, 1)), ('6', (-3, 1)), ('5', (1, 1)), ('4', (3, 1)),
              ('8', (3, -3)), ('9', (1, -3)), ('10', (-3, -3)), ('11', (-1, -3)),
              ('15', (-1, -1)), ('14', (-3, -1)), ('13', (1, -1)), ('12', (3, -1))])

qam_output_list = []

for i in range(int(n / 4)):
    num = _trans_(reshaped_input[i][0], reshaped_input[i][1], reshaped_input[i][2], reshaped_input[i][3])

    transed_num = complex(_map_[str(num)][0], _map_[str(num)][1])  # complex函数转换成复数形式，代表I Q两路
    qam_output_list.append(transed_num)

qam_output_array = np.array(qam_output_list)  # 相当于完成了串并转换

print(qam_output_array)

qam_output_real_array = np.zeros(int(n / 4))
qam_output_imag_array = np.zeros(int(n / 4))

for i in range(int(n / 4)):
    qam_output_real_array[i] = qam_output_array[i].real
    qam_output_imag_array[i] = qam_output_array[i].imag

print(qam_output_real_array)
print(qam_output_imag_array)

ifft_output = np.fft.ifft(qam_output_array)  # 傅里叶逆变换

print(ifft_output)

real_array = np.zeros(int(n / 4))  # 存储实部
imag_array = np.zeros(int(n / 4))  # 存储虚部

for i in range(int(n / 4)):
    real_array[i] = ifft_output[i].real
    imag_array[i] = ifft_output[i].imag


def wgn(x, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(x ** 2) / len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)


real_array_ = real_array + wgn(real_array, _db_)  # 加入高斯白噪声后的信号
imag_array_ = imag_array + wgn(imag_array, _db_)

fft_input_list = []

for i in range(int(n / 4)):  # 将加入噪声后的信号转换为复数形式
    transed_num_ = complex(real_array_[i], imag_array_[i])
    fft_input_list.append(transed_num_)
fft_input_array = np.array(fft_input_list)

fft_output = np.fft.fft(fft_input_array)  # fft

print("fft_output:")
print(fft_output)

i_output = np.zeros(int(n / 4))
q_output = np.zeros(int(n / 4))

for i in range(int(n / 4)):
    i_output[i] = fft_output[i].real
    q_output[i] = fft_output[i].imag

# plt.figure(figsize=(5,8))

plt.subplot(221)
plt.plot(input[:20])
plt.subplot(222)
plt.scatter(qam_output_real_array[0:int(n / 4)], qam_output_imag_array[0:int(n / 4)])
plt.title('plot img 1')
plt.subplot(223)
plt.scatter(i_output[0:int(n / 4)], q_output[0:int(n / 4)])
plt.title('plot img 2')

nn = np.array([(-3, -3), (-3, -1), (-1, -3), (-1, -1), (3, 3), (3, 1), (1, 3), (1, 1),
               (-3, 3), (-3, 1), (-1, 3), (-1, 1), (3, -3), (3, -1), (1, -3), (1, -1)])

for _n_ in range(100):
    _i_ = i_output[_n_]
    _q_ = i_output[_n_]

    d_list = []
    for i in range(16):
        d = (_i_ - nn[i][0]) ** 2 + (_q_ - nn[i][1]) ** 2
        d_list.append(d)

    print(d_list.index(min(d_list)), end=' ')

plt.show()
