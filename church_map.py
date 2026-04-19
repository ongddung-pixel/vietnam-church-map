import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 웹사이트의 제목과 레이아웃 설정
st.set_page_config(page_title="베트남 사역 지도", layout="wide")

st.title("🇻🇳 베트남 교회 사역 지도 공유 시스템")
st.write("아이폰/아이패드 앱에서 내보낸 CSV 파일을 아래에 올려주세요.")

# 2. 파일 업로드 칸 만들기
uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type=["csv"])

# 파일을 올렸을 때만 아래 내용이 실행됩니다.
if uploaded_file is not None:
    # 엑셀(CSV) 파일 읽기
    df = pd.read_csv(uploaded_file)
    
    # 3. 지도 그리기 (데이터에 있는 위도/경도의 중간 지점을 중심으로)
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)

    # 4. 교회 하나씩 지도에 찍기 (반복문)
    for index, row in df.iterrows():
        # --- [1] 정보창에 표시될 텍스트 정의 (이게 꼭 있어야 합니다!) ---
        info_text = f"<b>{row['Name']}</b><br>지도자: {row['Leader']}<br>연락처: {row['Phone']}"
        
        # --- [2] 분류(Category)에 따라 마커 색상 정하기 ---
        category_str = str(row['Category']) 
        
        if "건축" in category_str:
            map_color = "blue"    # 건축교회는 파란색
        elif "일반" in category_str:
            map_color = "red"     # 일반교회는 빨간색
        else:
            map_color = "orange"  # 그 외는 오렌지색
        
        # --- [3] 지도에 마커 찍기 ---
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(info_text, max_width=300), # 위에서 만든 info_text를 여기서 사용합니다
            tooltip=row['Name'],
            icon=folium.Icon(color=map_color, icon='plus', prefix='glyphicon')
        ).add_to(m)

    # 5. 화면에 지도 보여주기
    st_folium(m, width="100%", height=600)
    
    # 6. 아래에 표로도 보여주기
    st.subheader("📋 전체 목록")
    st.dataframe(df)

else:
    # 파일을 아직 안 올렸을 때 보여줄 기본 안내
    st.info("CSV 파일을 올려주시면 지도가 나타납니다.")
    # 기본 베트남 지도 보여주기
    m = folium.Map(location=[14.0583, 108.2772], zoom_start=5)
    st_folium(m, width="100%", height=600)