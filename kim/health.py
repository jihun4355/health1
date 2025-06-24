# import csv
# import json
# import os
# from datetime import datetime
# import matplotlib.pyplot as plt
# import pandas as pd

# WORKOUT_FILE = "workout_log.csv"
# BODY_FILE = "body_log.csv"
# MAX_WEIGHT_FILE = "max_weights.json"

# EQUIPMENTS = [
#     "시티드 로우", "힙 (이너)", "힙 (아웃)", "레그 익스텐션", "레그 컬", "레그 프레스",
#     "와이드 스쿼트", "힙 쓰러스트", "몬스터 글루트", "덤벨 숄더 프레스", "티 바 로우",
#     "랫 풀 다운", "덤벨 컬", "케이블 푸시 다운", "핵 스쿼트", "플랭크", "하이 로우",
#     "밀리터리 프레스", "사이드 레터럴 레이즈", "런지", "숄더 프레스", "로우", "케이블 풀 스루",
#     "V-Sit Up", "스티프 데드리프트", "백 익스텐션", "덤벨 킥 백", "스쿼트", "바벨 백 스쿼트",
#     "어시스트 풀 업", "스미스 머신 스쿼트", "체스트 프레스", "케틀벨 스윙", "스모 데드리프트",
#     "암 풀 다운", "아이소 레터럴 로우", "스미스 밀리터리 프레스", "케이블 프론트 레이즈"
# ]

# def load_max_weights():
#     if os.path.exists(MAX_WEIGHT_FILE):
#         with open(MAX_WEIGHT_FILE, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return {}

# def save_max_weights(data):
#     with open(MAX_WEIGHT_FILE, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)

# def select_equipment():
#     for idx, eq in enumerate(EQUIPMENTS):
#         print(f"{idx + 1}. {eq}")
#     index = int(input("운동 종목 번호 선택: ")) - 1
#     return EQUIPMENTS[index]

# def record_workout():
#     date = input("날짜 (빈칸 = 오늘): ") or datetime.today().strftime("%Y-%m-%d")
#     equipment = select_equipment()
#     part = input("운동 부위: ")
#     weight = float(input("무게(kg): "))
#     reps = int(input("횟수: "))
#     sets = int(input("세트: "))
#     fatigue = int(input("운동 후 피로도 (1~10): "))

#     max_data = load_max_weights()
#     if equipment not in max_data or weight > max_data[equipment]:
#         max_data[equipment] = weight
#         save_max_weights(max_data)

#     row = {
#         "날짜": date, "종목": equipment, "부위": part, "무게": weight,
#         "횟수": reps, "세트": sets, "피로도": fatigue
#     }
#     save_row(WORKOUT_FILE, row)
#     print("✅ 운동 기록 저장 완료")

# def record_body():
#     date = input("날짜 (빈칸 = 오늘): ") or datetime.today().strftime("%Y-%m-%d")
#     height = float(input("키 (cm): "))
#     weight = float(input("체중 (kg): "))
#     muscle = float(input("골격근량 (kg): "))
#     fat = float(input("체지방률 (%): "))
#     bmi = round(weight / ((height / 100) ** 2), 2)

#     row = {
#         "날짜": date, "키": height, "체중": weight,
#         "골격근량": muscle, "체지방률": fat, "BMI": bmi
#     }
#     save_row(BODY_FILE, row)
#     print("✅ 체성분 기록 저장 완료")

# def save_row(file, row):
#     file_exists = os.path.exists(file)
#     with open(file, 'a', newline='', encoding='utf-8-sig') as f:
#         writer = csv.DictWriter(f, fieldnames=row.keys())
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(row)

# def recommend_weight():
#     equipment = select_equipment()
#     max_data = load_max_weights()
#     if equipment in max_data:
#         percent = float(input("사용할 비율 (예: 60, 80): "))
#         rec = round(max_data[equipment] * (percent / 100), 1)
#         print(f"👉 추천 중량: {rec}kg (최대 {max_data[equipment]}kg의 {percent}%)")
#     else:
#         print("❗ 해당 종목의 최대 중량 정보 없음")

# def plot_graph(data, x_key, y_key, title, ylabel):
#     if data.empty:
#         print("❗ 데이터가 없습니다.")
#         return
#     plt.plot(data[x_key], data[y_key], marker='o')
#     plt.title(title)
#     plt.xlabel("날짜")
#     plt.ylabel(ylabel)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# def show_graphs():
#     workout_df = pd.read_csv(WORKOUT_FILE, encoding="utf-8-sig") if os.path.exists(WORKOUT_FILE) else pd.DataFrame()
#     body_df = pd.read_csv(BODY_FILE, encoding="utf-8-sig") if os.path.exists(BODY_FILE) else pd.DataFrame()

#     if not workout_df.empty:
#         workout_df["총중량"] = workout_df["무게"] * workout_df["횟수"] * workout_df["세트"]
#         plot_graph(workout_df, "날짜", "총중량", "운동 성과 그래프", "총중량 (kg)")
#         plot_graph(workout_df, "날짜", "피로도", "피로도 변화", "피로도")

#     if not body_df.empty:
#         plot_graph(body_df, "날짜", "체중", "체중 변화", "체중 (kg)")
#         plot_graph(body_df, "날짜", "BMI", "BMI 변화", "BMI")

# def main():
#     print("\n==== 🏋️ 두 파일 기반 헬스 시스템 ====")
#     while True:
#         print("\n1. 운동 기록")
#         print("2. 체성분 기록")
#         print("3. 중량 추천")
#         print("4. 그래프 보기")
#         print("5. 종료")

#         choice = input("번호 선택: ")
#         if choice == "1": record_workout()
#         elif choice == "2": record_body()
#         elif choice == "3": recommend_weight()
#         elif choice == "4": show_graphs()
#         elif choice == "5":
#             print("👋 종료합니다.")
#             break
#         else:
#             print("❗ 잘못된 입력")

# if __name__ == "__main__":
#     main()























# import streamlit as st
# import pandas as pd
# import datetime
# import os

# FILE_PATH = "health_records.csv"

# # 🏋️‍♀️ 운동 종목 정의
# exercise_dict = {
#     1: "시티드 로우", 2: "힙 (이너)", 3: "힙 (아웃)", 4: "레그 익스텐션",
#     5: "레그 컬", 6: "레그 프레스", 7: "와이드 스쿼트", 8: "힙 쓰러스트",
#     9: "몬스터 글루트", 10: "덤벨 숄더 프레스", 11: "티 바 로우", 12: "랫 풀 다운",
#     13: "덤벨 컬", 14: "케이블 푸시 다운", 15: "핵 스쿼트", 16: "플랭크",
#     17: "하이 로우", 18: "밀리터리 프레스", 19: "사이드 레터럴 레이즈", 20: "런지",
#     21: "숄더 프레스", 22: "로우", 23: "케이블 풀 스루", 24: "V-Sit Up",
#     25: "스티프 데드리프트", 26: "백 익스텐션", 27: "덤벨 킥 백", 28: "스쿼트",
#     29: "바벨 백 스쿼트", 30: "어시스트 풀 업", 31: "스미스 머신 스쿼트",
#     32: "체스트 프레스", 33: "케틀벨 스윙", 34: "스모 데드리프트", 35: "암 풀 다운",
#     36: "아이소 레터럴 로우", 37: "스미스 밀리터리 프레스", 38: "케이블 프론트 레이즈"
# }

# # 📄 초기 CSV 파일 생성
# if not os.path.exists(FILE_PATH):
#     df_init = pd.DataFrame(columns=["날짜", "종목", "운동 부위", "무게", "횟수", "세트", "피로도"])
#     df_init.to_csv(FILE_PATH, index=False)

# # 🔷 사이드바 메뉴
# menu = st.sidebar.radio("📌 메뉴 선택", ["운동 기록", "기록 확인", "종목 번호표"])

# # ===============================
# # 🏋️‍♂️ 운동 기록 입력
# # ===============================
# if menu == "운동 기록":
#     st.title("🏋️ 헬스 일지 기록 시스템")
#     st.subheader("운동 기록 입력")

#     # 입력 폼
#     with st.form(key="input_form"):
#         date = st.date_input("날짜", datetime.date.today())
#         exercise_number = st.number_input("종목 번호", min_value=1, max_value=len(exercise_dict), step=1)
#         part = st.text_input("운동 부위", placeholder="예: 어깨, 하체, 등")
#         weight = st.number_input("무게 (kg)", min_value=0.0, step=1.0)
#         reps = st.number_input("횟수", min_value=1, step=1)
#         sets = st.number_input("세트", min_value=1, step=1)
#         fatigue = st.slider("피로도 (1-10)", 1, 10, 5)

#         submit = st.form_submit_button("저장")

#     # 저장 처리
#     if submit:
#         record = {
#             "날짜": date.strftime("%Y-%m-%d"),
#             "종목": exercise_dict.get(exercise_number, f"번호 {exercise_number}"),
#             "운동 부위": part,
#             "무게": weight,
#             "횟수": reps,
#             "세트": sets,
#             "피로도": fatigue
#         }
#         df = pd.read_csv(FILE_PATH)
#         df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
#         df.to_csv(FILE_PATH, index=False)
#         st.success("✅ 운동 기록이 저장되었습니다.")

# # ===============================
# # 📊 기록 확인
# # ===============================
# elif menu == "기록 확인":
#     st.title("📊 운동 기록 전체 보기")
#     df = pd.read_csv(FILE_PATH)

#     if df.empty:
#         st.info("아직 입력된 기록이 없습니다.")
#     else:
#         df["날짜"] = pd.to_datetime(df["날짜"])
#         df_sorted = df.sort_values(by="날짜", ascending=False)
#         st.dataframe(df_sorted, use_container_width=True)

# # ===============================
# # 🧾 종목 번호표
# # ===============================
# elif menu == "종목 번호표":
#     st.title("📘 운동 종목 번호표")
#     ex_df = pd.DataFrame(list(exercise_dict.items()), columns=["번호", "운동 종목"])
#     st.dataframe(ex_df, use_container_width=True)













import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

WORKOUT_FILE = "workout_log.csv"
BODY_FILE = "body_log.csv"
MAX_WEIGHT_FILE = "max_weights.json"

EQUIPMENTS = [
        ”인클라인 덤벨프레스“, ”인클라인 머신 프레스“, 인클라인 덤벨 플라이”, “디클라인 프레스”,
        “딥스”, “슈러그”, “랫풀다운”, “티바로우”, “시티드 로우”, “dy로우”, “원암풀다운”, 
        “어시스트 풀업”, “페이스 풀”, “덤벨 숄더 프레스”, “머신 숄더 프레스”, “비하인드 넥 프레스”, 
        “덤벨 사이드 레테럴 레이즈“, ”케이블 사이드 레테럴 레이즈“, ”업라이트 로우“, ”리어델트 플라이“, 
        ”레그 컬“, ”레그 프레스“, ”핵프레스“, ”레그 익스텐션“, ”바벨 컬“, ”해머 컬“, 
        ”프리처컬“, ”케이블 푸시다운“, ”라잉 트라이셉스 익스텐션“
]

st.set_page_config(page_title="🏋️‍♂️ 헬스 일지", layout="wide")
st.title("🏋️‍♂️ 헬스 일지 기록 시스템")

def load_df(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

def save_row(file, row):
    df = load_df(file, list(row.keys()))
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(file, index=False, encoding='utf-8-sig')

def load_max_weights():
    if os.path.exists(MAX_WEIGHT_FILE):
        with open(MAX_WEIGHT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_max_weights(data):
    with open(MAX_WEIGHT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏋️ 운동 기록", "📊 체성분 기록", "📈 그래프", "🔢 중량 추천", "📖 전체 기록 보기"])

with tab1:
    st.subheader("운동 기록 입력")
    with st.expander("📋 운동 종목 리스트"):
        ex_df = pd.DataFrame({"번호": list(range(1, len(EQUIPMENTS)+1)), "운동 종목": EQUIPMENTS})
        st.dataframe(ex_df, use_container_width=True, height=300)

    with st.form("workout_form"):
        date = st.date_input("날짜", value=datetime.today()).strftime('%Y-%m-%d')
        ex_index = st.number_input("종목 번호", min_value=1, max_value=len(EQUIPMENTS), step=1)
        exercise = EQUIPMENTS[ex_index - 1]
        part = st.text_input("운동 부위")
        weight = st.number_input("무게 (kg)", 0.0)
        reps = st.number_input("횟수", 1, step=1)
        sets = st.number_input("세트", 1, step=1)
        fatigue = st.slider("피로도 (1~10)", 1, 10)
        submit = st.form_submit_button("저장")

        if submit:
            row = {"날짜": date, "종목": exercise, "부위": part, "무게": weight, "횟수": reps, "세트": sets, "피로도": fatigue}
            save_row(WORKOUT_FILE, row)
            max_weights = load_max_weights()
            if exercise not in max_weights or weight > max_weights[exercise]:
                max_weights[exercise] = weight
                save_max_weights(max_weights)
            st.success("✅ 운동 기록 저장 완료")

with tab2:
    st.subheader("체성분 입력")
    with st.form("body_form"):
        date = st.date_input("날짜", value=datetime.today(), key="body_date").strftime('%Y-%m-%d')
        height = st.number_input("키 (cm)", 0.0)
        weight = st.number_input("체중 (kg)", 0.0)
        muscle = st.number_input("골격근량 (kg)", 0.0)
        fat = st.number_input("체지방률 (%)", 0.0)
        bmi = round(weight / ((height / 100) ** 2), 2) if height > 0 else 0
        submit2 = st.form_submit_button("저장")

        if submit2:
            row = {"날짜": date, "키": height, "체중": weight, "골격근량": muscle, "체지방률": fat, "BMI": bmi}
            save_row(BODY_FILE, row)
            st.success(f"✅ 체성분 저장 완료! BMI: {bmi}")

with tab3:
    st.subheader("📈 운동 및 체성분 변화 그래프")
    body_df = load_df(BODY_FILE, ["날짜", "키", "체중", "골격근량", "체지방률", "BMI"])
    workout_df = load_df(WORKOUT_FILE, ["날짜", "종목", "부위", "무게", "횟수", "세트", "피로도"])

    if not workout_df.empty:
        workout_df['날짜'] = pd.to_datetime(workout_df['날짜'])
        workout_df['총중량'] = workout_df['무게'] * workout_df['횟수'] * workout_df['세트']
        st.line_chart(workout_df.set_index('날짜')["총중량"], height=250, use_container_width=True)
        st.line_chart(workout_df.set_index('날짜')["피로도"], height=250, use_container_width=True)

    if not body_df.empty:
        body_df['날짜'] = pd.to_datetime(body_df['날짜'])
        for col in ["체중", "골격근량", "체지방률", "BMI"]:
            st.line_chart(body_df.set_index('날짜')[col], height=250)

with tab4:
    st.subheader("📌 중량 추천 계산기")
    max_data = load_max_weights()
    if not max_data:
        st.warning("❗ 등록된 최대 중량 데이터가 없습니다.")
    else:
        exercise = st.selectbox("운동 종목 선택", list(max_data.keys()))
        ratio = st.slider("사용 비율 (%)", 10, 100, 70)
        recommended = round(max_data[exercise] * (ratio / 100), 1)
        st.metric(label="추천 중량 (kg)", value=f"{recommended}kg", delta=f"{ratio}% of {max_data[exercise]}kg")

with tab5:
    st.subheader("📖 전체 기록 보기")
    df_workout = load_df(WORKOUT_FILE, ["날짜", "종목", "부위", "무게", "횟수", "세트", "피로도"])
    df_body = load_df(BODY_FILE, ["날짜", "키", "체중", "골격근량", "체지방률", "BMI"])

    if not df_workout.empty:
        st.markdown("### 🏋️ 운동 기록")
        st.dataframe(df_workout.sort_values(by="날짜", ascending=False), use_container_width=True)
    else:
        st.info("운동 기록이 없습니다.")

    if not df_body.empty:
        st.markdown("### 📊 체성분 기록")
        st.dataframe(df_body.sort_values(by="날짜", ascending=False), use_container_width=True)
    else:
        st.info("체성분 기록이 없습니다.")
