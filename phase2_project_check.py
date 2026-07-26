"""Phase 2 프로젝트 — M3/M4 검증 (2026-07-25, 실행 대행분)

M3: pole placement로 구한 게인의 step 응답. PID / PI-D / I-PD 세 구조 비교
M4: L = C*G의 Bode와 Nyquist, 마진

M5(노이즈)부터는 사용자 구현.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 설계용 모델 G = 100/(s(s+10)),  사양 zeta=0.6, wn=13.3, p=40
Kp, Ki, Kd = 8.1529, 70.756, 0.4596

den = [1, 10 + 100 * Kd, 100 * Kp, 100 * Ki]     # s^3 + (10+100Kd)s^2 + 100Kp s + 100Ki

structures = [
    ("PID   (D on error)",     [100 * Kd, 100 * Kp, 100 * Ki]),
    ("PI-D  (D on meas.)",     [100 * Kp, 100 * Ki]),
    ("I-PD  (P,D on meas.)",   [100 * Ki]),
]

# ---------- M3: 세 구조의 step 응답 ----------
t = np.linspace(0, 1.4, 7000)
plt.figure(figsize=(9, 4.5))
print("=== M3  같은 pole, 다른 분자 ===")
for label, num in structures:
    _, y = signal.step(signal.TransferFunction(num, den), T=t)
    os = max(0.0, (y.max() - 1) * 100)
    idx = np.where(np.abs(y - 1) > 0.02)[0]
    ts = t[idx[-1]] if len(idx) else 0.0
    z = np.roots(num) if len(num) > 1 else np.array([])
    ok = "PASS" if os <= 10 and ts <= 0.5 else "FAIL"
    print(f"{label:22s} OS={os:5.1f}%  ts={ts:.3f}s  zeros={np.round(z,2) if z.size else 'none'}   {ok}")
    plt.plot(t, y, lw=1.8, label=f"{label}   OS {os:.1f}%, ts {ts:.2f}s")

print("\npole (세 구조 동일):", np.round(np.roots(den), 3))

# 외란 응답 Y/D = G/(1+CG) — setpoint weighting과 무관함을 확인
_, yd = signal.step(signal.TransferFunction([100, 0], den), T=t)
print(f"외란 step: 최대 편차 {np.abs(yd).max():.4f} rad,  y(inf) = {yd[-1]:+.2e}  (세 구조 동일)")

plt.axhline(1, color="k", ls=":", lw=0.8)
plt.axhline(1.10, color="r", ls="--", lw=1, label="spec 10%")
plt.axvline(0.5, color="r", ls="--", lw=1, label="spec 0.5s")
plt.xlabel("t [s]"); plt.ylabel("y"); plt.legend(fontsize=8); plt.grid(alpha=0.3)
plt.title("M3 - PID vs PI-D vs I-PD (identical poles, different numerators)")
plt.tight_layout()

# ---------- M4: 마진 ----------
Lnum, Lden = [100 * Kd, 100 * Kp, 100 * Ki], [1, 10, 0, 0]
w = np.logspace(-2, 4, 400000)
s = 1j * w
L = np.polyval(Lnum, s) / np.polyval(Lden, s)
mag, ph = np.abs(L), np.unwrap(np.angle(L)) * 180 / np.pi

i = np.where(np.diff(np.sign(mag - 1)))[0]
w_gc = np.interp(0, [mag[i[0] + 1] - 1, mag[i[0]] - 1], [w[i[0] + 1], w[i[0]]])
pm = 180 + np.interp(w_gc, w, ph)
crossings = np.where(np.diff(np.sign(ph + 180)))[0]
vm = np.min(np.abs(1 + L))

print("\n=== M4  L = C*G 의 마진 ===")
print(f"w_gc = {w_gc:.2f} rad/s   PM = {pm:.1f} deg   (사양 >= 45)")
print(f"phase: w->0 에서 {ph[0]:.2f} deg,  w->inf 에서 {ph[-1]:.2f} deg   (적분기 2개 = type 2)")
print(f"-180 교차(w>0): {'없음 -> GM = inf' if len(crossings)==0 else w[crossings]}")
print(f"vector margin = {vm:.3f}   (권장 >= 0.5)")

# w_gc에서의 위상 장부
z_at = Lnum[0] * (1j * w_gc) ** 2 + Lnum[1] * (1j * w_gc) + Lnum[2]
print(f"\nw_gc={w_gc:.1f}에서 위상 장부:")
print(f"  1/s^2      : -180.0 deg")
print(f"  1/(s+10)   : {-np.degrees(np.arctan(w_gc/10)):+.1f} deg")
print(f"  zero 2개   : {np.degrees(np.angle(z_at)):+.1f} deg")
print(f"  합계       : {ph[np.argmin(np.abs(w-w_gc))]:.1f} deg  ->  PM = {pm:.1f}")

fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
ax[0].semilogx(w, 20 * np.log10(mag), lw=1.8)
ax[0].axhline(0, color="k", ls=":", lw=0.8)
ax[0].plot(w_gc, 0, "ro", ms=7, label=f"w_gc = {w_gc:.1f}")
ax[0].set_ylabel("mag [dB]"); ax[0].set_ylim(-60, 120)
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3, which="both")
ax[0].set_title("M4 - Bode of L = C*G   (type-2: phase starts at -180)")
ax[1].semilogx(w, ph, lw=1.8)
ax[1].axhline(-180, color="r", ls=":", lw=1)
ax[1].plot(w_gc, pm - 180, "ro", ms=7)
ax[1].annotate(f"PM = {pm:.1f} deg", xy=(w_gc, pm - 180), xytext=(w_gc * 2, -160),
               arrowprops=dict(arrowstyle="->"))
ax[1].set_ylabel("phase [deg]"); ax[1].set_xlabel("w [rad/s]"); ax[1].set_ylim(-200, -60)
ax[1].grid(alpha=0.3, which="both")
plt.tight_layout()

plt.figure(figsize=(6, 6))
plt.plot(L.real, L.imag, lw=1.5)
plt.plot(L.real, -L.imag, lw=1.5, color="C0", alpha=0.35)
plt.plot(-1, 0, "rx", ms=12, mew=2, label="-1")
th = np.linspace(0, 2 * np.pi, 200)
plt.plot(-1 + vm * np.cos(th), vm * np.sin(th), "r--", lw=1, label=f"vector margin = {vm:.2f}")
plt.plot(np.cos(th), np.sin(th), "k:", lw=0.8, label="|L| = 1")
plt.xlim(-3, 3); plt.ylim(-3, 3); plt.gca().set_aspect("equal")
plt.grid(alpha=0.3); plt.legend(fontsize=8); plt.title("M4 - Nyquist")
plt.tight_layout()

plt.show()
