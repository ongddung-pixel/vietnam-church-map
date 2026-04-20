import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- [중요] 지부장님의 구글 시트 웹 게시 URL을 여기에 붙여넣으세요 ---
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQK02XkY_Hh8I448_A7TYorUfhy9u_3ufzONkqVfX8nCi_8uwID-0u6mHtCdcdkj9TmSDghEKj7H75h/pub?output=csv" "여기에_복사한_주소를_넣으세요"

st.set_page_config(page_title="베트남 사역 실시간 지도", layout="wide")
st.title("🇻🇳 베트남 교회 사역 실시간 공유 시스템")

# 데이터를 구글 시트에서 직접 가져오는 함수
@st.cache_data(ttl=600) # 10분마다 데이터를 새로고침합니다
def load_data():
    return pd.read_csv(GOOGLE_SHEET_URL)

try:
    df = load_data()
    
    # 지도 생성
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)

    for index, row in df.iterrows():
        info_text = f"<b>{row['Name']}</b><br>지도자: {row['Leader']}<br>연락처: {row['Phone']}"
        
        category_str = str(row['Category'])
        map_color = "blue" if "건축" in category_str else "red" if "일반" in category_str else "orange"
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(info_text, max_width=300),
            tooltip=row['Name'],
            icon=folium.Icon(color=map_color, icon='plus', prefix='glyphicon')
        ).add_to(m)

    st_folium(m, width="100%", height=600)
    st.subheader("📋 실시간 사역 현황 (구글 시트 연동)")
    st.dataframe(df)

except Exception as e:
    st.error("구글 시트 데이터를 불러오지 못했습니다. URL을 확인해 주세요.")