"""Phase 0 - Session B: frequency response verification.

Plots |H(e^jw)| for the five filters from phase0-freqresponse-problems.md
and overlays the hand-computed H(0), H(pi) values as dots so they can be
checked against the curves.

Run:  python phase0_freqresponse_check.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# filter name -> (coefficients, hand-computed (H(0), |H(pi)|))
filters = {
    'B1 moving avg [0.5, 0.5]':    ([0.5, 0.5],        (1, 0)),
    'B2 difference [0.5, -0.5]':   ([0.5, -0.5],       (0, 1)),
    'B3 3-pt avg [1/3, 1/3, 1/3]': ([1/3, 1/3, 1/3],   (1, 1/3)),
    'B4 [0.25, 0.5, 0.25]':        ([0.25, 0.5, 0.25], (1, 0)),
    'B5 [1, 0, -1]':               ([1, 0, -1],        (0, 0)),
}

fig, ax = plt.subplots(figsize=(9, 5))
for name, (b, (h0, hpi)) in filters.items():
    w, h = freqz(b, worN=1024)
    line, = ax.plot(w, np.abs(h), label=name)
    # hand-computed endpoint values as dots (should sit on the curve ends)
    ax.plot([0, np.pi], [h0, hpi], 'o', color=line.get_color())

ax.set_xlabel('w (rad/sample)')
ax.set_ylabel('|H|')
ax.set_title('Session B filters - dots = hand-computed H(0), H(pi)')
ax.set_xticks([0, np.pi/2, 2*np.pi/3, np.pi],
              ['0', 'pi/2', '2pi/3', 'pi'])
ax.grid(True, alpha=0.4)
ax.legend()
plt.tight_layout()
plt.show()
