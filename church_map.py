import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- [1] 지부장님이 주신 구글 시트 URL 연결 ---
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQK02XkY_Hh8I448_A7TYorUfhy9u_3ufzONkqVfX8nCi_8uwID-0u6mHtCdcdkj9TmSDghEKj7H75h/pubhtml"

# 웹 페이지 설정
st.set_page_config(page_title="베트남 사역 실시간 지도", layout="wide")
st.title("🇻🇳 베트남 교회 사역 실시간 현황판")
st.markdown("지부장님이 구글 시트를 수정하면 이 지도는 **실시간으로 자동 업데이트**됩니다.")

# 데이터를 구글 시트에서 가져오는 함수
@st.cache_data(ttl=60) # 1분마다 새로운 데이터가 있는지 확인합니다
def load_data():
    try:
        # 구글 시트 읽기
        data = pd.read_csv(GOOGLE_SHEET_URL)
        return data
    except Exception as e:
        st.error(f"구글 시트에 연결할 수 없습니다: {e}")
        return None

# 데이터 불러오기 실행
df = load_data()

if df is not None:
    try:
        # 1. 지도 생성 (데이터에 등록된 모든 교회의 중앙 지점 찾기)
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)

        # 2. 교회 마커 하나씩 찍기
        for index, row in df.iterrows():
            # 마커를 눌렀을 때 나올 정보 (이름, 지도자, 전화번호)
            info_text = f"""
            <div style='width:200px'>
                <b>{row['Name']}</b><br>
                성함: {row['Leader']}<br>
                연락처: {row['Phone']}<br>
                주소: {row['Address']}
            </div>
            """
            
            # 분류(Category)에 따른 색상 구분
            cat = str(row['Category'])
            if "건축" in cat:
                map_color = "blue"    # 건축교회는 파란색
            elif "일반" in cat:
                map_color = "red"     # 일반교회는 빨간색
            else:
                map_color = "orange"  # 그 외는 주황색
            
            # 지도에 십자가 마커 추가
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(info_text, max_width=300),
                tooltip=row['Name'],
                icon=folium.Icon(color=map_color, icon='plus', prefix='glyphicon')
            ).add_to(m)

        # 3. 화면에 지도 출력
        st_folium(m, width="100%", height=600)
        
        # 4. 하단에 상세 목록 표 출력
        st.subheader("📋 전체 사역 데이터 목록")
        st.dataframe(df)

    except Exception as e:
        st.warning("시트의 제목(헤더)을 확인해 주세요.")
        st.info("첫 줄 제목이 Name, Latitude, Longitude, Category, Leader, Phone, Address 인지 확인 부탁드립니다.")
else:
    st.info("구글 시트 게시를 기다리는 중이거나 URL이 올바르지 않습니다.")