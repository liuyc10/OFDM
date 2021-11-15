
import encoding
import matplotlib.pyplot as plt
import numpy as np

fs = 2048
N = 1024
t = np.arange(0, 0.5, 1 / fs)

plt.plot(t, 210 * np.sin(np.pi * t))
plt.plot(t, 120 * np.sin(2 * np.pi * t))

plt.show()