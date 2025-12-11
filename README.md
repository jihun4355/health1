# 🏋️ 헬스 일지 기록 시스템 (Streamlit Health Log App)

개인 운동 기록을 쉽게 저장하고, 체성분 변화 그래프, 중량 추천, 최대 중량 관리까지 지원하는  
**Streamlit 기반 헬스 기록 웹 애플리케이션**입니다.  
모든 기록은 사용자 ID별로 파일이 자동 생성되어 관리됩니다.

---

## 📄 주요 기능

### 1️⃣ 운동 기록 저장
- 날짜별 운동 종목, 부위, 중량, 횟수, 세트, 피로도 입력  
- 저장 시 자동으로 사용자별 CSV 파일(`{user}_workout_log.csv`) 생성  
- 운동 기록 입력과 함께 **최대 중량 자동 업데이트**

### 2️⃣ 체성분(BMI) 기록
- 키, 체중, 골격근량, 체지방률 입력  
- BMI 자동 계산  
- 사용자별 CSV(`{user}_body_log.csv`)로 저장  

### 3️⃣ 그래프 분석 (Streamlit Line Charts)
- 날짜별 **총중량 변화 그래프**  
- 피로도 변화  
- 체중 / 골격근량 / 체지방률 / BMI 시계열 분석  

### 4️⃣ 중량 추천 계산기
- max_weights.json 기반  
- 등록된 유저의 최대 중량 × 비율(%)로 적정 중량 추천  
- 예: 80%로 운동하고 싶을 때 자동 계산

### 5️⃣ 전체 기록 조회 및 삭제 기능
- 운동 기록을 카드 형태로 표시  
- ❌ 버튼으로 개별 기록 삭제  
- 체성분 기록 전체 조회도 지원

---

## 🗂 프로젝트 파일 구조

📁 project_root
│── health.py # Streamlit 메인 앱 
health
│── devcontainer.json # 개발환경 설정 
devcontainer
│── requirements.txt # 필요 라이브러리 
requirements
│── max_weights.json # 사용자 최대 중량 
max_weights
│── workout_log.csv # (자동 생성) 운동 기록
│── body_log.csv # (자동 생성) 체성분 기록
│── health_records.csv # (자동 생성)
│── README.md # 프로젝트 소개 문서


---

## 🚀 실행 방법

### 1) 가상환경 설치(선택)


python -m venv venv
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)


### 2) 필요 패키지 설치


pip install -r requirements.txt


### 3) Streamlit 실행


streamlit run health.py


### 4) 웹 브라우저에서 접속
Streamlit이 자동으로 다음과 같은 URL을 열어줍니다:



http://localhost:8501


---

## 🧠 코드 구조 요약

### ✔ 사용자별 파일 관리 (health.py)
- 입력한 user_id 기반으로 파일명을 다음처럼 생성:

```python
def get_user_filename(base_file):
    name, ext = os.path.splitext(base_file)
    return f"{user_id}_{name}{ext}"
