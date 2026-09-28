from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data/processed/financial_metrics.csv"
PEERS=ROOT/"data/peers.csv"

st.set_page_config(page_title="SK hynix DART Financial Dashboard", page_icon="📊", layout="wide")
st.title("SK hynix DART Financial Dashboard")
st.caption("OpenDART · 연결재무제표(CFS) · 사업보고서/반기/분기보고서 · 자동 업데이트")

if not DATA.exists():
    st.warning("아직 분석 데이터가 없습니다. GitHub Actions에서 DART 수집 워크플로우를 실행하세요.")
    st.stop()

df=pd.read_csv(DATA)
df["label"]=df["year"].astype(str)+" "+df["period"]

c1,c2,c3,c4=st.columns(4)
latest=df.iloc[-1]
c1.metric("최근 매출", f"{latest['revenue']/1e12:,.1f}조원" if pd.notna(latest['revenue']) else "-")
c2.metric("최근 영업이익", f"{latest['operating_income']/1e12:,.1f}조원" if pd.notna(latest['operating_income']) else "-")
c3.metric("영업이익률", f"{latest['operating_margin']*100:,.1f}%" if pd.notna(latest['operating_margin']) else "-")
c4.metric("순차입금", f"{latest['net_debt']/1e12:,.1f}조원" if pd.notna(latest['net_debt']) else "-")

left,right=st.columns(2)
with left:
    fig=px.line(df,x="label",y=["revenue","operating_income","net_income"],markers=True,title="매출·영업이익·순이익 추이")
    fig.update_yaxes(tickformat=".2s")
    st.plotly_chart(fig,use_container_width=True)
with right:
    fig=px.line(df,x="label",y=["operating_margin","net_margin"],markers=True,title="수익성 추이")
    fig.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("현금흐름·재무안정성")
left,right=st.columns(2)
with left:
    fig=px.bar(df,x="label",y=["cfo","fcf"],barmode="group",title="영업현금흐름·FCF")
    st.plotly_chart(fig,use_container_width=True)
with right:
    fig=px.line(df,x="label",y=["current_ratio","debt_ratio","equity_ratio"],markers=True,title="유동비율·부채비율·자기자본비율")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Annual")
st.dataframe(df[df.period=="annual"].sort_values("year",ascending=False).reset_index(drop=True),use_container_width=True,hide_index=True)
st.subheader("Half-year")
st.dataframe(df[df.period=="half-year"].sort_values("year",ascending=False).reset_index(drop=True),use_container_width=True,hide_index=True)
st.subheader("Quarterly")
st.dataframe(df[df.period.isin(["q1","q3"])].sort_values(["year","period"],ascending=False).reset_index(drop=True),use_container_width=True,hide_index=True)

st.subheader("국내 Peer Firms")
if PEERS.exists(): st.dataframe(pd.read_csv(PEERS),use_container_width=True,hide_index=True)
else: st.info("peer firms 데이터 파일이 없습니다.")

st.caption("자료: 금융감독원 OpenDART. OpenDART 구조화 재무제표 API의 제공기간 제한으로 2010~2014년은 자동 재무수치 산출 대상에서 제외됩니다.")
