# 필터 · 제어이론 학습 로드맵

> 작성일: 2026-07-04 · 기준: 주 5~7시간, 총 5~6개월
> 대상: CS 전공, 신호및시스템은 연속/이산 푸리에 변환까지 수강
> **기간 재조정 (2026-07-11)**: 실측 페이스 기준(Phase 1·3 각각 2일 완료)으로 남은 구간을 "학습일"(세션 2~3개를 소화하는 날) 단위로 산정
> **범위 확장 (2026-07-25)**: Phase 7(MPC) 추가, Phase 8(비선형·적응) 선택 항목으로 기록 — **Phase 6까지 8~11 학습일, MPC 포함 시 11~15 학습일**

## 설계 원칙

1. **손 유도 → Python 검증**: 진단 결과 개념 직관은 강하지만 손계산 절차가 약함. 모든 단계에서 손으로 유도한 뒤 코드로 검증하는 짝을 유지한다.
2. **선형대수는 필요해지기 직전에**: 최대 빈칸이지만 처음부터 하면 동기가 없다. 상태공간(Phase 5) 직전에 배치.
3. **베이즈 강점은 칼만에서 회수**: 로드맵 전체가 칼만 필터라는 정상을 향하는 구조. 칼만 필터 = 베이즈 갱신의 재귀적 적용.

## 진단 요약 (2026-07-04)

| 영역 | 상태 | 비고 |
|---|---|---|
| 베이즈 추론 | ✅ 강함 | 수치 계산까지 두 번 검증됨 |
| 개념 직관 (테일러=선형화, 오일러=회전, 고유값 의미) | ✅ 강함 | |
| 컨볼루션 정리, 나이퀴스트, FFT | ✅ 탄탄 | |
| 필터 주파수응답 직관 | ⚠️ 암기 수준 | 차분 필터가 고역통과임을 판단 못함 |
| 미분방정식 (초기조건 처리) | ⚠️ 복습 필요 | 일반해에 IC 대입 절차가 흔들림 |
| 분산 대수 | ⚠️ 반쪽 | a²는 알지만 +상수 처리 모름 |
| 공분산, 포아송/지수/기하분포 | ❌ 빈칸 | 칼만 직전에 보충 |
| 선형대수 (rank, 대각화, 최소제곱, SVD, 양의 정부호) | ❌ 최대 빈칸 | Phase 4에서 재무장 |
| 라플라스, 전달함수, Z-변환, PID, 보드선도, 칼만 | ❌ 미학습 | 본 로드맵의 학습 대상 |

---

## ✅ Phase 0 — 워밍업 (완료: 2026-07-04)

재검증에서 흔들린 기초를 굳힌다. 짧지만 건너뛰면 Phase 1이 모래 위에 선다.

- [x] 1차 미분방정식 (Session A, phase0-ode-problems.md): 일반해 → IC → verify 절차 장착
- [x] 주파수응답 판별법 (Session B, phase0-freqresponse-problems.md): H 유도, 양끝 판별, zero 발견, Python 검증
- [x] 분산 대수 (Session C, phase0-variance-problems.md): 전 문제 자력, C1 설욕, σ²/N까지
- 복습 포인트: y_p 개념(A-3), H(e^(jω)) 유도 시작하기(B-1), 수식→그래프 읽기(A-4)

**자료**: 3Blue1Brown *Differential Equations* 시리즈 · Paul's Online Notes (ODE)

## ✅ Phase 1 — 라플라스 변환과 전달함수 (완료: 2026-07-05)

두 트랙(필터·제어)의 공통 관문. X(jω) 표기의 정체(s = σ + jω의 허수축 제한)가 여기서 해소된다.

- [x] 라플라스 변환 정의, 주요 변환쌍, "미분 → s곱" 성질 (Session 1, phase1-laplace-problems.md)
- [x] 미분방정식 → 대수방정식 → 전달함수 H(s) 흐름 체득 (Session 2, phase1-transferfunction-problems.md)
- [x] **극점 위치 ↔ 시간응답 모양** 대응표: 좌반평면=감쇠, 우반평면=발산, 허수축=경계 — 대화로 정리(별도 문제 파일 없음)
- [x] 1차 시스템(시정수, Session 2) + **2차 시스템(감쇠비 ζ, 고유진동수 ωn) 계단응답** (Session 3, phase1-2ndorder-problems.md)
- [x] Python: `scipy.signal.step`으로 극점 옮겨가며 응답 관찰 (phase1_2ndorder_check.py 실행·확인 완료)

**자료**: Oppenheim *Signals and Systems* 9장 · YouTube **Brian Douglas** (Control System Lectures)

## Phase 2 — 고전 제어 (학습일 2~3일, 세션 4개) ← 다음 차례

- [x] 블록선도, 피드백의 의미, 닫힌루프 전달함수 G/(1+GH) 유도 (Session 1, phase2-feedback-problems.md)
- [x] PID: P만(정상상태 오차 잔존) → +I(오차 제거, 오버슛) → +D(감쇠) 순서로 시뮬레이션하며 체감 (Session 2, phase2-pid-problems.md)
- [ ] 보드 선도 읽기/그리기, 이득 여유·위상 여유 (Session 3)
- [ ] **root locus** — K가 변할 때 pole이 그리는 궤적. Session 2에서 손으로 이미 한 것(W2의 −(2+K), W5의 수직선)의 이름과 작도법. Bode와 짝: root locus는 pole의 이동, Bode는 주파수별 이득·위상 (Session 3에 포함)
- [ ] 📌 **프로젝트**: PID 튜닝 — `python-control` 시뮬레이션(크루즈 컨트롤/온도 제어) **또는 Dynamixel 실물** (미정). 실물로 하면 system identification(PWM 모드 step 응답으로 G·H 동정)이 앞에 붙고, loop rate를 낮춰가며 발진 지점을 찾아 phase margin을 실측할 수 있음. Phase 3의 my_iir을 filtered derivative 구현에 재사용

**자료**: Åström & Murray *Feedback Systems* (무료 PDF) · Brian Douglas

## ✅ Phase 3 — 디지털 필터 (완료: 2026-07-11) 🔑

CS 본능과 가장 잘 맞는 구간. Phase 2와 순서를 바꿔도 된다. (Phase 2보다 먼저 진행하기로 결정 — Phase 1의 pole/ROC 직관을 바로 재사용할 수 있고, 최초 진단에서 약했던 필터 주파수응답 직관을 직접 복구하는 구간이라 우선순위를 앞당김)

- [x] Z-변환 = 이산판 라플라스, 단위원 ↔ 허수축 대응, "극점이 단위원 안 = 안정" (Session 1, phase3-ztransform-problems.md)
- [x] FIR 필터: 윈도우 설계법, 선형 위상의 의미 (Session 2, phase3-fir-problems.md)
- [x] IIR 필터: 아날로그 프로토타입(버터워스 등) + 쌍선형 변환 — Phase 1이 재사용됨 (Session 3, phase3-iir-problems.md)
- [x] 📌 **프로젝트**: 드론 고도 센서 노이즈 필터링 (phase3-project.md, phase3_project.py) — my_convolve·my_iir 직접 구현(scipy와 1e-15 일치), FIR/IIR 지연·RMS 비교, 결론 작성, filtfilt zero-phase까지

**자료**: *The Scientist and Engineer's Guide to DSP* (dspguide.com, 무료)

## Phase 4 — 선형대수 재무장 (학습일 3~4일, 세션 4~5개)

상태공간 진입 직전 배치. 최대 빈칸이지만 목표가 명확해 빠르게 간다.

- [ ] **동치 사슬 하나로 꿰기**: rank ↔ det≠0 ↔ 열 선형독립 ↔ 역행렬 존재
- [ ] 대각화 A = PDP⁻¹ (아는 고유값 직관에서 한 걸음), e^(At)이 대각화로 쉬워지는 이유
- [ ] 최소제곱법 — 이미 아는 정사영 (uᵀb)u의 일반화로 접근
- [ ] 양의 정부호 행렬, SVD는 개념만
- [ ] 그래디언트 = 최급상승 방향 (5분 보충)

**자료**: 3Blue1Brown *Essence of Linear Algebra* 전편 · MIT 18.06 (Strang) 선별 강의

## Phase 5 — 상태공간 제어 (학습일 2~3일, 세션 3~4개)

- [ ] 상태공간 모델 ẋ = Ax + Bu, y = Cx + Du, 전달함수와의 상호 변환
- [ ] **안정성 = A의 고유값** (Phase 4 즉시 회수)
- [ ] 가제어성/가관측성 개념, 상태 피드백, LQR 맛보기, 이산화
- [ ] 📌 **프로젝트**: 도립진자 선형화(테일러 1차 — 이미 아는 것) → 상태 피드백으로 세우기

## Phase 6 — 칼만 필터 (학습일 3일, 세션 3~4개 + 최종 프로젝트) 🏔️ 최종 목적지

- [ ] 공분산, 다변량 가우시안 보충 (확률 빈칸 해소)
- [ ] 칼만 필터를 **베이즈 갱신의 재귀적 적용**으로 유도: 예측(사전) → 측정(우도) → 갱신(사후)
- [ ] 1D 필터 직접 구현 → 2D 확장
- [ ] 📌 **최종 프로젝트**: 2D 물체 추적기 (노이즈 낀 위치 측정 → 위치+속도 추정)

**자료**: Labbe, *Kalman and Bayesian Filters in Python* (무료 Jupyter 북) — 이 구간은 이 책 하나로 충분

## Phase 7 — MPC (Model Predictive Control) (학습일 3~4일) — 추가: 2026-07-25

Phase 6 이후의 확장. **현대 제어의 실무 표준**이고, PID·LQR이 못 다루는 두 가지를 정면으로 푼다.

동작 원리: 매 스텝마다 ① 모델로 미래 N스텝 예측 → ② 비용 최소화 입력 시퀀스를 최적화로 계산 →
③ **첫 입력만 적용하고 나머지는 버림** → ④ 다음 스텝에서 다시 (receding horizon).

| | 설계 방식 | 제약 조건 | 계산량 |
|---|---|---|---|
| PID | pole placement | ❌ | 곱셈 몇 번 |
| LQR (Phase 5) | 무한구간 최적화, 닫힌 해 | ❌ | 곱셈 몇 번 |
| **MPC** | 유한구간 최적화, 매 스텝 온라인 | ✅ 명시적 | QP 1회 |

- [ ] receding horizon 개념, LQR과의 관계(제약 없는 무한구간 MPC = LQR)
- [ ] 비용함수 설계, 예측 지평선 N과 제어 지평선의 트레이드오프
- [ ] **제약 조건 처리** — Phase 2에서 땜빵(anti-windup)으로 처리한 actuator 포화를 최적화 제약으로 직접 기술. windup이 개념적으로 발생하지 않음
- [ ] QP(이차계획법) 기초 — 새로 필요한 유일한 수학
- [ ] 📌 **프로젝트**: 도립진자를 **입력 제한을 걸고** MPC로 세우기 → Phase 5의 LQR 버전과 직접 비교

**선수 조건**: Phase 5(예측 모델 = 상태공간), Phase 4(선형대수), Phase 3(이산화 ✅).
그리고 실전에서는 **Phase 6이 사실상 선수 조건** — MPC는 "현재 상태"를 알아야 예측하는데
실제로는 일부만 측정되므로 상태 추정기가 필요하다. **Kalman + MPC가 현대 제어의 표준 스택.**

**자료**: Rawlings & Mayne *Model Predictive Control* (무료 PDF) · `do-mpc` / `cvxpy` 파이썬 라이브러리

## Phase 8 — 비선형·적응 제어 (선택, 미정) — 추가: 2026-07-25

**하기로 결정한 것이 아니라, 안 하기로 한 이유를 남겨두는 칸.**

- [ ] Lyapunov 안정성 — 비선형 시스템의 안정성 판정. 아래 두 항목의 공통 선수 조건
- [ ] 적응 제어 (MRAC, MIT rule) — 게인을 실시간 경사하강으로 조정: `dθ/dt = −γ·e·∂e/∂θ`
- [ ] 되먹임 선형화, sliding mode

**우선순위가 낮은 이유** (2026-07-25 판단):
1. **MIT rule은 안정성 보장이 없다.** 직관으로 만든 규칙이라 발산 사례가 있고, 이후 Lyapunov 기반
   MRAC로 대체됨. 제대로 하려면 Lyapunov 모듈이 선행되어야 함
2. **feedback 자체가 이미 robustness를 준다** — Phase 2 B5에서 실측: plant gain이 50% 변해도
   closed-loop 오차는 0.7%만 틀어짐. 대부분의 plant 변동은 feedback이 흡수하고,
   나머지는 게인 스케줄링이라는 훨씬 단순한 방법으로 처리됨
3. 드론·로봇 목표에는 MPC(Phase 7)가 훨씬 실용적

단, **드론 자세 제어는 본질적으로 비선형(SO(3) 위의 회전)** 이라 그쪽으로 깊이 갈 경우 Lyapunov가 필요해짐.

---

## 진행 기록

| 날짜 | Phase | 메모 |
|---|---|---|
| 2026-07-04 | 진단 완료 | 로드맵 수립, Phase 0 시작 전 |
| 2026-07-04 | Phase 0 — ODE 세션 완료 | 1·2·5번 자력 정답, 3번 함께 풀이, 4번 y_p 보충 후 자력 정답 (phase0-ode-problems.md). verify 습관 장착, y_p 개념·그래프 읽기는 해설 필요했음 |
| 2026-07-04 | Phase 0 — 주파수응답 세션 완료 | B1 함께 풀이(H 개념부터), B2·B3·B4 자력 정답, B5 해석 오답(band-pass 학습), B3의 zero를 Python으로 스스로 발견 (phase0-freqresponse-problems.md). 남은 것: 분산 대수 |
| 2026-07-04 | **Phase 0 전체 완료** 🎓 | Session C(분산) C1~C5 전부 자력 정답 — 보조 없이 완주한 첫 세션. C1로 재검증 오답 설욕, σ²/N 유도·해석까지. 다음: Phase 1 Laplace |
| 2026-07-04 | Phase 1 — Session 1 완료 (Laplace 정의·기본 성질) | W0~L3 자력, L1 ROC·L3 통분에서 오답 교정, L4 개념 해설 후 이해, L5는 힌트 1회 후 자력 완주 (phase1-laplace-problems.md). 대화로 ROC·좌우반평면·안정성 개념까지 깊게 다짐 |
| 2026-07-04 | Phase 1 — Session 2 완료 (전달함수 H(s)) | T1~T3 전부 자력, T4는 e^0=1을 e로 착각한 계산 실수를 스스로 진단·교정 (phase1-transferfunction-problems.md). "1차 시스템 τ↔pole↔정착시간" 삼단 대응 확립. 남은 것: 2차 시스템(ζ,ωn), scipy 실행 |
| 2026-07-05 | **Phase 1 전체 완료** 🎓 (Session 3, 2차 시스템) | H(s)=ωₙ²/(s²+2ζωₙs+ωₙ²) 유도부터 직접 함(L{ẍ} 자력 유도 → IC=0 대입). ωₙ² 계수의 의미(DC gain=1 정규화)까지 스스로 확인. P1 표준형 매칭에서 제곱근 빠뜨린 실수 자가교정. P2~P4(overdamped pole, underdamped 복소pole, ωd 개념) 자력. P5에서 ζ=2를 "발산"·"더 빠르다"로 두 번 오답했다가 직접 계산 후 교정(원점에 가까운 pole이 지배 = 더 느림, T3/T4 규칙 재확인). 마지막에 "ζ=2도 진동하는거 아니야?" 질문 — ζ²−1 부호로 실근/복소근 경계가 정확히 ζ=1임을 재확인하며 마무리. 다음: Phase 2(고전 제어) 또는 Phase 3(디지털 필터) 중 선택 |
| 2026-07-05 | Phase 3 시작 결정 + Session 1 완료 (Z-transform) | Phase 2보다 Phase 3를 먼저 하기로 결정(Phase 1 직관 재사용 + 필터 약점 복구). W0(세 변환 비교)에서 "e를 z로 뭉갰다"는 오해 → 복리 비유(연속=rate 누적=더하기, 이산=ratio 반복=곱하기)로 정리, 최종 자력 도달. Z1~Z4(감쇠/pole/ROC, 단위원=안정 대응, 상수 vs 진동 구분, shift property) 전부 자력. Z2에서 "단위원 위=진동"이라 오해했다가 각도(angle)와 크기(magnitude)를 구분하며 교정. Z5(전달함수 H(z))는 Y/X 방향을 헷갈렸다가 스스로 "실수로 적었다"며 즉시 교정. 다음: Phase 3 Session 2 (FIR 필터) |
| 2026-07-05 | Phase 3 — Session 2 완료 (FIR 필터) 🎓 | F1(이동평균=저역), F2(차분필터=고역) 전부 자력 — **Phase 0에서 판단 못했던 차분필터 문제를 Z-transform으로 완전히 해소**. F3(zero↔주파수감쇠)은 직관은 맞았으나 "거리" 개념으로 정밀화 필요. F4(선형위상)에서 "왜 정확히 1칸이냐" 스스로 반문 → e^(−jω) 인수분해 유도 자력 완성, 이어서 파생 질문 4개(순수지연과의 차이, 5탭 지연 규칙 일반화, 탭개수 vs 필터강도 — DC gain 정규화 후 비단조 리플 발견, sinc vs Gaussian 윈도우 트레이드오프)로 원래 문제 범위를 크게 넘어서는 깊은 이해 도달. F5(ideal filter→window)는 "주파수영역에서 꼬리생기나"로 Gibbs phenomenon을 스스로 예측. 다음: Phase 3 Session 3 (IIR 필터, 버터워스+쌍선형변환) 또는 프로젝트 |
| 2026-07-11 | 워밍업(6일 공백) + Phase 3 — Session 3 완료 (IIR 필터) 🎓 | 워밍업 W1~W5: pole 정의·H(z) 레시피만 재장착하니 판단 5문제 전부 자력(지난 오답 지점 전부 통과), 거리 방법 \|H\|=∏zero거리/∏pole거리 일반화 확인. Session 3: I1(1-pole IIR, DC정규화) — **상수 계수 0.1 누락 2회(세션 감시 대상)** 외 자력. I2(공진기)에서 pole/zero 역할 혼동("원 위로 가면 필터됨") → 거리 방법으로 교정, "단위원 위=발산" 오답도 발진기/공진 누적으로 정밀화. I3에서 "y[n−1] 하나=pole 하나?" 구조 질문 자력. I4에서 **연속/이산 규칙 혼동 발견**(s=−1을 "부호 반전"으로 읽음) → 두 세계 규칙표로 교정, τ 재장착. I5 bilinear 대입 자력 완주 — 이동평균=1차 Butterworth의 bilinear 이미지 발견, "왜 아날로그로 돌아가나" 동기 질문(답안지 번역 구도). Python 검증 4문제 전부 손계산 일치. 다음: Phase 3 프로젝트(필터 직접 설계·적용) |
| 2026-07-11 | **Phase 3 전체 완료** 🎓 — 프로젝트 (드론 고도 필터링) | 첫 코딩 프로젝트. my_convolve: "x[n]·h[n]" element-wise 시도 → "x랑 h가 시간축이야 주파수축이야?" 질문으로 컨볼루션 정리 양변 구분하며 해소, 수식↔코드 대응표로 자력 완성(lfilter와 6.7e-16 일치). my_iir: 버그 4개(경계 체크, 계수-과거 짝, 부호, i=0 자기소거)를 전부 **"답을 아는 미니 테스트"(δ→0.1·0.9ⁿ)로 잡는** 디버깅 루프 체득. butter 반환 순서 뒤집힘도 경험. M3에서 자발적 확장: "FIR 25-tap이면 똑같잖아?" → 실험으로 검증(지연 동률, RMS 1.16배 악화 — 4배 예측 빗나감), correlate vs covariance 질문, "linear phase가 뭐가 좋은데?" → 신호의 소비자 관점(값 vs 모양) 획득. 결론 리뷰 2회(수치 오류 0.7→0.0707, 반대 논거 보강) 후 승인. M4 filtfilt 추론 자력. 다음: **Phase 2 (고전 제어)** — 프로젝트의 "지연이 제어에 독" 논의가 위상 여유로 이어짐 |
| 2026-07-11 | Phase 2 시작 — Session 1 완료 (block diagram, feedback) | B1 자력(직렬 pole-zero cancellation 함정은 분수곱 힌트 후 자력 발견, Phase 5 가관측성 예고). B2 **T = G/(1+GH) 자력 유도** — "R − H = E" 블록/신호 혼동 1회 교정, **"왜 유한한 Y 가정? 발산할 수도"** 파생 질문으로 1+GH=0 발산 조건·gain/phase margin 예고 도달, E/R 부호 실수는 미니테스트(G=H=1)로 자가 발견, T→1/H와 "정확도는 sensor가 결정" 해석까지. B3 pole=−(2+K) 자력, **"K=0은 open-loop이 아니라 그냥 모터 정지 아니야?"로 튜터 표현을 정정**(용어 구분: 제어 없음 vs open-loop control). B4 DC gain 방법 재소환 후 자력, 평형 논리("내려가려는 힘이 있으니 1보다 작은 곳에서 평형") 자력, e(∞)=2/(K+2), **적분항 예측**(Session 2 확인 예정). B5 예측·계산 자력(open 1.5 vs closed 0.987), 출제 오류((K+2)/K 보정) 검산으로 정정됨, robustness를 S(0)=1/50로 정량 연결. 확장 대화: 모터vs센서 책임 분담, Kalman=조건부 optimal, S+T=1. 다음: Session 2 (PID) |
| 2026-07-25 | 워밍업(14일 공백) + Phase 2 — Session 2 완료 (PID) 🎓 | 워밍업 W1~W5: W1 closed-loop 재유도 자력(B2의 신호/블록 혼동 교정된 채 통과). W2에서 "왜 빨라지나"를 시간 도메인으로 내려가 `ẏ=−2y+K(R−y)` → y의 계수 −(2+K) 자력 도출(ODE↔pole 동일성 확인). W3에서 `1/s`를 "unit step"으로 답해 **신호/블록 혼동 재발**(감시 대상) → 적분기로 교정, plant가 적분기를 공짜로 갖는 경우 발견. **W5에서 "실수부 다 −1이네"를 자력 발견** — K를 100배 키워도 정착 시간 불변, 진동만 증가(순손실)를 스스로 규명하고 `s²+2s+K`의 s계수에 K가 못 닿음까지 연결. 이어 `C=K_p+K_d·s` 대입해 pole placement 원리 자력 도달. 본편: P1(PI, e(∞)=0, I가 차수를 올림) → P2(적분값이 `2/K_i`를 지나치면 overshoot, windup 예고) → P3(**ζ=0.7, ωₙ=10 사양에서 K_p=12, K_i=100 역산 자력**, "PID=2차 plant를 완전 지배하는 최소 controller" 도출, Phase 5 예고) → P4(미분=고역통과 Phase 3 F2 회수, chattering, **필터↔지연 딜레마**가 드론 프로젝트 결론과 접속, filtered derivative의 properness 이유). P5에서 **"1차 plant엔 PID 다 할 필요 없는 거 아니야?"를 자발적으로 제기**하고 `(1+K_d)s²+(2+K_p)s+K_i`로 근거까지 유도(D가 최고차항에 앉아 ζ·ωₙ 둘 다 깎임, 실수부 −6→−3). 이어 **"PI보다 PID가 overshoot 적은 거 아니야?" 반문이 실측으로 입증됨(20.3% vs 30.8%)** — 튜터의 ζ→overshoot 예측이 zero를 무시한 오류였음을 인정하고 정정: 표준형 표는 분자가 상수일 때만 유효, PI/PID는 항상 zero 생성, PID는 biproper라 `y(0+)=T(∞)=0.5`(derivative kick, FVT의 쌍둥이). ⚠️ 표준형 매칭에서 `2ζωₙ`의 2 누락이 하루 3회(W4·P1·P5) — 절차 습관 감시 대상. 다음: Session 3 (Bode plot, gain/phase margin) |
