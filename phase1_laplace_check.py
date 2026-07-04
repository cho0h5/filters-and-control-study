"""Phase 1 - Session 1: Laplace transform verification.

Checks the hand-derived pairs from phase1-laplace-problems.md (L1-L5)
against sympy, then plots every pole found in this session on the
s-plane (Re(s) vs Im(s)) so the "pole position <-> time behavior"
correspondence is visible, not just symbolic.

Run:  python phase1_laplace_check.py
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

t, s = sp.symbols('t s', positive=True)
a, w0 = sp.symbols('a omega0', positive=True)

print("=== L1-L3: transform pairs ===")
pairs = [
    ('L1  e^(-at)u(t)', sp.exp(-a * t), sp.Rational(1) / (s + a)),
    ('L2  u(t)',         sp.Heaviside(t), sp.Rational(1) / s),
    ('L3  cos(w0 t)u(t)', sp.cos(w0 * t), s / (s**2 + w0**2)),
]
for name, x, hand in pairs:
    sympy_X = sp.laplace_transform(x, t, s, noconds=True)
    match = sp.simplify(sympy_X - hand) == 0
    print(f"{name:22s} hand={hand}   sympy={sympy_X}   match={match}")

print("\n=== L4: differentiation property ===")
x = sp.Function('x')
X = sp.Function('X')
lhs = sp.laplace_transform(x(t).diff(t), t, s, noconds=True)
print("sympy L{x'(t)} ->", lhs, "  (compare by hand to s*X(s) - x(0))")

print("\n=== L5: ODE solved two ways ===")
y = sp.Function('y')
ode = sp.Eq(y(t).diff(t) + 2 * y(t), 0)
sol = sp.dsolve(ode, y(t), ics={y(0): 3})
print("time-domain (dsolve):", sol)

Y = sp.laplace_transform(y(t), t, s, noconds=True)  # placeholder, real work below
Ys_hand = sp.Rational(3) / (s + 2)
y_recovered = sp.inverse_laplace_transform(Ys_hand, s, t)
print("Y(s) by hand:", Ys_hand)
print("inverse_laplace_transform(Y(s)) ->", y_recovered)

# --- s-plane pole plot: every pole seen this session ---
# L1, L5 use numeric stand-ins (a=3, and the -2 from L5) since a is symbolic above.
poles = {
    'L1  -a  (e.g. a=3)': [-3 + 0j],
    'L2  u(t)':           [0 + 0j],
    'L3  cos(w0 t), w0=5': [0 + 5j, 0 - 5j],
    'L5  y\'+2y=0':        [-2 + 0j],
}

fig, ax = plt.subplots(figsize=(6, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(poles)))
for (name, pts), c in zip(poles.items(), colors):
    xs = [p.real for p in pts]
    ys = [p.imag for p in pts]
    ax.scatter(xs, ys, marker='x', s=120, linewidths=2.5, color=c, label=name)

ax.axhline(0, color='gray', linewidth=1)
ax.axvline(0, color='gray', linewidth=1)
ax.axvspan(-6, 0, color='green', alpha=0.05)
ax.axvspan(0, 6, color='red', alpha=0.05)
ax.text(-5.5, 5.5, 'left half-plane\n(decay)', color='green', fontsize=9)
ax.text(3.5, 5.5, 'right half-plane\n(growth)', color='red', fontsize=9)
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel('Re(s)  =  sigma  (decay rate)')
ax.set_ylabel('Im(s)  =  omega  (oscillation freq)')
ax.set_title('Phase 1 Session 1 - every pole on the s-plane')
ax.grid(True, alpha=0.3)
ax.legend(loc='lower left', fontsize=8)
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
