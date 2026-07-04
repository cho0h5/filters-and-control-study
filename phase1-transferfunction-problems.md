# Phase 1 — Session 2: 전달함수 H(s)

> 목표: "입력이 있는" 시스템에서 H(s) = Y(s)/X(s)를 정의하고, 이걸로
> 자연응답(natural response)과 강제응답(forced response)을 분리해서 읽는 눈을 기른다.
> 선행: phase1-laplace-problems.md (L1~L5, pole/ROC/좌우반평면 개념)

## 도구 정리

**Session 1에서 다룬 것**: ẏ + 2y = **0** (입력 없음, IC만 있음) → 이건 "자연응답"만 있는 특수 케이스였다.

**이번엔 입력이 있는 경우**:

```
ẏ + a·y = b·x(t),   y(0) = y₀
```

양변에 Laplace, L4 성질 적용:

```
s·Y(s) − y₀ + a·Y(s) = b·X(s)
(s + a)·Y(s) = b·X(s) + y₀
Y(s) = ──────b·X(s)────── + ────y₀────
        (s + a)              (s + a)
       ─────┬─────          ────┬────
      forced response      natural response
      (입력에서 옴)          (IC에서 옴, Session 1의 그 항)
```

**전달함수의 정의**: IC = 0(y₀ = 0)이라고 놓았을 때 남는 **입력→출력 배율**:

```
H(s) := Y(s)/X(s)  (y₀ = 0일 때)  =  b / (s + a)
```

H(s)는 **시스템 고유의 값**이다 — 무슨 입력을 넣든 안 바뀐다. 입력을 바꾸면 X(s)만 바뀌고, Y(s) = H(s)·X(s)로 곱해서 출력이 나온다.

**Phase 0과의 연결**: Session A에서 풀던 y_h(homogeneous)와 y_p(particular)가 사실 이것의 재탕이다.
- natural response(y₀ 항) ↔ y_h의 역할 (시스템 고유 감쇠, pole = −a)
- forced response(X(s) 항) ↔ y_p를 향해 시스템이 끌려가는 과정

> 표기: ✍️ = 내가 쓴 답 그대로 / 💬 = Claude가 덧붙인 해설·교정

## 문제

### ✅ T1. 위 유도를 스스로 한 번 더: ẏ + 2y = x(t), y(0) = 0 (IC 없는 순수 버전) — 전부 자력

- ✍️ 양변 Laplace, L4 적용: Y(s) = X(s)/(s+2)
- ✍️ H(s) = Y(s)/X(s) = 1/(s+2)
- ✍️ pole = −2, L5(ẏ+2y=0, y(0)=3)의 pole과 "같음, 입력의 유무 차이만 있고 시스템은 같아서" —
  이유 설명까지 정확 (좌변 ẏ+2y 구조가 시스템을 정의하고, pole은 그 구조에서만 나옴 — 입력·IC는 우변/상수항일 뿐)
- 후속 질문 스레드: "왜 H=Y/X?" → LTI의 convolution 정리(Y=H·X가 입력 무관 항상 성립)로 해설 /
  "LTI라서?" → 정확, linear+time-invariant 각각의 역할 해설 /
  "모든 LTI가 H(s)로 고유 표현?" → 대체로 그렇다, 단서: IC=0(relaxed) + ROC 명시 필요, 순수지연 H(s)=e^(−sT)는 pole/zero 없는 예외 /
  "H(s)가 pole·zero 정보를 다 담고있나?" → 유리함수라면 H(s) ↔ {pole,zero,K} 동치 /
  "같은 H(s)에 ROC이 다를 수 있나?" → 가능, pole 2개 예제(−1,2)로 causal-불안정/anti-causal/사이(non-causal-안정) 3갈래 확인

### ✅ T2. 실전: 위 시스템에 x(t) = u(t) (unit step) 입력, y(0) = 0 — 전부 자력

- ✍️ X(s) = 1/s (L2 재사용)
- ✍️ Y(s) = H(s)·X(s) = 1/[s(s+2)]
- ✍️ 부분분수분해: A = 1/2, B = −1/2
  - 💬 표기: "1/2s"는 (1/2)/s와 1/(2s) 중 헷갈릴 수 있음(값은 같음) — 손 계산 시 `(1/2)/s`처럼 괄호로 명시하는 습관 권장 (T-이전 "3/s+2" 지적과 같은 패턴)
- ✍️ y(t) = (1/2)u(t) − (1/2)e^(−2t), inverse 정확
- ✍️ steady-state = (1/2)u(t), transient = −(1/2)e^(−2t)
  - 💬 확인: transient 항의 pole(−2)은 **시스템의 pole**(H(s)의 pole, T1에서 구한 그것), steady-state 항의 pole(0)은
    **입력의 pole**(step의 pole). 부분분수분해가 자동으로 "시스템 고유 성분"과 "입력이 강제한 성분"을 분리해준다

### ✅ T3. 표준형과 시정수(time constant) — 전부 자력

1차 시스템의 표준형: `τ·ẏ + y = K·x(t)` (τ, K는 상수)

- ✍️ 표준형: τ = 1/2, K = 1/2
- ✍️ pole 일치 확인: "같음" (−1/τ = −1/(1/2) = −2, T1의 pole과 일치)
- ✍️ 개념: "가까워짐. 천천히 감쇠하지" — τ=10 → pole=−0.1, 원점에 바짝 붙어 느리게 감쇠.
  **τ 크다 = pole이 원점에 가깝다 = 느린 시스템**, 이 삼단 대응이 이 세션의 핵심 결론

### ✅ T4. 정착 시간(settling time)과 pole의 관계 — 계산 "/e" 오기 자가교정 후 완료

y(t)의 transient 항은 e^(−t/τ) 꼴이다 (T2, T3 결과에서 확인 가능).

- ✍️ t=τ: "e^(-1) / e * 100 %" → 💬 **❌** (여분의 "/e") → ✍️ 원인 자가진단: "0넣어서 e 나오는거로 실수했어" —
  e^0을 **e**로 착각(맞으려면 **1**). e^(−t/τ)는 t=0일 때 이미 e^0=1(=100%)로 정규화되어 있어 나눌 필요 자체가 없었음
  → 정정: **e^(−1) × 100% ≈ 36.8%**
- ✍️ t=5τ: 같은 원인으로 같은 오기 → 정정: **e^(−5) × 100% ≈ 0.67%** —
  1% 미만이라 "사실상 다 죽었다"고 치는 게 "5τ = 정착 완료" 관례의 근거
- ✍️ pole이 더 왼쪽(τ 작음) → "빨라져" — 정확. τ 작을수록 e^(−t/τ)의 감쇠가 빠름

## Python 검증 (다 푼 뒤)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

taus = [0.5, 1, 2, 5]   # 여러 시정수 비교
fig, ax = plt.subplots(figsize=(8, 5))
for tau in taus:
    K = 1
    num = [K]
    den = [tau, 1]          # tau*s + 1
    sys = signal.TransferFunction(num, den)
    t, y = signal.step(sys)
    ax.plot(t, y, label=f'tau={tau}  (pole={-1/tau:.2f})')

ax.axhline(1, color='gray', linestyle=':', linewidth=1)
ax.axhline(1 - np.exp(-1), color='gray', linestyle='--', linewidth=1, label='63% (t=tau)')
ax.set_xlabel('t'); ax.set_ylabel('y(t)')
ax.set_title('1st-order step response — tau bigger = pole closer to origin = slower')
ax.legend(); ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()
```

T3, T4에서 손으로 구한 %와 그래프의 63%, 5τ 지점이 일치하는지 확인할 것.
