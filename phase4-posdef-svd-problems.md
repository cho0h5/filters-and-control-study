# Phase 4 Session 4 — 양의 정부호 · SVD · 그래디언트 (마무리)

> 목표: Phase 5·6·7에서 쓸 세 조각을 짧게 장착한다. 셋 다 앞 세션에 고리가 이미 걸려 있다 —
> 양의 정부호는 Session 2(eigenvalue), SVD는 Session 1(rank)·3($A^TA$), 그래디언트는 Session 3(내적).
> 선행: Session 1~3

## ✅ ① 양의 정부호 (positive definite)

Session 2의 $A$를 재사용:

$$
A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}, \qquad
\lambda = 3,\ 1, \qquad
\mathbf{v} = (1,1),\ (1,-1)
$$

새 연산: 벡터를 **양쪽에서** 곱하면 결과가 행렬이 아니라 **숫자 하나**가 된다.

- ✍️ $\mathbf{x} = (1,1)$: $\mathbf{x}^TA\mathbf{x} = (1,1)\cdot(3,3) = 6$ 자력
- ✍️ $\mathbf{x} = (1,-1)$: $\mathbf{x}^TA\mathbf{x} = 2$ 자력
- ✍️ **"$\lvert x \rvert^2 \cdot \lambda$야?"** 자력 — eigenvector에서는 $\mathbf{x}^TA\mathbf{x} = \lambda\lvert\mathbf{x}\rvert^2$

eigenvector가 아닌 일반 $\mathbf{x}$도 Session 2처럼 쪼개면:

$$
\mathbf{x} = c_1(1,1) + c_2(1,-1)
\;\Longrightarrow\;
\mathbf{x}^TA\mathbf{x} = 3c_1^2\cdot 2 + 1c_2^2 \cdot 2
$$

**제곱은 부호를 못 바꾸므로 $\mathbf{x}^TA\mathbf{x}$의 부호는 오직 $\lambda$들이 정한다.**

| | 조건 | 이름 |
|---|---|---|
| 모든 $\lambda > 0$ | 모든 $\mathbf{x}\ne0$에서 $\mathbf{x}^TA\mathbf{x} > 0$ | 양의 정부호 (positive definite) |
| 모든 $\lambda \ge 0$ | $\mathbf{x}^TA\mathbf{x} \ge 0$ | 양의 준정부호 (semi-definite) |

### 왜 필요한가

$$
\text{LQR 비용} \quad J = \int (\mathbf{x}^TQ\mathbf{x} + \mathbf{u}^TR\mathbf{u})\,dt
$$

$Q$, $R$이 양의 정부호가 아니면 **비용이 음수가 될 수 있고**, 그러면 최적화가
"상태를 저쪽으로 보내면 비용을 벌 수 있다"는 헛소리를 한다. 비용은 언제나 벌점이어야 한다.

**공분산 행렬도 항상 양의 준정부호** — $\mathbf{x}^T\Sigma\mathbf{x}$가 그 방향으로 잰 분산인데
분산이 음수일 수 없으므로. Phase 6에서 재등장.

## ✅ ② SVD — 개념만

대각화에는 제약이 있었다(정사각 + eigenvector가 충분할 것). Session 3의 $3\times2$ 행렬은
대각화 자체가 말이 안 된다. SVD는 그 제약을 없앤 버전:

$$
\text{대각화}: A = PDP^{-1} \quad(\text{정사각 + 조건}) \qquad
\text{SVD}: A = U\Sigma V^T \quad(\text{아무 행렬이나, 항상 존재})
$$

읽는 법은 대각화와 같이 **오른쪽부터**:

| | 하는 일 |
|---|---|
| $V^T$ | 회전 (입력 쪽에서 좋은 방향으로 돌려놓고) |
| $\Sigma$ | 늘이기 (각 축마다 $\sigma_i$배 — 대각행렬) |
| $U$ | 회전 (출력 쪽 방향으로 돌려놓는다) |

> **모든 행렬은 "돌리고 → 늘이고 → 돌리기"다.** $\sigma_i$를 **특이값**(singular value)이라 하고
> $\lambda$ 자리를 대신한다.

### ✍️ **"$\sigma_i$는 어디서 나온 거야?"** — 답은 Session 3에서 이미 나온 물건

$A$가 정사각형이 아니어도 $A^TA$는 **항상 정사각형**이다(최소제곱에서 $3\times2$로 $2\times2$를 만든 그것):

$$
\sigma_i = \sqrt{A^TA \text{의 eigenvalue}}
$$

**제곱근이 항상 실수인 이유**는 $A^TA$가 양의 준정부호이기 때문 — ①로 한 줄 증명이 된다:

$$
\mathbf{x}^T(A^TA)\mathbf{x} = (A\mathbf{x})^T(A\mathbf{x}) = \lVert A\mathbf{x}\rVert^2 \ge 0
$$

$A^TA$를 양쪽에서 조이면 그냥 **$A\mathbf{x}$의 길이 제곱**이 된다. 길이 제곱은 음수가 될 수 없다.

$V$의 열은 $A^TA$의 eigenvector, $U$의 열은 $AA^T$의 eigenvector.
**SVD는 대각화를 비정사각 행렬로 밀어 넣기 위해 $A^TA$를 경유하는 장치.**

### 0이 아닌 $\sigma$의 개수 = rank

- 💬 해설 필요했던 항목. 배율 $\sigma_i = 0$인 축은 그 방향을 **완전히 납작하게** 만들므로,
  살아남는 차원의 개수 = 0이 아닌 $\sigma$의 개수 = $\text{rank}$

### 실무에서 SVD를 쓰는 진짜 이유

$\det$과 $\text{rank}$는 **예/아니오**만 답한다. 실제 측정 데이터에서 $\sigma$가 정확히 0인 경우는
거의 없고 $10^{-7}$처럼 **거의** 0인 경우가 나온다.

| | 답하는 것 | |
|---|---|---|
| $\det$, $\text{rank}$ | 무너졌나 / 안 무너졌나 | 이산적 |
| $\sigma$ | 얼마나 무너지기 직전인가 | 연속적 |

가장 큰 $\sigma$와 가장 작은 $\sigma$의 비율이 **조건수**(condition number)이고,
크면 수치적으로 위태롭다는 뜻. Session 3의 $(A^TA)^{-1}$을 컴퓨터로 계산할 때 터지는 지점을
알려준다. Phase 6에서 공분산 행렬이 수치적으로 깨지는 문제가 정확히 이 얘기.

또한 rank가 무너졌을 때 쓰는 **pseudo-inverse**를 제대로 정의하는 도구가 SVD다(Session 3 말미).

## ✅ ③ 그래디언트 = 최급상승 방향

$$
\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)
$$

핵심은 **방향 도함수** — 단위벡터 $\hat{\mathbf{u}}$ 방향으로 갈 때 $f$가 변하는 속도:

$$
\hat{\mathbf{u}} \text{ 방향의 변화율} = \nabla f \cdot \hat{\mathbf{u}}
$$

- ✍️ $\theta = 0$, **같은 방향** 자력 (첫 답 "가장 기울기가 큰 방향"은 결론의 재진술이라 한 번 되물음)

$$
\nabla f \cdot \hat{\mathbf{u}} = \lVert\nabla f\rVert \cdot \lVert\hat{\mathbf{u}}\rVert \cos\theta
= \underbrace{\lVert\nabla f\rVert}_{\text{고정}} \cdot \underbrace{\cos\theta}_{\text{유일한 변수}}
$$

$$
\text{최급상승} = \nabla f \text{ 자신의 방향}, \qquad
\text{그때의 변화율} = \lVert\nabla f\rVert, \qquad
\text{최급하강} = -\nabla f
$$

> "그래디언트가 가장 가파른 방향"은 정의가 아니라 **내적에서 유도되는 결과**다.

쓰이는 곳: Phase 7 MPC의 QP 반복법, Phase 8의 MIT rule($d\theta/dt = -\gamma e\,\partial e/\partial\theta$),
Session 3의 최소제곱을 닫힌 해 대신 반복으로 풀 때.

---

## 진행 기록

| 항목 | 상태 | 메모 |
|---|---|---|
| ① 양의 정부호 | ✅ 2026-07-28 | $\mathbf{x}^TA\mathbf{x} = \lambda\lvert\mathbf{x}\rvert^2$ 자력 발견 |
| ② SVD (개념만) | ✅ 2026-07-28 | ✍️ "$\sigma_i$는 어디서 나온 거야?" — $A^TA$ 경유 구조를 이 질문이 열었음. rank 연결은 해설 |
| ③ 그래디언트 | ✅ 2026-07-28 | $\cos\theta$ 최대화로 $\theta=0$ 자력 |

**총평**: 세 조각 모두 앞 세션의 고리에 걸려 빠르게 끝남.
✍️ **"$\sigma_i$는 어디서 나온 거야?"** 가 이 세션에서 가장 값나가는 질문이었다 —
SVD를 "$A^TA$의 eigenvalue의 제곱근"으로 내려놓으면서 Session 1(rank)·2(eigenvalue)·3($A^TA$)이
한 자리에 모였고, 제곱근이 실수인 근거가 바로 앞에서 한 ①의 양의 준정부호였다.

**Phase 4 완료.** 다음: **Phase 5 — 상태공간 제어** (안정성 = A의 고유값이 Session 2에서 이미 준비됨)
