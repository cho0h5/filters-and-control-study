import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Z1, Z5의 pole을 단위원과 함께 그려서 안/밖 확인
for label, num, den in [('Z1 (a=0.5)', [1], [1, -0.5]),
                         ('Z5 (H(z))', [1], [1, -0.5])]:
    z, p, k = signal.tf2zpk(num, den)
    print(label, 'poles:', p, '|pole|:', np.abs(p))

theta = np.linspace(0, 2*np.pi, 200)
plt.plot(np.cos(theta), np.sin(theta), 'k--', label='unit circle')
plt.scatter([0.5], [0], color='red', label='pole (a=0.5)')
plt.axis('equal'); plt.legend(); plt.grid(True, alpha=0.4)
plt.title('Z-plane: pole vs unit circle')
plt.show()
