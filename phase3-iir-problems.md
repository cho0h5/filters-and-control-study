# Phase 3 — Session 3: IIR 필터 — 아날로그 프로토타입과 쌍선형 변환

> 목표: FIR이 zero만으로 필터를 만들었다면, IIR은 **pole을 심어서** 훨씬 적은 계산으로
> 날카로운 필터를 만든다. Phase 1에서 배운 아날로그 H(s)(Butterworth 프로토타입)를
> **bilinear transform**으로 디지털 H(z)로 옮기는 표준 설계 경로를 체득한다 — Phase 1이 그대로 재사용되는 구간.
> 선행: phase3-ztransform-problems.md, phase3-fir-problems.md, phase1-transferfunction-problems.md
> 워밍업(2026-07-11): pole 정의·H(z) 레시피 재장착, 거리 방법(|H| = ∏zero거리/∏pole거리) 일반화 확인

## 도구 정리

**IIR (Infinite Impulse Response) 필터**: 차분방정식에 **y[n−k] 피드백 항**이 있는 시스템.

```
y[n] = Σ b_k·x[n−k] − Σ a_k·y[n−k]     (recursive)
H(z) = B(z)/A(z)                        (분모 다항식 A(z)가 생김 → pole이 원점 밖에도 존재)
```

- FIR: pole 전부 원점 → 항상 안정, zero로만 조각 → 날카로우려면 tap이 많이 필요
- IIR: pole을 단위원 **안쪽 아무 데나** 심을 수 있음 → 적은 계수로 날카로운 응답. 대신 **안정성을 직접 챙겨야 하고**(pole이 단위원 안인지), linear phase는 일반적으로 포기

**거리 방법으로 본 IIR의 원리** (워밍업에서 확인): |H(e^jω)| = ∏(zero까지 거리)/∏(pole까지 거리).
pole을 단위원 근처에 심으면 그 각도(주파수)에서 분모가 작아져 gain이 솟는다 — zero가 "죽이는" 도구라면 pole은 "살리는" 도구.

**표준 설계 경로** (이 세션의 뼈대):

```
1. 아날로그 프로토타입 H(s) 선택   ← Phase 1의 세계 (Butterworth 등)
2. bilinear transform: s = 2/T · (1−z⁻¹)/(1+z⁻¹)
3. 디지털 H(z) 획득                ← Phase 3의 세계
```

bilinear transform은 s-평면의 **허수축 전체 ↔ 단위원**, **좌반평면 ↔ 단위원 내부**로 보내는 사상.
안정한 아날로그 필터는 변환 후에도 반드시 안정 — Phase 1의 "좌반평면=안정"과 Session 1의 "단위원 안=안정"이 정확히 이어붙는 지점.

**Butterworth 필터**: "통과대역이 최대한 평평한(maximally flat)" 아날로그 저역통과 프로토타입.

```
|H(jΩ)|² = 1 / (1 + (Ω/Ωc)^(2N))     (N = 차수, Ωc = 컷오프)
```

pole들은 s-평면에서 반지름 Ωc인 원 위, 좌반평면 쪽에만 등간격으로 배치된다.

> 표기: ✍️ = 네가 쓴 답 그대로 / 💬 = Claude가 덧붙인 해설·교정

## 문제

### ✅ I1. 첫 IIR 필터: y[n] = 0.9·y[n−1] + 0.1·x[n] — 상수 0.1 슬립 2회 외 전부 자력

- ✍️ (a) 처음 "z/(z−0.9)" → 💬 상수 0.1 누락 지적 → ✍️ **"z/(10z−9)"** 로 재유도 (= 0.1z/(z−0.9), 정답). 💬 관례: 분모 최고차 계수 1로 두면 pole·상수가 바로 읽힘
- ✍️ (b) pole = 0.9, 안정 ← 자력
- ✍️ (c) 처음 "모르겠음" → 💬 δ[n]을 recursion에 직접 넣는 방법 안내 → ✍️ "1, 0.9, 0.81 → 0.9^n" — 패턴은 자력, **0.1 스케일을 또 누락** (h[n] = 0.1·0.9ⁿ). "h가 무한히 많아서 Infinite" ← 자력
- ✍️ (d) 처음 "10, −(10/19)" (0.1 누락 + |H|에 음수) → 재계산 ✍️ **"1, 1/19"** 정답, "low pass" 판정 ← 자력. 💬 DC gain=1은 0.1 = 1−0.9로 맞춘 정규화 — FIR Session 2의 DC 정규화와 같은 설계 습관
- ✍️ (e) "H수(계수)는 같은데 h 수가 무한이 됨. pole이 0에 있었는데 0이 아님" ← 자력, 핵심 둘 다 포착. 💬 보강: 유한한 계수에서 무한한 h를 만들어내는 장치가 **피드백(recursion)**이고, 원점 밖 pole이 그 대수적 흔적
- ⚠️ 세션 감시 대상: **상수(스케일) 계수 누락** 2회 — pole/모양은 정확하나 k를 흘리는 경향

### ⚠️ I2. Pole로 공진 만들기: pole을 0.95·e^(±jπ/4)에 심은 필터 — (b)에서 pole/zero 역할 혼동 교정

- ✍️ (a) "peak가 0.95e^(±jπ/4)인거잖아" ← 방향 자력. 💬 정밀화: peak은 주파수 축의 **ω ≈ π/4** (pole의 angle). 정리: **pole의 angle → peak 주파수, magnitude(단위원과의 근접도) → peak 높이·날카로움** — W1의 angle/magnitude 구분의 설계 버전
- ✍️ (b) 처음 "원 위로 올라가면 π/4가 완전히 필터됨" ← **pole/zero 역할 혼동** (죽이는 건 zero, pole은 살리는 것). 💬 거리 방법으로 교정: pole 거리는 분모 → 거리 0이면 1/0 = 무한 증폭 → ✍️ 재답 "더 높아져" 정답. "1이 되면 발산해"는 절반 교정: 단위원 위 = 스스로는 1ⁿ 진동 유지(발진기), 발산은 \|pole\|>1. 단 공진 주파수 입력이 계속 들어오면 무한 누적(그네 밀기) — 이것이 "불안정" 분류의 이유
- ✍️ (c) "허수부분이 사라져야하니까" ← 자력. (z−p)(z−p*) = z² − 2Re(p)z + \|p\|², 실계수 확인

### ✅ I3. 왜 IIR인가 — 효율 — (a) 자력 + 구조 질문으로 확장, (b) 절반 자력

- ✍️ (a) 진행 중 스스로 구조 질문: **"y[n−1] 하나가 pole 하나 만드는거지?"** ← 정확. 💬 일반화: 피드백 최대 지연 = pole 개수(분모 차수), 입력 지연 = zero 개수(분자 차수). I2 공진기(pole 2개)가 y[n−1], y[n−2] 두 단을 쓰는 이유와 연결. 결론: 곱셈 1번짜리 피드백 항 = pole 1개 = 무한 tap FIR(0.1·0.9ⁿ)의 압축
- ✍️ (b-1) "좌우대칭 못해서 모든 주파수에 대해 똑같이 shift를 못해" ← 자력 — 한쪽 무한 꼬리 h는 대칭 불가 → linear phase 포기 (W4 재활용)
- (b-2) 안정성은 "기억 안 남" → 💬 해설: FIR은 pole이 전부 원점이라 안정성 공짜, IIR은 단위원 밖에 심을 수도 있어 체크가 의무. 날카로운 필터일수록 pole을 단위원에 바싹 붙임 → 계수 반올림 오차로도 원 밖 이탈 위험
- 💬 정리: **IIR의 거래** = 무한 tap 효과를 곱셈 몇 번에 (얻음) ↔ linear phase + 무조건적 안정성 (내줌)

### ⚠️ I4. Butterworth 프로토타입 (Phase 1 재사용) — (b)에서 연속/이산 규칙 혼동 발견·교정

- ✍️ (a) "1/(1+Ω²)" ← 자력, 정의식 N=1과 일치 확인
- ✍️ (b) "부호가 계속 바뀜" ← **이산 습관의 연속 세계 오적용**: z=−0.9는 poleⁿ(거듭제곱)이라 부호 반전이지만, s=−1은 e^(−t)(지수)라 매끈한 감쇠. 💬 규칙표 정리: 연속은 Re(s)<0=감쇠·Im(s)≠0=진동, 이산은 \|z\|<1=감쇠·angle≠0=진동 — 같은 "−1"도 세계가 다르면 의미가 다름. 이 어긋남을 잇는 게 I5 bilinear transform. τ는 "뭐였지" → 💬 복습: τ = 1/\|pole\| = 1, e^(−t/τ), ~4τ 정착 (Phase 1 삼단 대응 재장착)
- ✍️ (c) Ω≫1 "0으로 눌러붙어" ← 자력 / Ω≪1 "떨어지고" ← 방향 반대 교정: Ω<1이면 Ω^(2N)이 N↑에 따라 0으로 → gain이 1에 눌러붙음 = **maximally flat**. Ω=1은 N 무관 항상 1/2 (−3dB 컷오프 정의). N↑의 대가 = pole 수 = 계산량·phase 왜곡

### ✅ I5. Bilinear transform으로 디지털화 (이 세션의 정상) — 전부 자력 + 동기를 묻는 좋은 질문

- 시작 전 질문: **"Butterworth랑 bilinear가 뭐야? 왜 이산 다루다 갑자기 연속으로 갔어?"** → 💬 세션 전체의 동기 해설: pole 배치 최적화는 아날로그(s-평면)에서 100년 전에 해결됨(Butterworth 1930 = "좌반평면 원 위 등간격" 배치 공식, 형제로 Chebyshev·elliptic) → 직접 풀지 않고 **답안지를 번역**하는 게 표준 경로. bilinear = 좌반평면→단위원 안, 허수축→단위원을 보장하는 번역기. `signal.butter()` 한 줄의 내부가 이 두 단계
- ✍️ (a) **"(1+z⁻¹)/2"** ← 통분 자력 완주. 💬 = F1의 2-tap 이동평균! Session 2를 연 그 필터가 1차 Butterworth의 bilinear 이미지였음이 판명
- ✍️ (b) "pole 0으로 갔고 zero는 −1. 안정" ← 자력
- ✍️ (c) "고주파수 죽이네" ← 자력. 💬 아날로그 대응: 무한 허수축이 단위원에 눌려 들어가며 **Ω=∞가 z=−1(ω=π)에 착지** — "무한대에서 죽음"이 "Nyquist에서 죽음"으로 번역됨. warping 공식 Ω = tan(ω/2), 실전에선 pre-warp로 보정
- ✍️ (d) pole 착지점 z=0을 (b)에서 이미 자력 확인. 💬 보너스: 원점 착지 = 결과물이 FIR인 특수 케이스 (IIR 프로토타입 → FIR 번역)

## Python 검증 (다 푼 뒤)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# I1: 1-pole IIR vs FIR moving average
w, H_iir = signal.freqz([0.1], [1, -0.9])
w, H_fir = signal.freqz([0.5, 0.5], [1])
axes[0,0].plot(w, np.abs(H_iir), label='IIR: 0.1/(1-0.9z^-1)')
axes[0,0].plot(w, np.abs(H_fir), label='FIR: [0.5, 0.5]')
axes[0,0].set_title('I1: 1-pole IIR vs 2-tap FIR'); axes[0,0].legend()

# I2: resonator — pole 반지름 바꿔가며
for r in [0.9, 0.95, 0.99]:
    p = r * np.exp(1j*np.pi/4)
    a = np.real(np.poly([p, np.conj(p)]))  # 켤레쌍 → 실계수
    w, H = signal.freqz([1], a)
    axes[0,1].plot(w, np.abs(H), label=f'r={r}')
axes[0,1].set_title('I2: pole 반지름 vs 공진 날카로움'); axes[0,1].legend()

# I4: Butterworth 차수별 |H(jΩ)|
Omega = np.linspace(0, 3, 300)
for N in [1, 2, 4, 8]:
    axes[1,0].plot(Omega, 1/np.sqrt(1 + Omega**(2*N)), label=f'N={N}')
axes[1,0].axvline(1, color='gray', ls=':'); axes[1,0].set_title('I4: Butterworth 차수'); axes[1,0].legend()

# I5: bilinear 결과 vs scipy.signal.bilinear
b_d, a_d = signal.bilinear([1], [1, 1], fs=0.5)  # T=2
print('bilinear H(z):', b_d, a_d)  # 손 유도와 비교
w, H_d = signal.freqz(b_d, a_d)
axes[1,1].plot(w, np.abs(H_d), label='digital (bilinear)')
axes[1,1].plot(Omega[Omega<np.pi], 1/np.sqrt(1+Omega[Omega<np.pi]**2), '--', label='analog |H(jΩ)|')
axes[1,1].set_title('I5: analog vs digital'); axes[1,1].legend()

plt.tight_layout(); plt.show()
```
