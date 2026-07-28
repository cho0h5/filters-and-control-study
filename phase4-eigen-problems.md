# Phase 4 Session 2 — 고유벡터와 대각화

> 목표: eigenvector/eigenvalue에 이름과 절차를 붙이고, $A = PDP^{-1}$로 $A^n$·$e^{At}$가
> 왜 쉬워지는지 손으로 확인한다. 끝에서 **안정성 = eigenvalue**로 Phase 5 입구에 도달.
> 선행: Session 1(동치 사슬) — 특성방정식이 그 도구를 그대로 쓴다

$$
A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}
$$

일반 벡터 곱셈도 W0의 규칙 그대로 — **열의 조합**:

$$
M\begin{bmatrix}x\\y\end{bmatrix} = x \cdot (\text{첫째 열}) + y \cdot (\text{둘째 열})
$$

## ✅ E1~E2. eigenvector = 방향이 안 변하는 벡터

- ✍️ $A(1,1) = (3,3) = 3(1,1)$ — **방향 그대로, 크기만 3배**
- ✍️ $A(1,0) = (2,1)$ — 방향이 틀어짐
- ✍️ $A(1,-1) = (1,-1)$ — $\lambda = 1$

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

행렬이 하는 일은 보통 "회전 + 늘이기"가 섞인 것인데, eigenvector 방향에서만은 **순수한 늘이기**.

| eigenvector | $\lambda$ |
|---|---|
| $(1, 1)$ | 3 |
| $(1, -1)$ | 1 |

## ✅ E3~E4. 대각화 = 쪼개고 → 각자 늘이고 → 합치기

- ✍️ $(2,0) = 1\cdot(1,1) + 1\cdot(1,-1)$ 자력
- ✍️ 두 경로가 일치: ① eigen 경로 $3(1,1) + 1(1,-1) = (4,2)$, ② 직접 $A(2,0) = (4,2)$

$$
P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}, \qquad
D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}, \qquad
A = PDP^{-1}
$$

오른쪽부터 읽으면 손으로 밟은 순서 그대로:

| | 하는 일 | 손으로 한 것 |
|---|---|---|
| $P^{-1}$ | 원래 좌표 → eigen 좌표 (쪼개기) | E3 |
| $D$ | 각 좌표에 $\lambda$ 곱하기 | E4 ① |
| $P$ | eigen 좌표 → 원래 좌표 (합치기) | E4 ① |

> **대각화 = 이 변환이 그냥 늘이기로 보이는 기저를 찾는 것.**
> $A$가 복잡해 보인 건 $\mathbf{e}_1, \mathbf{e}_2$로 봤기 때문이고, $(1,1)\cdot(1,-1)$로 보면 숫자 두 개다.

## ✅ E5. 왜 이득인가 — 거듭제곱과 $e^{At}$

- ✍️ $A^{10}(2,0) = 3^{10}(1,1) + 1^{10}(1,-1)$ 자력

$$
A^n = P D^n P^{-1}, \qquad
D^n = \begin{bmatrix} 3^n & 0 \\ 0 & 1^n \end{bmatrix}
$$

$D$가 대각이라 **거듭제곱이 각 숫자의 거듭제곱**. 행렬 곱 10번이 곱셈 2번이 된다.

$$
e^{At} = P\,e^{Dt}\,P^{-1}, \qquad
e^{Dt} = \begin{bmatrix} e^{3t} & 0 \\ 0 & e^{1t} \end{bmatrix}
$$

$e^{At}$는 정의부터 무한급수인데, 대각화하면 **평범한 스칼라 지수 두 개**가 된다.
$3^n$은 폭발하고 $1^n$은 가만히 있으므로 시간이 지나면 $(1,1)$ 방향이 지배 —
Phase 1·2의 **dominant pole**이 eigenvalue 크기 싸움으로 나타난 것.

## ✅ 빈칸 메우기 — ✍️ **"P랑 P⁻¹은 어떻게 구하는지 안 다뤘잖아"**

사용자가 정확히 지적. eigenvector를 튜터가 건네주기만 했고 $P^{-1}$은 계산한 적이 없었음.

### 빈칸 1 — 특성방정식 (**Session 1이 회수되는 자리**)

$$
A\mathbf{v} = \lambda\mathbf{v} \;\Rightarrow\; (A - \lambda I)\mathbf{v} = 0
$$

$\mathbf{v} \ne 0$인 해가 있으려면 $(A-\lambda I)$가 **차원을 무너뜨려야** 한다
(Session 1의 $B$가 서로 다른 입력을 같은 출력으로 보낸 그 상황):

$$
0 \text{이 아닌 } \mathbf{v} \text{를 } 0 \text{으로 보낸다}
\iff \text{차원 붕괴}
\iff \det(A - \lambda I) = 0
$$

- ✍️ $(2-\lambda)^2 - 1 = 0 \Rightarrow \lambda = 3, 1$ 자력 — 건네받았던 숫자가 계산으로 나옴
- ✍️ $\lambda = 3$: $\begin{bmatrix}-1 & 1\\ 1 & -1\end{bmatrix}\mathbf{v} = 0 \Rightarrow x = y$
- ✍️ $\lambda = 1$: $x + y = 0 \Rightarrow (1,-1)$ 자력

### ✍️ **"여러 개가 존재하잖아"** — 정확한 지적

해집합은 벡터 하나가 아니라 **직선 하나 통째**. 정의가 크기에 무관하기 때문:

$$
A\mathbf{v} = \lambda\mathbf{v} \;\Rightarrow\; A(c\mathbf{v}) = c(A\mathbf{v}) = c(\lambda\mathbf{v}) = \lambda(c\mathbf{v})
$$

그래서 eigenvector는 엄밀히는 **벡터가 아니라 방향**이고, 그 직선을 **eigenspace**라 한다.
Session 1과 연결: $(A - 3I)$가 평면을 뭉갤 때 **직선 하나 전체가 0으로** 가는데, 그게 eigenspace다.
$P$에는 그 직선에서 아무거나 하나 골라 넣으면 되고($P$에서 커진 만큼 $P^{-1}$에서 되돌아옴),
관례는 ① 정수로 깔끔한 것(손계산) ② 길이 1로 정규화(수치계산·직교행렬, Phase 6에서 재등장).

### 빈칸 2 — $P^{-1}$

$$
M = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
\;\Rightarrow\;
M^{-1} = \frac{1}{\det M}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

$\det = 0$이면 나눌 수 없다 — **역행렬이 없다**가 공식에서도 그대로 보인다.

- ✍️ $\det P = -2$, $P^{-1} = \begin{bmatrix} 1/2 & 1/2 \\ 1/2 & -1/2 \end{bmatrix}$ 자력
- ✍️ $PDP^{-1} = A$ 손으로 확인 완료 (행렬곱 = 상대의 각 열에 적용)
- 💬 곁다리: $(1,1)\cdot(1,-1) = 0$ — $A$가 **대칭행렬**이라 eigenvector가 직교. Phase 6 공분산에서 재등장

## ✅ 안정성 회수 — Phase 5의 입구

해가 eigen 방향으로 쪼개지고 **각 조각이 자기 $\lambda$로만 굴러가므로**, 판단은 $\lambda$를 하나씩 보는 일이 된다:

$$
x(t) = c_1 e^{3t}(1,1) + c_2 e^{1t}(1,-1), \qquad
x[n] = c_1 3^n (1,1) + c_2 1^n (1,-1)
$$

> **하나라도 조건을 어기면 불안정.** 터지는 조각 하나가 결국 전체를 지배한다.

| | 연속시간 $(s, \lambda)$ | 이산시간 $(z, \lambda)$ |
|---|---|---|
| 해의 모양 | $e^{\lambda t}$ | $\lambda^n$ |
| 안정 | $\text{Re}(\lambda) < 0$ | $\lvert\lambda\rvert < 1$ |
| 경계 | $\text{Re}(\lambda) = 0$ (허수축) | $\lvert\lambda\rvert = 1$ (단위원) |
| 불안정 | $\text{Re}(\lambda) > 0$ | $\lvert\lambda\rvert > 1$ |
| **"아무것도 안 함"** | $\lambda = 0$ | $\lambda = 1$ |

**상태공간에서 $A$의 eigenvalue가 곧 그 pole이다.** Phase 1의 전달함수 분모 근, Phase 3의 단위원 안팎이
여기서 하나로 합쳐진다.

- ⚠️ **연속/이산 혼동 재발** — $\lambda = 1$을 "유지"로 답함. 이산에서는 맞지만 연속에서는
  $e^{1t} = e^t$로 **이미 폭발**. Phase 3 I4에서 $s = -1$을 "부호 반전"으로 읽은 것과 **같은 패턴**.
  미니 테스트($t = 0, 1, 10$에서 $e^t$ vs $1^n$)로 자가 교정. 위 표의 맨 아랫줄이 함정 지점
- ✍️ 최종 판정: 연속·이산 **둘 다 불안정** (연속은 두 $\lambda$ 모두 위반, 이산은 $\lambda=3$ 하나로 위반)

---

## 진행 기록

| 항목 | 상태 | 메모 |
|---|---|---|
| E1~E2 eigenvector | ✅ 2026-07-28 | "방향 그대로, 크기만" 자력 |
| E3~E4 대각화 $PDP^{-1}$ | ✅ 2026-07-28 | 두 경로 일치를 손으로 확인 |
| E5 $A^n$, $e^{At}$ | ✅ 2026-07-28 | $3^{10}$ vs $1^{10}$ → dominant 방향 |
| 특성방정식, $P^{-1}$ | ✅ 2026-07-28 | **사용자가 빈칸을 스스로 지적해서 메움**. eigenspace도 자력 발견 |
| 안정성 (연속/이산) | ✅ 2026-07-28 | ⚠️ $\lambda=1$에서 연속/이산 혼동 재발 → 미니 테스트로 교정 |

**총평**: 계산은 전부 자력. 두 번의 지적이 세션의 질을 올렸다 —
✍️ "$P$랑 $P^{-1}$은 어떻게 구하는지 안 다뤘잖아"(튜터가 eigenvector를 건네주기만 하고 넘어간 것을 포착),
✍️ "여러 개가 존재하잖아"(eigenvector의 해집합이 직선 전체임을 스스로 발견 → eigenspace).
전자 덕분에 특성방정식이 **Session 1의 동치 사슬을 도구로 쓰는 구조**라는 게 드러났다.
남은 감시 대상은 **연속/이산 규칙 혼동**(Phase 3 I4 이후 두 번째).

**다음**: Session 3 (최소제곱 = 정사영의 일반화, Phase 6 칼만 게인의 뿌리)
