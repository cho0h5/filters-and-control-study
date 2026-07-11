# Phase 2 — Session 1: Block diagram과 feedback

> 목표: block diagram을 "s-도메인 수식의 그림 표기"로 읽고, negative feedback의
> closed-loop transfer function을 **직접 유도**한다. 그리고 feedback이 하는 일 두 가지 —
> **pole을 옮긴다**(속도가 바뀐다), **오차를 줄인다**(그러나 P만으로는 0이 안 된다) — 를 확인한다.
> 선행: Phase 1 (H(s), pole ↔ 응답 속도, DC gain)

## 도구 정리

**Block diagram의 부품은 딱 3개다.** 전부 s-도메인(Laplace) 신호 위에서 동작한다.

```
1) block:              X(s) ──▶[ G(s) ]──▶ G(s)·X(s)        (곱하기)
2) summing junction:   A ──▶(+)──▶ A − B                     (더하기/빼기, 부호는 화살표 옆에 표시)
                            ▲(−)
                            B
3) pickoff point:      ────●────▶  같은 신호가 두 갈래로     (복사)
```

블록 하나가 곱하기인 이유는 이미 안다: Y(s) = H(s)·X(s) (Phase 1 T1, convolution 정리).
즉 block diagram은 **연립 대수방정식을 그림으로 그린 것**이고, "diagram 정리"는 그냥 식 소거다.

**용어 주의 (표기 충돌)**: 제어 교과서에서는 관례상
- G(s) = **plant** (제어 대상: 모터, 히터, 차량...) — 지금까지 우리가 H(s)라 부르던 그것
- H(s) = **sensor** (출력을 측정해서 되돌리는 경로) — 새 등장인물
- 닫힌루프 전체의 전달함수는 T(s)로 쓴다

H(s) = 1이면 (출력을 그대로 되먹임) **unity feedback**이라 부른다. 이 세션 대부분은 unity feedback.

**표준 negative feedback 구조** (이 그림을 계속 쓴다):

```
 R(s) ──▶(+)──▶ E(s) ──▶[ G(s) ]──▶ Y(s) ──●──▶
          ▲(−)                              │
          └───────────[ H(s) ]◀─────────────┘
```

- R = reference (원하는 값, setpoint), E = error, Y = 실제 출력

> 표기: ✍️ = 내가 쓴 답 그대로 / 💬 = Claude가 덧붙인 해설·교정

## 문제

### ✅ B1. Series와 parallel — diagram을 식으로 (자력, cancellation 함정은 유도 후 자력 발견)

(a) 직렬(series): `X ──▶[G₁]──▶[G₂]──▶ Y`. 전체 전달함수 Y/X는? 전체 시스템의 pole 집합은
G₁, G₂ 각각의 pole과 어떤 관계인가?

- ✍️ Y/X = G₁·G₂, pole은 "각 pole의 합집합 — 곱하기니까 각 분모를 0으로 만드는 게 나중에도 유지돼"
- 💬 함정 문제(G₁=1/(s+2), G₂=(s+2)/(s+3)): 처음 "제곱 어떻게 했었는지 기억 안 나네"로 분수 곱셈에서
  멈칫 → 분자끼리/분모끼리 힌트 후 ✍️ "(s+2)가 약분되니까 pole은 {−3}만 남네" 자력 발견.
  규칙 정정판: **직렬 pole = 합집합, 단 pole-zero cancellation이 없을 때**.
  cancellation돼도 물리 모드는 사라진 게 아니라 입출력에서 안 보일 뿐 → Phase 5(가제어성/가관측성) 예고

(b) 병렬(parallel): X가 pickoff로 갈라져 [G₁]과 [G₂]를 각각 통과한 뒤 summing junction에서
(+,+)로 합쳐져 Y가 된다. 전체 전달함수는? (Phase 3에서 이 구조를 이미 만난 적 있다 — 어디였을까?)

- ✍️ "합", Phase 3 연결은 "fir" — 정답. H(z) = 1 + z⁻¹ = 경로별 합, FIR은 병렬 규칙을 이미 쓰고 있었던 것

### ✅ B2. 핵심 유도: closed-loop transfer function ★ — 유도 자력, 파생 질문으로 발산 조건까지

위 표준 negative feedback 그림에서, diagram을 보고 **연립방정식 2개**를 세운 뒤
E(s)를 소거하여 T(s) = Y(s)/R(s)를 유도하라.

- ✍️ 첫 시도 "R − H = E" → 💬 H는 신호가 아니라 블록(경로를 따라가면 (−)에 들어오는 신호는 H·Y)
  → ✍️ E = R − H·Y 교정, Y = G·E와 연립해 **T = G/(1+GH) 자력 유도**
- ✍️ unity feedback: T = G/(1+G)
- 검산(G→∞): ✍️ "E가 작아져?" 직관은 정확 → 파생 질문 **"왜 유한한 Y라고 가정해? 발산할 수도 있잖아"** →
  💬 가정이 아니라 결과(1+GH≠0인 한 해가 존재, negative feedback의 자기억제 구조) +
  네 의심이 맞는 경우가 정확히 **1+GH=0** — 위상 지연으로 우반평면 근이 생기면 진짜 발산,
  그걸 재는 자가 gain/phase margin (Session 3 예고)
- ✍️ E/R 유도: "1/(1−HG)" 부호 실수 → 미니 테스트(G=H=1 → ∞ vs 1/2 모순)로 자가 발견 →
  **E/R = 1/(1+GH)** (나중에 sensitivity function으로 재등장). G→∞ ⇒ E→0 ⇒ **T → 1/H**
- ✍️ 해석: gain 크면 정확도는 "H"가 결정 — 💬 정확도의 책임이 plant에서 sensor로 이사, feedback의 존재 이유

### B3. Feedback은 pole을 옮긴다 — Phase 1 회수 ★

Plant G(s) = 1/(s+2) (Phase 1 T1의 그 시스템, τ=0.5)를 gain K와 함께 unity feedback으로 감싼다:
loop 안의 전달함수는 K·G(s), sensor H=1.

(a) T(s) = Y/R를 구하라 (B2 결과에 대입).

(b) closed-loop pole은 어디인가? K = 0, 2, 8일 때 각각 계산하라.

(c) K가 커지면 시스템은 빨라지는가 느려지는가? Phase 1 T3의 삼단 대응
(τ ↔ pole 위치 ↔ 속도)으로 답하라. **open-loop plant는 그대로인데 응답 속도가 바뀌었다** —
필터에서는 못 하던 일이다. 이게 제어의 첫 번째 무기.

- ✍️ (a) 대입 자력 → 겹분수 정리 후 T = K/(s+2+K), (b) "s = −2−K → K 커질수록 pole 왼쪽으로" (−2, −4, −10)
- 파생 질문 2개: "K=0이 왜 open-loop이야? H가 무시돼?" → 💬 신호가 K에서 죽는 것(보일러 코드 뽑기 비유) →
  ✍️ **"open-loop이 아니라 그냥 모터가 동작 안 하는 거 아니야?"** — 정확한 반박. 💬 용어 정정:
  K=0은 "제어 없음", open-loop control은 "결과 안 보고 밀기"(B5 예고). 공통점은 **pole을 못 옮긴다**,
  "open-loop pole"은 G 자체의 pole을 가리키는 관용구
- ✍️ (c) "빨라져", τ = 1/(2+K), K=8이면 0.5 → 0.1로 "5배" — plant 그대로인데 속도 변경, 제어의 첫 무기 확인
- 세션 중 확장 대화: "모터가 그지같아도 센서만 좋으면 돼?" → 💬 정확도는 산다,
  못 사는 것 둘(saturation의 물리 한계, 위상 지연이 정하는 K 상한) + 센서 맹신 문제 → 필터 → 지연 → Kalman 예고 /
  "Kalman이 최종 보스? 제일 좋아?" → 💬 선형+Gaussian+모델 기지 전제에서 증명된 optimal,
  주파수 분리(Phase 3)와 달리 동역학 모델+노이즈 통계로 Bayes 재귀 갱신 / "T(s)의 T가 뭐야?" →
  Transfer, S = E/R와 짝: unity feedback에서 **S + T = 1** 시소 구조

### B4. P control의 한계: steady-state error ★

B3의 시스템에 step 입력 R(s) = 1/s를 넣는다. K는 "오차에 비례해 미는" **proportional gain**이고,
이 구조가 곧 **P controller**다.

(a) 최종 정착값 y(∞)는 T(s)의 DC gain으로 읽을 수 있다 (Phase 3에서 쓰던 그 방법, s=0).
K = 2, 8, 98일 때 y(∞)를 각각 구하라.

(b) steady-state error e(∞) = 1 − y(∞)를 K의 식으로 써라. K를 아무리 키워도
e(∞) = 0이 **정확히는** 안 되는 이유를 diagram의 E(s) 관점에서 설명하라.
(y가 목표에 도달했다고 가정하면 E는 얼마가 되고, 그러면 G를 미는 힘은?)

(c) 예측: 그럼 e(∞) = 0을 만들려면 controller가 어떤 성질을 가져야 할까?
"E가 0이 아니었던 **과거의 기록**"이라는 힌트로 한 문장 예측만 남겨라 — Session 2(PID)에서 실험으로 확인한다.

- ✍️ (a) DC gain 방법 재소환 필요("phase3에서 쓰던 방법이 뭐지" → z=1 정규화 기억 연결, s=0 대응) 후
  y(∞) = 0.5, 0.8, 0.98 전부 자력
- ✍️ (b) 개념 먼저 자력: "에러가 없는 상태에서 내려가려는 힘이 있으니까 **1보다 작은 곳에서 평형**" →
  식 e(∞) = 2/(K+2), "K 커질수록 e 작아짐". 💬 분자 2 = plant pole 크기(새는 속도)라는 해석 덧붙임
- ✍️ (c) 예측: "적분항" — 누적합이니까 E=0이어도 기억된 값이 u=2를 공급.
  💬 역방향 논리 보강: 적분기가 있으면 E≠0인 상태는 평형 자체가 불가(적분값이 계속 변함) →
  정착 = E=0 강제. overshoot이라는 대가는 Session 2에서 실험

### B5. 애초에 왜 feedback인가 — robustness 예측→실험

의문: 어차피 정착값이 DC gain으로 정해진다면, feedback을 걷어내고 plant의 DC gain(G(0) = 1/2)을
미리 역보정해서 — 입력에 ×2를 곱해 — open-loop로 밀면 정확히 1에 정착하지 않나?
(실제로 이걸 **open-loop compensation**이라 한다.)
💬 출제 정오: 처음엔 "(K+2)/K를 곱한다"로 냈으나 검산하면 DC = (K+2)/2 = 50(K=98)이 되는 오류.
올바른 보정은 plant DC gain의 역수인 ×2.

이제 plant가 노후화되어 G(s) = 1/(s+2)가 아니라 **1.5/(s+2)**가 되었다고 하자 (gain 50% 변동).

(a) 예측 먼저 (계산 전에 직관으로): open-loop 보정과 closed-loop(K=98) 중
어느 쪽 y(∞)가 더 크게 틀어질까?

(b) 손 계산: 두 경우의 y(∞)를 각각 구하라. (open-loop: 보정 배율은 여전히 옛날 값 ×2 그대로.
closed-loop: B4(a)의 계산에서 G만 1.5/(s+2)로 바꿔서.)

(c) 결론 한 줄: feedback의 두 번째 무기는 무엇인가?

- ✍️ (a) 예측: "open loop" — 근거를 💬 조임: open-loop 정확도는 G가 결정(변동 통과),
  closed-loop 정확도는 H가 결정(T≈1/H)인데 H는 안 변함
- ✍️ (b) closed: 147/149 ≈ 0.987 자력 (0.98 → 0.987, 0.7%p) / open: "K도 98로 가정?" 질문 →
  💬 open-loop에는 K 자체가 없음(고정 배율 ×2 → plant 사슬) → ✍️ y(∞) = 1.5 (50% 그대로 통과)
- ✍️ (c) "G가 좀 바뀌어도 된다" = **robustness**. 💬 정량 연결: 억제 배율 = S(0) = 1/(1+K·G(0)) = 1/50,
  50% × 1/50 ≈ 1% ↔ 실측 0.7%p. E/R가 "sensitivity"인 이유 + S+T=1 시소로 마무리

## Python 검증 (다 푼 뒤)

phase2_feedback_check.py 실행:
- Fig 1 — B3/B4: K별 closed-loop step response. 손으로 구한 pole 위치(범례)와
  y(∞) 값이 그래프와 일치하는지 확인
- Fig 2 — B5: plant gain이 1.0 → 1.5로 변했을 때 open-loop 보정 vs closed-loop 비교.
  (b)의 손 계산 값과 정착값이 일치하는지 확인
