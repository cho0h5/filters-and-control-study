import numpy as np
import scipy

def make_signal(fs=100, dur=10.0, seed=0):
    """fs: 샘플링 주파수 Hz, 반환: (t, clean, noisy)"""
    rng = np.random.default_rng(seed)
    t = np.arange(0, dur, 1/fs)
    clean = (1.0*np.sin(2*np.pi*0.3*t)          # 천천히 오르내리는 고도 (0.3 Hz)
             + 0.5*np.sin(2*np.pi*0.8*t))        # 기동 성분 (0.8 Hz)
    noise = (0.4*np.sin(2*np.pi*23*t)            # 모터 진동 (23 Hz)
             + 0.3*rng.standard_normal(len(t)))  # 백색 잡음
    return t, clean, clean + noise

def my_convolve(x, h):
    y = np.zeros(len(x))
    for n in range(len(x)):

        for i in range(len(h)):
            if n - i < 0:
                continue

            y[n] += x[n - i] * h[i]

    return y

def my_iir(x, b, a):
    y = np.zeros(len(x))
    for n in range(len(x)):
        
        for i in range(len(b)):
            if n - i < 0:
                continue

            y[n] += b[i] * x[n - i]

        for i in range(1, len(a)):
            if n - i < 0:
                continue

            y[n] -= a[i] * y[n - i]

    return y

# ---------- M3: 비교 ----------
import matplotlib.pyplot as plt
from scipy import signal

t, clean, noisy = make_signal()

h = signal.firwin(51, 2, fs=100)
y_fir = my_convolve(noisy, h)

b, a = scipy.signal.butter(2, 2, fs=100)
y_iir = my_iir(noisy, b, a)

def measure_delay(y, ref):
    """출력이 ref보다 몇 샘플 늦는지 (cross-correlation 피크)"""
    c = np.correlate(y, ref, 'full')
    return np.argmax(c) - (len(ref) - 1)

def aligned_rms(y, ref, d):
    """지연 d만큼 되돌려 정렬한 뒤 잔차 RMS"""
    if d > 0:
        y, ref = y[d:], ref[:-d]
    return np.sqrt(np.mean((y - ref) ** 2))

d_fir = measure_delay(y_fir, clean)
d_iir = measure_delay(y_iir, clean)
print(f'FIR: 계수 {len(h)}개, 지연 {d_fir}샘플 (예측 25), 정렬 후 RMS {aligned_rms(y_fir, clean, d_fir):.4f}')
print(f'IIR: 계수 {len(b) + len(a) - 1}개, 지연 {d_iir}샘플, 정렬 후 RMS {aligned_rms(y_iir, clean, d_iir):.4f}')
print(f'참고: noisy 자체의 RMS(필터 전) = {np.sqrt(np.mean((noisy - clean) ** 2)):.4f}')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8))
for ax, (lo, hi) in zip((ax1, ax2), ((0, 10), (4, 6))):
    m = (t >= lo) & (t < hi)
    ax.plot(t[m], noisy[m], color='0.8', label='noisy')
    ax.plot(t[m], clean[m], 'k--', label='clean')
    ax.plot(t[m], y_fir[m], label=f'FIR 51-tap (delay {d_fir})')
    ax.plot(t[m], y_iir[m], label=f'IIR butter2 (delay {d_iir})')
    ax.set_xlabel('t (s)'); ax.set_ylabel('altitude')
    ax.legend(); ax.grid(True, alpha=0.4)
ax1.set_title('M3: full view')
ax2.set_title('M3: zoom (4~6 s)')
plt.tight_layout()
plt.show()
