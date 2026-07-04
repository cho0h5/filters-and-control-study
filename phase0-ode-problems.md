# Phase 0 — Session A: First-order ODE 연습문제

> 목표: general solution → initial condition → verify 절차를 손에 붙이기
> 규칙: 모든 문제 **verify 두 줄 포함** (ODE 대입 확인 + IC 확인)

## 풀이 절차

```
y' + ay = b
```

1. **y_h** (homogeneous): `e^(λt)` 추측 → characteristic equation `λ + a = 0` → `y_h = C·e^(−at)`
2. **y_p** (particular): 상수 `K` 추측 (수평선) → 상수의 미분은 0 → `aK = b` → `K = b/a`
   - y_p는 ODE만 만족하면 됨. initial condition은 y_p의 책임이 아님!
   - 의미: steady-state value = 모든 해가 수렴하는 중심선 = DC gain(1/a) × 입력(b)
3. **General solution** = `y_h + y_p = C·e^(−at) + b/a`
4. **Initial condition은 맨 마지막**: general solution에 t=0 대입 → C 확정
5. **Verify**: ① 해를 ODE에 대입해 좌변 = 우변 확인 ② y(0) 확인

## 문제

### ✅ 1. `y' = −4y, y(0) = 3` — 완료

답: `y = 3e^(−4t)`
Verify: y' = −12e^(−4t) = −4y ✓, y(0) = 3 ✓

### ✅ 2. `y' = 2y, y(0) = −1` — 완료

답: `y = −e^(2t)`
Verify: y' = −2e^(2t) = 2y ✓, y(0) = −1 ✓

### 📖 3. `y' + 3y = 6, y(0) = 0` — 함께 풀이함 (복습용)

| 단계 | 계산 |
|---|---|
| ① y_h | λ + 3 = 0 → λ = −3 → `C·e^(−3t)` |
| ② y_p | 3K = 6 → `K = 2` (= steady-state value) |
| ③ general | `y = C·e^(−3t) + 2` |
| ④ IC | 0 = C + 2 → `C = −2` |
| 답 | **`y = 2(1 − e^(−3t))`** |
| ⑤ verify | y' = 6e^(−3t), 3y = −6e^(−3t)+6 → 합 6 ✓, y(0) = 0 ✓ |

- steady-state value = 2, 수렴 속도는 지수의 3이 지배
- **time constant τ = 1/3**: τ마다 남은 거리의 63%씩 접근
- 그래프: 0에서 출발해 수평선 y=2에 아래에서 달라붙는 곡선

### ✅ 4. `y' + y = 2, y(0) = 5` — 자력 (y_p 개념 보충 후)

> 표기: ✍️ = 내가 쓴 답 그대로 / 💬 = Claude가 덧붙인 해설·교정

- ✍️ ① y_h = Ce^(-t) ② y_p = 2 ③ general = Ce^(-t) + 2 ④ C = 3 ⑤ verify: -3e^(-t) + 3e^(-t) + 2 = 2
- 💬 답 정리: `y = 3e^(−t) + 2`. verify에 y(0) = 3+2 = 5 확인 한 줄 추가 권장
- 💬 추가 질문(그래프)은 못 풀어서 해설로 이해: 5에서 출발해 수평선 y=2에 **위에서 감속하며** 달라붙는 감쇠 곡선 (3번은 아래서 접근 — 같은 중심선, C 부호만 반대). first-order는 목표에 가까울수록 y'→0이라 **절대 overshoot 없음** (overshoot은 2차·complex pole부터). "수식 → 그래프 읽기"(출발점·도착점·빠르기) 자체가 낯설었음 → 복습 포인트

### ✅ 5. `T' = −0.1(T − 20), T(0) = 90` (분 단위, 커피 식히기) — 완전 자력

- ✍️ u(t) = 70e^(-0.1t) / T(t) = 70e^(-0.1t) + 20 / verify: -7e^(-0.1t) = -0.1(70e^(-0.1t) + 20 - 20) / 도달 시각 = -10ln0.5 / steady-state 20 확인 YES
- 💬 정리: t = −10·ln(0.5) = 10·ln2 ≈ **6.9분**. verify까지 스스로 쓴 첫 문제
- 💬 출제 장치 해설: 55°C는 90→20의 정중앙 = half-life 문제였음: `t_half = τ·ln2 ≈ 0.693τ` (τ = 10분). first-order는 뭐든 "τ마다 63%, 0.693τ마다 절반" 시계로 움직인다

---

## 🎓 Session A 완료 (2026-07-04)

실제 경과 (복습 우선순위용):
- **1, 2번**: 자력 (verify는 처음에 생략 → 이후 습관화)
- **3번**: 막혀서 **함께 풀이** — y_p 단계에서 걸림. 절차 전체를 다시 볼 땐 이 문제부터
- **4번**: y_p 개념("아무 해나 하나 찾기", IC는 y_p 책임 아님) 보충 설명 후 **자력**. 추가질문(수식→그래프 읽기)은 해설로 이해
- **5번**: substitution 포함 **완전 자력**, verify도 스스로 씀

교정 확인된 것: 초기조건 처리 절차, verify 습관. 아직 설명이 필요했던 것: y_p의 의미, 수식을 그래프로 읽기.
다음: Session B 주파수응답 판별법

## 배운 개념 메모

- **좌변 = 시스템 본성, 우변 = 외부 입력**. ODE는 게임 루프의 업데이트 규칙(`y += dt·f(y,u)`)의 연속 극한
- homogeneous의 상수는 **곱셈** `C·e^(λt)` (덧셈 `e^(λt)+c`는 해가 아님 — 대입하면 a·c가 남음)
- C는 homogeneous 단계에서 고르지 않는다 — **해 가족 전체**를 들고 가다가 IC가 마지막에 한 곡선을 지목
- ODE 차수 = 미정 상수 개수 = 필요한 IC 개수 (2차부터는 complex 근 → 진동 가능)
- characteristic equation의 근 λ = Phase 1의 **pole** (음수면 감쇠 = stable)
