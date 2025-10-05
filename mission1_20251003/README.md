# 미션 1: 야놀자 리뷰 요약

## 📌 미션 정보

- **날짜**: 2025.10.03 (금)
- **학습 범위**: Part4 - 야놀자 리뷰 요약
- **제출 기한**: 2025.10.03 23:59

---

## 🎯 학습 목표

이 미션에서는 야놀자 숙박 리뷰 데이터를 활용하여 리뷰를 요약하는 AI 서비스를 개발합니다.

### 주요 학습 내용
- LLM을 활용한 텍스트 요약
- 프롬프트 엔지니어링 기초
- 리뷰 데이터 전처리 및 분석

---

## 📝 실습 내용

### 구현 기능
- [ ] 야놀자 리뷰 데이터 수집/로드
- [ ] 리뷰 데이터 전처리
- [ ] LLM을 활용한 리뷰 요약
- [ ] 요약 결과 평가

### 사용 기술
- Python
- OpenAI API / LangChain
- Jupyter Notebook

---

## 💻 실행 방법

```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# Jupyter Notebook 실행
jupyter notebook

# 또는 Python 파일 실행
python main.py
```

---

## 📊 실행 결과

> 이곳에 실행 결과 스크린샷이나 출력 내용을 추가하세요!
[alt text](image.png)

```
예시:
원본 리뷰: "위치가 좋고 방도 깨끗했습니다. 다만 조식이 아쉬웠어요..."
요약 결과: "위치와 청결도는 우수하나 조식 개선 필요"
```

---

## 🤔 학습 내용 정리

### 배운 점
- 숙소 리뷰(JSON 파일)를 크롤링해와 요약하는 파이프라인을 구축
- OpenAI API를 이용해 다양한 요약 생성 실험
- MT-Bench 스타일 **pairwise 평가**를 적용해 모델 출력 품질 비교
- 목표: **리뷰 요약 자동화** 및 **평가 자동화** 경험


### 처리 흐름
## ⚙️ 처리 흐름

### 1. 라이브러리 임포트 및 환경 설정
- `openai`, `datetime`, `json` 등 필요 모듈 로드  
- 환경 변수(`.env`) 로드 및 API 키 설정  

---

### 2. 데이터 로드 및 전처리
- 리뷰 JSON 파일 읽기 (`json.load`)  
- 날짜 필터링으로 최근 N개월 리뷰만 사용  
- 평점 기준으로 좋은 / 나쁜 리뷰 분리  
- 리뷰 개수 제한 (예: `reviews_good[:30]`)  
- 토큰 기반으로 초과 입력 컷 (`truncate_text_by_tokens`)  

---

### 3. 프롬프트 설계
- 기본 요약 지시문(Baseline Prompt) 구성  
- 예시를 포함한 `1-shot`, `2-shot` 형태의 프롬프트 설계  
- 프롬프트와 리뷰를 조합하는 방식 정의  

---

### 4. 요약 생성 함수 (`summarize`)

---

### 5. 샘플 생성 및 비교
- 동일한 리뷰에 대해 여러 번 요약 생성 (`for _ in range(eval_count)`)  
- 결과를 리스트 형태로 저장  

---

### 6. Pairwise 평가
- MT-Bench 구조 참고  
- A와 B 요약을 나란히 제시하고 심판 모델이 `[[A]]`, `[[B]]`로 판정  
- `pairwise_eval_batch()`로 여러 쌍을 일괄 평가 → Wins, Losses, Ties 집계  

---

### 7. 결과 분석 및 시각화
- 평가 결과를 바탕으로 요약 품질 비교  
- `Gradio`를 이용해 UI 구성, 요약 결과를 직접 테스트할 수 있도록 구현  


### 어려웠던 점
gpt-3.5-turbo-0125 모델의 16K 토큰 제한으로 인해 BadRequestError(400)가 자주 발생했음
리뷰 데이터가 많을 경우 입력 토큰이 초과되어 모델 호출이 실패하는 문제가 반복됨
이를 해결하기 위해 전처리 단계에서

```python
reviews_good[:min(len(reviews_good), 30)]
```

형태로 리뷰 개수를 30개로 제한하고,
tiktoken을 사용해 토큰 수를 직접 계산하여 초과 입력을 자르는 함수를 추가

```python
def truncate_text_by_tokens(text, model="gpt-3.5-turbo-0125", max_tokens=6000):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    if len(tokens) > max_tokens:
        print(f"{len(tokens)} → {max_tokens}로 잘라냅니다.")
        tokens = tokens[:max_tokens]
    return enc.decode(tokens)
```

하지만 이렇게 잘라내면 일부 문맥이 손실되어 “정확한 요약이 되는지”에 대한 의문이 남았음


---
**작성자**: [최지선]  
**작성일**: 2025.10.05

