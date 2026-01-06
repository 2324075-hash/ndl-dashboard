import streamlit as st
import pandas as pd
import plotly.express as px

# ページの設定
st.set_page_config(page_title="NDL統計分析", layout="wide")

st.title("🏛 国立国会図書館 統計ダッシュボード")
st.caption("出典：国立国会図書館年報 令和6年版（令和5年度実績統計）に基づき作成")

# 1. 確定実績データ（西暦表記に変更）
# 2023年(R5)末までの最新数値を反映
data = {
    "年度": [2019, 2020, 2021, 2022, 2023],
    "図書(万冊)": [1153.9, 1172.5, 1191.1, 1209.7, 1246.9], 
    "デジタル化資料(万点)": [298.1, 313.2, 329.0, 362.4, 446.0], 
    "来館者数(万人)": [72.8, 15.6, 18.2, 61.0, 67.0]
}
df = pd.DataFrame(data)

# 2. サイドバー
st.sidebar.header("表示期間設定")
selected_range = st.sidebar.slider("対象年度", 2019, 2023, (2019, 2023))

# フィルタリング
df_filtered = df[(df["年度"] >= selected_range[0]) & (df["年度"] <= selected_range[1])]

# 3. 指標表示
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("最新の蔵書数", f"{df['図書(万冊)'].iloc[-1]}万冊")
with c2:
    st.metric("デジタル化累計", f"{df['デジタル化資料(万点)'].iloc[-1]}万点")
with c3:
    st.metric("最新の来館者数", f"{df['来館者数(万人)'].iloc[-1]}万人")

# 4. グラフ
st.subheader("📊 統計データの推移")
col_a, col_b, col_c = st.columns(3)

# X軸を西暦として正しく表示（整数表示）
with col_a:
    fig1 = px.line(df_filtered, x="年度", y="図書(万冊)", title="図書所蔵数の推移", markers=True)
    fig1.update_xaxes(dtick=1) # 1年刻み
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = px.area(df_filtered, x="年度", y="デジタル化資料(万点)", title="デジタル化資料の加速(万点)", color_discrete_sequence=['#00CC96'])
    fig2.update_xaxes(dtick=1)
    st.plotly_chart(fig2, use_container_width=True)

with col_c:
    fig3 = px.bar(df_filtered, x="年度", y="来館者数(万人)", title="来館者数の変化(万人)", color_discrete_sequence=['#FF4B4B'])
    fig3.update_xaxes(dtick=1)
    st.plotly_chart(fig3, use_container_width=True)

# 5. データ表
st.subheader("📋 根拠データ一覧")
st.dataframe(df_filtered, use_container_width=True)