
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
    "인클라인 덤벨프레스", "인클라인 머신 프레스", "인클라인 덤벨 플라이", "디클라인 프레스",
    "딥스", "슈러그", "랫풀다운", "티바로우", "시티드 로우", "dy로우", "원암풀다운",
    "어시스트 풀업", "페이스 풀", "덤벨 숄더 프레스", "머신 숄더 프레스", "비하인드 넥 프레스",
    "덤벨 사이드 레테럴 레이즈", "케이블 사이드 레테럴 레이즈", "업라이트 로우", "리어델트 플라이",
    "레그 컬", "레그 프레스", "핵프레스", "레그 익스텐션", "바벨 컬", "해머 컬",
    "프리처컬", "케이블 푸시다운", "라잉 트라이셉스 익스텐션"
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
