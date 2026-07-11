import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# I1: 1-pole IIR vs FIR moving average — 손계산 |H(1)|=1, |H(-1)|=1/19 확인
w, H_iir = signal.freqz([0.1], [1, -0.9])
w, H_fir = signal.freqz([0.5, 0.5], [1])
print('I1: |H| at w=0 =', abs(H_iir[0]), '(손계산 1)')
print('I1: |H| at w=pi ~', abs(H_iir[-1]), '(손계산 1/19 =', 1/19, ')')
axes[0, 0].plot(w, np.abs(H_iir), label='IIR: 0.1/(1-0.9z^-1)')
axes[0, 0].plot(w, np.abs(H_fir), label='FIR: [0.5, 0.5]')
axes[0, 0].set_title('I1: 1-pole IIR vs 2-tap FIR')
axes[0, 0].set_xlabel('omega (0 ~ pi)'); axes[0, 0].set_ylabel('|H(e^jw)|')
axes[0, 0].legend(); axes[0, 0].grid(True, alpha=0.4)

# I2: resonator — pole 반지름 바꿔가며 (angle -> peak 주파수, magnitude -> 높이·날카로움)
for r in [0.9, 0.95, 0.99]:
    p = r * np.exp(1j * np.pi / 4)
    a = np.real(np.poly([p, np.conj(p)]))  # 켤레쌍 -> 실계수 (I2c)
    w, H = signal.freqz([1], a)
    axes[0, 1].plot(w, np.abs(H), label=f'r={r}')
axes[0, 1].axvline(np.pi / 4, color='gray', ls=':', label='pole angle pi/4')
axes[0, 1].set_title('I2: pole radius vs resonance sharpness')
axes[0, 1].set_xlabel('omega (0 ~ pi)'); axes[0, 1].set_ylabel('|H(e^jw)|')
axes[0, 1].legend(); axes[0, 1].grid(True, alpha=0.4)

# I4: Butterworth 차수별 — 통과대역은 더 평평, 차단대역은 더 가파르게, Omega=1은 항상 -3dB
Omega = np.linspace(0, 3, 300)
for N in [1, 2, 4, 8]:
    axes[1, 0].plot(Omega, 1 / np.sqrt(1 + Omega**(2 * N)), label=f'N={N}')
axes[1, 0].axvline(1, color='gray', ls=':')
axes[1, 0].axhline(1 / np.sqrt(2), color='gray', ls=':', label='-3dB')
axes[1, 0].set_title('I4: Butterworth order (maximally flat)')
axes[1, 0].set_xlabel('Omega (analog freq)'); axes[1, 0].set_ylabel('|H(jOmega)|')
axes[1, 0].legend(); axes[1, 0].grid(True, alpha=0.4)

# I5: 손 유도 H(z) = (1+z^-1)/2 vs scipy.signal.bilinear
b_d, a_d = signal.bilinear([1], [1, 1], fs=0.5)  # T=2 (fs=1/T)
print('I5: bilinear 분자 =', b_d, '(손 유도 [0.5, 0.5])')
print('I5: bilinear 분모 =', a_d, '(손 유도 [1, 0] — pole이 원점 = FIR)')
w, H_d = signal.freqz(b_d, a_d)
Om = np.tan(w / 2)  # warping: 디지털 w를 아날로그 Omega로 되돌려 비교
axes[1, 1].plot(w, np.abs(H_d), label='digital (bilinear)')
axes[1, 1].plot(w, 1 / np.sqrt(1 + Om**2), '--', label='analog |H(j tan(w/2))|')
axes[1, 1].set_title('I5: analog vs digital (matches incl. warping)')
axes[1, 1].set_xlabel('omega (0 ~ pi)'); axes[1, 1].set_ylabel('|H|')
axes[1, 1].legend(); axes[1, 1].grid(True, alpha=0.4)

plt.tight_layout()
plt.show()
