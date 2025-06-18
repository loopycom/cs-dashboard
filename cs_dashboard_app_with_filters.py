import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📊 CS Dashboard (with Filters)")

uploaded_file = st.file_uploader("📂 문의내역 엑셀 업로드", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "날짜" in df.columns:
        df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    with st.sidebar:
        st.header("🔍 필터")
        min_date = df["날짜"].min()
        max_date = df["날짜"].max()
        start_date, end_date = st.date_input("날짜 범위", [min_date, max_date])

        문의유형_컬럼명 = [col for col in df.columns if "유형" in col or "카테고리" in col]
        type_column = 문의유형_컬럼명[0] if 문의유형_컬럼명 else None
        if type_column:
            selected_types = st.multiselect("문의 유형 선택", options=df[type_column].dropna().unique(), default=df[type_column].dropna().unique())
        else:
            selected_types = None

    filtered_df = df[
        (df["날짜"] >= pd.to_datetime(start_date)) &
        (df["날짜"] <= pd.to_datetime(end_date))
    ]
    if selected_types and type_column:
        filtered_df = filtered_df[filtered_df[type_column].isin(selected_types)]

    st.markdown("### ✅ 요약 지표")
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 문의 수", len(filtered_df))
    col2.metric("답변 완료", filtered_df["상태"].str.contains("완료").sum() if "상태" in filtered_df.columns else "-")
    col3.metric("미답변 수", filtered_df["상태"].str.contains("대기|미답", na=False).sum() if "상태" in filtered_df.columns else "-")

    st.markdown("### 📈 일자별 인입 추이")
    if "날짜" in filtered_df.columns:
        daily_counts = filtered_df.groupby(filtered_df["날짜"].dt.date).size().reset_index(name="건수")
        fig = px.line(daily_counts, x="날짜", y="건수", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    if type_column:
        st.markdown("### 🧭 유형별 분포")
        type_counts = filtered_df[type_column].value_counts().reset_index()
        type_counts.columns = ["유형", "건수"]
        fig2 = px.pie(type_counts, names="유형", values="건수", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 필터링된 데이터 보기"):
        st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("왼쪽 상단에서 문의내역 엑셀 파일을 업로드해주세요.")

