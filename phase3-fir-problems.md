# Phase 3 — Session 2: FIR 필터와 윈도우 설계법

> 목표: FIR 필터를 Z-transform 틀 안에서 다루고, **zero의 위치가 주파수응답을 결정**한다는
> 감각을 세운다. Phase 0에서 암기로 넘어갔던 "이동평균=저역통과, 차분필터=고역통과"를
> 이번엔 손으로 유도해서 확실히 잡는다. 마지막엔 ideal filter → window 설계법 연결.
> 선행: phase3-ztransform-problems.md (H(z), 단위원, pole/ROC), phase0-freqresponse-problems.md (H(e^jω) 개념)

## 도구 정리

**FIR (Finite Impulse Response) 필터**: 임펄스응답 h[n]이 **유한한 길이**만 갖는 시스템.

```
y[n] = Σ_{k=0}^{M} h[k]·x[n−k]   (컨볼루션 — 이미 신호및시스템에서 배운 것)
H(z) = Σ_{k=0}^{M} h[k]·z^(−k)   (유한한 다항식, z^(−1)의 차수 M짜리)
```

**FIR의 특별한 성질**: H(z)의 분모가 없다(=1). 그러니 **pole은 전부 z=0**(원점, 단위원 안쪽 정중앙)에만 있다 — 그래서 FIR 필터는 계수를 어떻게 짜든 **항상 안정**하다. 대신 필터의 모양(주파수응답)은 전적으로 **zero의 위치**가 결정한다.

**주파수응답**: Z-transform Session 1에서 "단위원=DTFT"였다는 것 기억나지? 그러니:

```
H(e^(jω)) = H(z)|_{z=e^(jω)}
```

즉 H(z)를 단위원 위에서 평가한 게 곧 주파수응답이다. **zero가 단위원 위 또는 근처에 있으면, 그 각도(주파수)에서 H(e^jω)가 0 또는 매우 작아진다** — 이게 필터 설계의 핵심 원리.

> 표기: ✍️ = 네가 쓴 답 그대로 / 💬 = Claude가 덧붙인 해설·교정

## 문제

### ✅ F1. 2-tap 이동평균 필터: y[n] = 0.5x[n] + 0.5x[n−1] — 전부 자력

- ✍️ (선행 질문) "y[n]의 계수를 h[0], h[1]로 바로 써도 되냐"는 질문 → 💬 해설: h[n]은 정의상 x=δ[n] 입력의 응답. 피드백(y[n−1]) 항이 없는 **non-recursive(FIR)** 식은 이미 컨볼루션 형태 그 자체라 계수를 바로 읽으면 됨. IIR(Z5)은 h[n]이 무한해서 이 지름길이 안 통함
- ✍️ H(z) = 0.5 + 0.5/z ← 자력
- ✍️ zero = −1 ← 자력
- ✍️ H(e^jω) at ω=0,π: **1, 0** ← 자력
- ✍️ "저역통과. ω=π일 때 zero야" ← 자력, zero 위치와 결론 정확히 연결

### ✅ F2. 차분 필터: y[n] = 0.5x[n] − 0.5x[n−1] (Phase 0에서 헷갈렸던 필터) — 전부 자력, 복습 포인트 해소

- ✍️ H(z) = 0.5 − 0.5/z, zero at ω=0(z=1) ← 자력
- ✍️ H(e^jω) at ω=0,π: **0, 1** ← 자력
- ✍️ "고역" ← 자력. **Phase 0 진단에서 판단 못했던 문제를 이번엔 Z-transform으로 완전히 자력 해결 — 복습 포인트 해소됨**

### ⚠️ F3. 일반화: zero 위치 ↔ 주파수 감쇠 — 직관은 맞았으나 기하학적 근거는 해설 필요

- ✍️ "e^(jw)가 연속이니까 zero근처도 zero비스무리한게 나오겠지" → 💬 방향은 맞으나 정밀화: "연속이라서"가 아니라 **거리(distance)** 개념. H(z)의 인수 (z−zero)의 크기 = z와 zero 사이의 복소평면 거리. z=e^jω가 단위원 위에서 zero 위치에 가까워질수록(각도가 zero의 각도에 가까워질수록) 그 거리가 작아져서 H도 작아짐 — pole-zero plot으로 주파수응답을 스케치하는 표준 원리

### ⚠️ F4. 선형위상(linear phase) — 직관은 자력, 엄밀한 유도는 단계별 해설 후 자력 완성. 파생 질문들로 깊게 확장

- ✍️ "무게중심이 한 스텝 뒤에있어" ← 자력, `h=[0.25,0.5,0.25]`의 무게중심(=n=1)을 정확히 짚음
- 후속 질문 "왜 대칭이라는게 정확히 1만큼 민다는뜻이야" (증명 요구) → 💬 단계별 유도 가이드: H(e^jω)에서 e^(−jω) 묶어내기
  - ✍️ 괄호 정리: **0.5 + 0.5cosω** ← 자력 도달. 괄호가 순수 실수라서 위상 전체가 e^(−jω) 하나로 인수분해됨 = 정확히 1칸 지연이라는 엄밀한 근거 확인 (Z-transform Session1의 Z4 shift property 재활용)
- 파생 질문 1: "F4 필터랑 y[n]=x[n−1]은 뭐가 달라?" → 💬 해설: 순수지연(h=[0,1,0])은 |H|=1 항상(all-pass, 필터링 없음). F4는 같은 지연(e^(−jω))에 **ω마다 다른 크기(0.5+0.5cosω)**가 추가로 곱해진 것 — "지연은 보험, 크기가 실제 필터링을 담당"
- 파생 질문 2: "[0.125,0.25,0.5,0.25,0.125]는 2칸 지연?" → ✍️ 스스로 예측(맞음) → 같은 방식(e^(−j2ω) 묶기)으로 검증: H=e^(−j2ω)[0.5+0.5cosω+0.25cos2ω], 괄호 실수 확인 → **규칙: 대칭 중심 인덱스 = 지연 칸 수**
- 파생 질문 3(탭 개수 vs 필터 강도): "[0.125,0.25,0.5,0.25,0.125]가 [0,0.25,0.5,0.25,0]보다 더 강한 저역필터야?" → 💬 먼저 DC gain(계수 합) 비교부터 유도(1.25 vs 1, 정규화 필요성 확인) → 정규화 후 실제 비교: 중간 주파수는 h_A가 더 강하게 억제하지만 ω=π에서 h_A는 완전히 0이 안 되고 되레 올라감(0.2) — **비단조적 리플**, "탭 개수가 많다고 무조건 더 좋은 필터가 아니다"라는 결론
- 파생 질문 4(sinc vs Gaussian): "sinc로 하면 고주파가 더 잘 필터돼?" → 💬 개념 정정: sinc은 윈도우가 아니라 ideal 필터 자체. 진짜 비교는 "sinc을 어떤 윈도우로 자르냐"— 사각형 윈도우(날카로운 컷오프, 강한 리플) vs Gaussian 윈도우(리플 거의 없음, 넓은 전환구간)의 트레이드오프
- 파생 질문 5: "sinc을 Gaussian으로 5탭 잘라도 [0,0.25,0.5,0.25,0]보다 더 저주파필터?" → 💬 정정: 자동으로 그렇진 않음. 날카로움을 결정하는 **1순위 변수는 탭 개수(필터 길이)**, 윈도우 모양은 그 위에서 리플만 조절하는 2차 변수. 5탭이면 어떤 윈도우를 써도 원천적으로 한계

### ✅ F5. Ideal filter의 문제 → window 설계법 — 개념 방향은 자력, 세부는 해설로 보강

- ✍️ "전체에 걸쳐 0이 아니면 fir이 아니니까" ← 자력이나 절반. 💬 보강: FIR(유한길이) 위반뿐 아니라 **인과성(n<0에서도 0 아님 = 미래입력 필요)**도 동시에 위반
- ✍️ "자르면 이상적이지 않겠지" → 💬 구체화 요청(컨볼루션 정리 힌트) → ✍️ **"주파수에선 컨볼루션하는거. 주파수영역에서 꼬리가생기나"** ← 자력으로 정확한 방향(컨볼루션 정리 적용, side-lobe로 인한 "꼬리") 도달 → 💬 명명: **Gibbs phenomenon**, F4의 "윈도우 모양이 성능을 결정" 결론과 연결됨

## Python 검증 (다 푼 뒤)

```python
import numpy as np
import matplotlib.pyplot as plt

def freq_response(h, worN=512):
    w = np.linspace(0, np.pi, worN)
    H = np.array([sum(hk * np.exp(-1j*wk*k) for k, hk in enumerate(h)) for wk in w])
    return w, H

filters = {
    'F1 moving avg [0.5, 0.5]': [0.5, 0.5],
    'F2 difference [0.5, -0.5]': [0.5, -0.5],
}

fig, ax = plt.subplots(figsize=(8, 5))
for label, h in filters.items():
    w, H = freq_response(h)
    ax.plot(w, np.abs(H), label=label)

ax.set_xlabel('omega (0 ~ pi)'); ax.set_ylabel('|H(e^jw)|')
ax.set_title('F1 vs F2 frequency response')
ax.legend(); ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()

# F5: ideal lowpass sinc를 rectangular window로 자른 뒤 실제 주파수응답 (Gibbs 리플 확인)
wc = np.pi/4
N = 21
n = np.arange(-(N//2), N//2+1)
h_ideal = np.where(n==0, wc/np.pi, np.sin(wc*n)/(np.pi*n))
w, H = freq_response(np.roll(h_ideal, -(N//2)))  # causal shift
plt.figure(figsize=(8,5))
plt.plot(w, np.abs(H))
plt.axvline(wc, color='gray', linestyle=':', label='cutoff wc')
plt.title(f'Windowed ideal lowpass (N={N}) — Gibbs ripple 확인')
plt.legend(); plt.grid(True, alpha=0.4)
plt.show()
```
