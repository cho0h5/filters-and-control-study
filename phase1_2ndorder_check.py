import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

wn = 2
zetas = [0, 0.3, 0.7, 1, 2]
fig, ax = plt.subplots(figsize=(8, 5))
for zeta in zetas:
    num = [wn**2]
    den = [1, 2*zeta*wn, wn**2]
    sys = signal.TransferFunction(num, den)
    t, y = signal.step(sys, T=np.linspace(0, 10, 1000))
    ax.plot(t, y, label=f'zeta={zeta}')

ax.axhline(1, color='gray', linestyle=':', linewidth=1)
ax.set_xlabel('t'); ax.set_ylabel('y(t)')
ax.set_title('2nd-order step response by damping ratio')
ax.legend(); ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()
