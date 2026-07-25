"""Phase 2 Session 2 — PID 검증

Fig 1: P5 네 경우(P / PI / PI강함 / PID) step response 비교
Fig 2: P3 설계 검증 — K_p=12, K_i=100이 정말 ζ=0.7, ωn=10을 만드나
Fig 3: P4 — 측정 노이즈가 있을 때 순수 D vs filtered D의 제어입력 u(t)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# plant G(s) = 1/(s+2)
G_num, G_den = [1.0], [1.0, 2.0]


def closed_loop(Kp, Ki=0.0, Kd=0.0, tau_f=0.0):
    """C(s)·G(s)를 unity feedback으로 닫은 T(s)를 반환.

    C(s) = Kp + Ki/s + Kd*s        (tau_f = 0)
         = Kp + Ki/s + Kd*s/(tau_f*s+1)  (tau_f > 0)
    """
    if tau_f == 0.0:
        # C = (Kd s^2 + Kp s + Ki) / s
        C_num = [Kd, Kp, Ki]
        C_den = [1.0, 0.0]
    else:
        # C = (Kd s)/(tau_f s+1) + Kp + Ki/s  를 통분: 분모 = s(tau_f s + 1)
        # 분자 = Kd s^2 + Kp s (tau_f s+1) + Ki (tau_f s+1)
        C_num = np.polyadd(
            np.polyadd([Kd, 0.0, 0.0], np.polymul([Kp, 0.0], [tau_f, 1.0])),
            np.polymul([Ki], [tau_f, 1.0]),
        )
        C_den = np.polymul([1.0, 0.0], [tau_f, 1.0])

    L_num = np.polymul(C_num, G_num)          # loop gain L = C*G
    L_den = np.polymul(C_den, G_den)
    T_num = L_num                              # T = L/(1+L)
    T_den = np.polyadd(L_den, L_num)
    return signal.TransferFunction(T_num, T_den)


def control_effort(Kp, Ki, Kd, tau_f, t, r, y):
    """측정 y(잡음 포함)에 대해 u(t)를 직접 적분해서 계산 (Fig 3용)."""
    dt = t[1] - t[0]
    e = r - y
    integ = 0.0
    d_state = 0.0
    u = np.zeros_like(t)
    for i in range(len(t)):
        integ += e[i] * dt
        if i == 0:
            de = 0.0
        else:
            de = (e[i] - e[i - 1]) / dt
        if tau_f > 0:                                   # 1차 저역통과로 미분값 평활
            d_state += (de - d_state) * dt / tau_f
            dterm = Kd * d_state
        else:
            dterm = Kd * de
        u[i] = Kp * e[i] + Ki * integ + dterm
    return u


# ---------- Fig 1: P5 네 경우 ----------
cases = [
    ("P    (Kp=10)",              dict(Kp=10)),
    ("PI   (Kp=10, Ki=50)",       dict(Kp=10, Ki=50)),
    ("PI   (Kp=10, Ki=200)",      dict(Kp=10, Ki=200)),
    ("PID  (Kp=10, Ki=200, Kd=1)", dict(Kp=10, Ki=200, Kd=1)),
]

t = np.linspace(0, 3, 3000)
plt.figure(figsize=(9, 5))
print("=== Fig 1 (P5) ===")
for label, gains in cases:
    T = closed_loop(**gains)
    _, y = signal.step(T, T=t)
    plt.plot(t, y, label=label)
    os = (y.max() - y[-1]) / y[-1] * 100 if y.max() > y[-1] else 0.0
    print(f"{label:28s}  y(inf)={y[-1]:.4f}  e(inf)={1-y[-1]:+.4f}  overshoot={os:5.1f}%")
plt.axhline(1.0, color="k", ls=":", lw=0.8)
plt.title("Fig 1 - P vs PI vs PI(strong I) vs PID   [plant 1/(s+2), step]")
plt.xlabel("t [s]"); plt.ylabel("y"); plt.legend(); plt.grid(alpha=0.3)

# ---------- Fig 2: P3 설계 검증 ----------
Kp3, Ki3 = 12.0, 100.0
T3 = closed_loop(Kp=Kp3, Ki=Ki3)
t2 = np.linspace(0, 1.5, 3000)
_, y3 = signal.step(T3, T=t2)

poles = np.roots(T3.den)
wn = np.abs(poles[0])
zeta = -np.real(poles[0]) / wn
os3 = (y3.max() - 1) * 100
# 2% settling time
idx = np.where(np.abs(y3 - 1) > 0.02)[0]
ts = t2[idx[-1]] if len(idx) else 0.0

print("\n=== Fig 2 (P3 설계 검증) ===")
print(f"목표:  zeta=0.700  wn=10.00")
print(f"실측:  zeta={zeta:.3f}  wn={wn:.2f}   poles={poles}")
print(f"overshoot={os3:.1f}%   2% settling={ts:.3f}s")

plt.figure(figsize=(9, 4))
plt.plot(t2, y3, label=f"PI  Kp={Kp3:g}, Ki={Ki3:g}")
plt.axhline(1.0, color="k", ls=":", lw=0.8)
plt.axhline(1.05, color="r", ls="--", lw=0.8, label="+5% (expected OS for zeta=0.7)")
plt.title("Fig 2 - P3 pole placement check (target zeta=0.7, wn=10)")
plt.xlabel("t [s]"); plt.ylabel("y"); plt.legend(); plt.grid(alpha=0.3)

# ---------- Fig 3: P4 노이즈 ----------
rng = np.random.default_rng(0)
t3 = np.linspace(0, 2, 4000)
r = np.ones_like(t3)
T_pid = closed_loop(Kp=10, Ki=200, Kd=1)
_, y_clean = signal.step(T_pid, T=t3)
y_meas = y_clean + rng.normal(0, 0.01, len(t3))     # 센서 노이즈 sigma=0.01

u_pure = control_effort(10, 200, 1.0, 0.0, t3, r, y_meas)
u_filt = control_effort(10, 200, 1.0, 0.01, t3, r, y_meas)   # tau_f = 10ms

print("\n=== Fig 3 (P4 노이즈) ===")
print(f"센서 노이즈 sigma = 0.01 (출력의 1%)")
print(f"순수 D     : u의 표준편차 = {u_pure.std():9.2f},  |u|max = {np.abs(u_pure).max():9.2f}")
print(f"filtered D : u의 표준편차 = {u_filt.std():9.2f},  |u|max = {np.abs(u_filt).max():9.2f}")

fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
ax[0].plot(t3, u_pure, lw=0.6, color="crimson")
ax[0].set_title("Fig 3 - pure derivative  Kd*s   (sensor noise sigma=0.01)")
ax[0].set_ylabel("u(t)"); ax[0].grid(alpha=0.3)
ax[1].plot(t3, u_filt, lw=0.8, color="steelblue")
ax[1].set_title("filtered derivative  Kd*s/(0.01s+1)")
ax[1].set_xlabel("t [s]"); ax[1].set_ylabel("u(t)"); ax[1].grid(alpha=0.3)
plt.tight_layout()

plt.show()
