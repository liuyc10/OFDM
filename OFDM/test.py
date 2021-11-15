import encoding
import matplotlib.pyplot as plt
import numpy as np


s = 'asdf'

print(s)

code = encoding.convert_to_hex(s)

print(code)

qam_code = encoding.encoding_16QAM(encoding.sampling(code,4))

print(qam_code)
print(len(qam_code))

plt.subplot(321)
plt.scatter(qam_code.real, qam_code.imag)

ifft_output = np.fft.ifft(qam_code)

print(ifft_output)

air_real = ifft_output.real
air_imag = ifft_output.imag
#print(air_imag)

fft_output = np.fft.fft(ifft_output)
print(fft_output)
print(len(fft_output))
plt.subplot(324)
plt.plot(ifft_output.real, ifft_output.imag)

fft_output_real = np.fft.fft(air_real)
print(fft_output_real)
print(len(fft_output_real))
plt.subplot(324)
plt.scatter(ifft_output.real, ifft_output.imag)

fft_output_imag = np.fft.fft(air_imag)
print(fft_output_imag)
plt.subplot(325)
plt.scatter(fft_output_imag.real, fft_output_imag.imag)


plt.show()

output = encoding.convert_to_text(code)

print(output)

