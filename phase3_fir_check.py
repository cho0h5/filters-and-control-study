import numpy as np
import matplotlib.pyplot as plt

def freq_response(h, worN=512):
    w = np.linspace(0, np.pi, worN)
    H = np.array([sum(hk * np.exp(-1j*wk*k) for k, hk in enumerate(h)) for wk in w])
    return w, H

filters = {
    'F1 moving avg [0.5, 0.5]': [0.5, 0.5],
    'F2 difference [0.5, -0.5]': [0.5, -0.5],
}

fig, ax = plt.subplots(figsize=(8, 5))
for label, h in filters.items():
    w, H = freq_response(h)
    ax.plot(w, np.abs(H), label=label)

ax.set_xlabel('omega (0 ~ pi)'); ax.set_ylabel('|H(e^jw)|')
ax.set_title('F1 vs F2 frequency response')
ax.legend(); ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()

# F5: ideal lowpass sinc를 rectangular window로 자른 뒤 실제 주파수응답 (Gibbs 리플 확인)
wc = np.pi/4
N = 21
n = np.arange(-(N//2), N//2+1)
h_ideal = np.where(n==0, wc/np.pi, np.sin(wc*n)/(np.pi*n))
w, H = freq_response(np.roll(h_ideal, -(N//2)))  # causal shift
plt.figure(figsize=(8,5))
plt.plot(w, np.abs(H))
plt.axvline(wc, color='gray', linestyle=':', label='cutoff wc')
plt.title(f'Windowed ideal lowpass (N={N}) — Gibbs ripple 확인')
plt.legend(); plt.grid(True, alpha=0.4)
plt.show()
