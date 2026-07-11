import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ── Fig 1: B3/B4 — unity feedback, G = K/(s+2) → T = K/(s+2+K) ──
Ks = [2, 8, 98]
fig, ax = plt.subplots(figsize=(8, 5))
for K in Ks:
    num = [K]
    den = [1, 2 + K]        # s + (2+K)
    sys = signal.TransferFunction(num, den)
    t, y = signal.step(sys, T=np.linspace(0, 3, 1000))
    ax.plot(t, y, label=f'K={K}  (pole={-(2+K)}, y_inf={K/(K+2):.3f})')

ax.axhline(1, color='gray', linestyle=':', linewidth=1, label='reference')
ax.set_xlabel('t'); ax.set_ylabel('y(t)')
ax.set_title('P control step response — bigger K = pole further left = faster, but e(inf) never 0')
ax.legend(); ax.grid(True, alpha=0.4)
plt.tight_layout()

# ── Fig 2: B5 — plant gain 1.0 → 1.5, open-loop compensation vs closed-loop ──
K = 98
fig2, ax2 = plt.subplots(figsize=(8, 5))
for g, style in [(1.0, '--'), (1.5, '-')]:
    # open-loop: pre-multiply by 2 = 1/G(0)  (calibrated for the OLD plant g=1)
    comp = 2
    ol = signal.TransferFunction([g * comp], [1, 2])
    # closed-loop: T = gK/(s+2+gK)
    cl = signal.TransferFunction([g * K], [1, 2 + g * K])
    T = np.linspace(0, 3, 1000)
    ax2.plot(*signal.step(ol, T=T), style, color='tab:orange', label=f'open-loop comp, plant gain={g}')
    ax2.plot(*signal.step(cl, T=T), style, color='tab:blue', label=f'closed-loop K={K}, plant gain={g}')

ax2.axhline(1, color='gray', linestyle=':', linewidth=1)
ax2.set_xlabel('t'); ax2.set_ylabel('y(t)')
ax2.set_title('Plant drifts 1.0 -> 1.5: who stays near the reference?')
ax2.legend(); ax2.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()
