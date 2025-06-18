
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CS 대시보드", layout="wide")
st.title("📊 CS 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("문의내역 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    df["문의 생성 일자"] = pd.to_datetime(df["문의 생성 일자"])
    df["답변 상태"] = df["답변 생성 일자"].notnull().map({True: "답변 완료", False: "답변 대기"})

    st.markdown("### ✅ 요약 지표")
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 문의 수", len(df))
    col2.metric("답변 완료", df["답변 상태"].value_counts().get("답변 완료", 0))
    col3.metric("답변 대기", df["답변 상태"].value_counts().get("답변 대기", 0))

    # 일별 추이
    st.markdown("### 📈 일별 인입 추이")
    daily_inquiry = df.groupby(df["문의 생성 일자"].dt.date).size().reset_index(name="문의 수")
    fig1 = px.line(daily_inquiry, x="문의 생성 일자", y="문의 수", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # 유형별 분포
    st.markdown("### 🥧 문의 유형 분포")
    type_counts = df["유형"].value_counts().reset_index()
    type_counts.columns = ["유형", "건수"]
    fig2 = px.pie(type_counts, names="유형", values="건수", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # 답변 상태
    st.markdown("### 📊 답변 상태")
    status_counts = df["답변 상태"].value_counts().reset_index()
    status_counts.columns = ["답변 상태", "건수"]
    fig3 = px.bar(status_counts, x="답변 상태", y="건수", text="건수")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("왼쪽에서 엑셀 파일을 업로드해주세요.")
