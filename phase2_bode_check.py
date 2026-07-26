"""Phase 2 Session 3 — Bode, 안정 여유, root locus 검증

Fig 1: D2/D3  L = 8/(s(s+2))의 Bode. 손 점근선 vs 실제 곡선, w_gc와 PM 표시
Fig 2: D4     지연 T를 늘려가며 phase가 내려앉는 모습 + step 응답
Fig 3: D1/D4  Nyquist — GM, PM, vector margin이 한 그림에서 보이는 것
Fig 4: D5/D6  root locus 두 개 (pole 2개 vs 3개)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

DEG = 180.0 / np.pi


def margins(num, den, delay=0.0):
    """w_gc, PM, w_pc, GM을 수치로 계산. delay는 순수 지연 T [s]."""
    w = np.logspace(-2, 3, 200000)
    s = 1j * w
    L = np.polyval(num, s) / np.polyval(den, s) * np.exp(-s * delay)
    mag, ph = np.abs(L), np.unwrap(np.angle(L)) * DEG

    # gain crossover: |L| = 1
    i = np.where(np.diff(np.sign(mag - 1.0)))[0]
    w_gc = np.interp(0, [mag[i[0] + 1] - 1, mag[i[0]] - 1], [w[i[0] + 1], w[i[0]]]) if len(i) else np.nan
    pm = 180 + np.interp(w_gc, w, ph) if len(i) else np.nan

    # phase crossover: ∠L = -180
    j = np.where(np.diff(np.sign(ph + 180.0)))[0]
    if len(j):
        w_pc = np.interp(-180, [ph[j[0]], ph[j[0] + 1]], [w[j[0]], w[j[0] + 1]])
        gm_db = -20 * np.log10(np.interp(w_pc, w, mag))
    else:
        w_pc, gm_db = np.nan, np.inf

    vm = np.min(np.abs(1 + L))       # vector margin = -1까지 최단거리
    return w_gc, pm, w_pc, gm_db, vm, w, mag, ph


# ================= Fig 1 : D2/D3 =================
num, den = [8.0], [1.0, 2.0, 0.0]          # L = 8/(s^2+2s) = 8/(s(s+2))
w_gc, pm, w_pc, gm_db, vm, w, mag, ph = margins(num, den)

print("=== D2/D3  L = 8/(s(s+2)) ===")
print(f"손계산:  w_gc = 2.5      PM = 38.7 deg    GM = inf")
print(f"실측:    w_gc = {w_gc:.4f}   PM = {pm:.2f} deg   GM = {gm_db:.1f} dB")
print(f"         vector margin = {vm:.4f}   (=1/max|S|, -1까지 최단거리)")
print(f"         zeta ~ PM/100 = {pm/100:.3f}   vs  손계산 1/sqrt(8) = {1/np.sqrt(8):.3f}")

fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
ax[0].semilogx(w, 20 * np.log10(mag), lw=2, label="exact")
# 손 점근선: w<2 는 -20dB/dec, w>2 는 -40dB/dec
wa = np.array([0.1, 2.0]); ax[0].semilogx(wa, 20*np.log10(8/(wa*2)), "r--", lw=1, label="asymptote -20dB/dec")
wb = np.array([2.0, 100.0]); ax[0].semilogx(wb, 20*np.log10(8/wb**2), "g--", lw=1, label="asymptote -40dB/dec")
ax[0].axhline(0, color="k", ls=":", lw=0.8)
ax[0].axvline(2, color="gray", ls=":", lw=0.8)
ax[0].plot(w_gc, 0, "ro", ms=7, label=f"w_gc = {w_gc:.2f}")
ax[0].set_ylabel("magnitude [dB]"); ax[0].set_ylim(-60, 50)
ax[0].set_title("Fig 1 - Bode of L = 8/(s(s+2))   corner at w=2")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3, which="both")

ax[1].semilogx(w, ph, lw=2)
ax[1].axhline(-180, color="r", ls=":", lw=1)
ax[1].axvline(2, color="gray", ls=":", lw=0.8)
ax[1].plot(w_gc, pm - 180, "ro", ms=7)
ax[1].annotate(f"PM = {pm:.1f} deg", xy=(w_gc, pm - 180), xytext=(w_gc * 1.4, -100),
               arrowprops=dict(arrowstyle="->", lw=1))
ax[1].set_ylabel("phase [deg]"); ax[1].set_xlabel("w [rad/s]"); ax[1].set_ylim(-200, -80)
ax[1].grid(alpha=0.3, which="both")
plt.tight_layout()

# ================= Fig 2 : D4 지연 =================
print("\n=== D4  지연이 먹는 PM  (w_gc x T) ===")
delays = [0.0, 0.05, 0.15, 0.27]
fig2, ax2 = plt.subplots(1, 2, figsize=(11, 4))
t = np.linspace(0, 12, 4000)
for T in delays:
    wg, p, _, _, v, ww, mm, pp = margins(num, den, delay=T)
    print(f"T = {T*1000:5.0f} ms  ->  w_gc = {wg:.3f}   PM = {p:6.2f} deg   VM = {v:.3f}")
    ax2[0].semilogx(ww, pp, lw=1.5, label=f"T = {T*1000:.0f} ms  (PM {p:.1f})")
    # Pade 1차 근사로 step 응답
    if T == 0:
        Ld_num, Ld_den = num, den
    else:
        Ld_num = np.polymul(num, [-T / 2, 1.0])
        Ld_den = np.polymul(den, [T / 2, 1.0])
    Tcl = signal.TransferFunction(Ld_num, np.polyadd(Ld_den, Ld_num))
    _, y = signal.step(Tcl, T=t)
    ax2[1].plot(t, y, lw=1.2, label=f"T = {T*1000:.0f} ms")

ax2[0].axhline(-180, color="r", ls=":", lw=1)
ax2[0].set_xlabel("w [rad/s]"); ax2[0].set_ylabel("phase [deg]"); ax2[0].set_ylim(-300, -80)
ax2[0].set_title("Fig 2a - delay eats phase only (magnitude unchanged)")
ax2[0].legend(fontsize=8); ax2[0].grid(alpha=0.3, which="both")
ax2[1].axhline(1, color="k", ls=":", lw=0.8)
ax2[1].set_xlabel("t [s]"); ax2[1].set_ylabel("y")
ax2[1].set_title("Fig 2b - step response (Pade approx)")
ax2[1].legend(fontsize=8); ax2[1].grid(alpha=0.3)
plt.tight_layout()

# ================= Fig 3 : Nyquist =================
wn_ = np.logspace(-1, 3, 20000)
Ln = np.polyval(num, 1j * wn_) / np.polyval(den, 1j * wn_)
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.plot(Ln.real, Ln.imag, lw=1.5)
ax3.plot(Ln.real, -Ln.imag, lw=1.5, color="C0", alpha=0.4)
ax3.plot(-1, 0, "rx", ms=12, mew=2, label="-1 point")
th = np.linspace(0, 2 * np.pi, 200)
ax3.plot(-1 + vm * np.cos(th), vm * np.sin(th), "r--", lw=1, label=f"vector margin = {vm:.3f}")
ax3.plot(np.cos(th), np.sin(th), "k:", lw=0.8, label="|L| = 1")
ax3.set_xlim(-3, 1); ax3.set_ylim(-2, 2); ax3.set_aspect("equal")
ax3.set_xlabel("Re"); ax3.set_ylabel("Im"); ax3.grid(alpha=0.3)
ax3.set_title("Fig 3 - Nyquist: distance to -1 is what actually matters")
ax3.legend(fontsize=8)

# ================= Fig 4 : root locus =================
def locus(poles, Kmax, n=4000):
    Ks = np.linspace(1e-6, Kmax, n)
    base = np.poly(poles)
    return Ks, np.array([np.roots(np.polyadd(base, [K])) for K in Ks])

fig4, ax4 = plt.subplots(1, 2, figsize=(11, 5))
for a, (poles, Kmax, title) in zip(ax4, [
    ([0, -2], 120, "G = 1/(s(s+2))     n-m=2, asymptote 90 deg"),
    ([0, -2, -10], 600, "G = 1/(s(s+2)(s+10))   n-m=3, asymptote 60 deg"),
]):
    Ks, R = locus(poles, Kmax)
    for k in range(R.shape[1]):
        a.plot(R[:, k].real, R[:, k].imag, ".", ms=1, color="C0")
    a.plot(np.real(poles), np.imag(poles), "kx", ms=10, mew=2, label="open-loop poles")
    a.axvline(0, color="r", ls="--", lw=1)
    a.axhline(0, color="k", lw=0.5)
    a.set_title(title, fontsize=10); a.set_xlabel("Re"); a.set_ylabel("Im")
    a.grid(alpha=0.3); a.legend(fontsize=8)
ax4[1].plot([0, 0], [np.sqrt(20), -np.sqrt(20)], "ro", ms=7,
            label=f"crossing at K=240, w={np.sqrt(20):.2f}")
ax4[1].legend(fontsize=8)

# D5 검증
print("\n=== D5  1/(s(s+2)(s+10)) 안정 한계 ===")
for K in [200, 240, 280]:
    r = np.roots([1, 12, 20, K])
    print(f"K = {K:3d}  ->  roots = {np.round(r, 3)}   max Re = {r.real.max():+.3f}"
          f"   {'stable' if r.real.max() < 0 else 'UNSTABLE'}")

plt.tight_layout()
plt.show()
