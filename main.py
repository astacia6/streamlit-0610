import streamlit as st
import folium
from streamlit_folium import st_folium

# 명소 데이터 정의
tourist_spots = {
    "도쿄타워": {
        "description": """
        도쿄의 대표적인 랜드마크인 도쿄타워는 1958년에 세워진 통신탑으로, 에펠탑을 모티프로 했습니다.
        타워 꼭대기에서는 도쿄 시내를 한눈에 볼 수 있으며, 저녁에는 아름답게 조명이 들어옵니다.
        주변에는 조조지(절)와 음식점도 많아 하루 코스로도 좋습니다.
        """,
        "location": (35.6586, 139.7454)
    },
    "아사쿠사 & 센소지": {
        "description": """
        아사쿠사는 도쿄의 전통적인 분위기를 간직한 지역으로, 센소지는 도쿄에서 가장 오래된 절입니다.
        가미나리몬(雷門)이라는 붉은 문이 유명하며, 나카미세 거리에서는 다양한 일본 간식과 기념품을 즐길 수 있습니다.
        """,
        "location": (35.7148, 139.7967)
    },
    "시부야 스크램블 교차로": {
        "description": """
        세계에서 가장 혼잡한 교차로 중 하나인 시부야 스크램블은 도쿄의 현대적인 모습을 상징합니다.
        수백 명이 동시에 횡단보도를 건너는 장면은 드라마와 영화에서도 자주 등장합니다.
        근처에는 하치공 동상과 쇼핑센터도 있습니다.
        """,
        "location": (35.6595, 139.7005)
    },
    "우에노 공원": {
        "description": """
        도쿄 북쪽에 위치한 우에노 공원은 박물관, 동물원, 연못이 있는 넓은 녹지 공간입니다.
        특히 봄에는 벚꽃 명소로 유명하여 많은 사람들이 방문합니다.
        국립서양미술관, 도쿄국립박물관 등 문화 시설도 함께 즐길 수 있습니다.
        """,
        "location": (35.7156, 139.7730)
    },
    "도쿄 스카이트리": {
        "description": """
        634m 높이의 도쿄 스카이트리는 일본에서 가장 높은 건축물로, 전망대에서 탁 트인 도쿄 시내 전경을 볼 수 있습니다.
        저녁에는 멋진 조명 쇼도 감상할 수 있으며, 도쿄 소라마치 쇼핑몰과 레스토랑도 연결되어 있습니다.
        """,
        "location": (35.7100, 139.8107)
    },
}

# 타이틀
st.title("🗼 도쿄 주요 관광지 가이드")

# 관광지 선택
selected_spot = st.selectbox("방문하고 싶은 명소를 선택하세요", list(tourist_spots.keys()))

# 선택된 관광지 정보
spot_info = tourist_spots[selected_spot]
st.subheader(f"📍 {selected_spot}")
st.markdown(spot_info["description"])

# 지도 표시
m = folium.Map(location=spot_info["location"], zoom_start=16)
folium.Marker(spot_info["location"], tooltip=selected_spot, popup=selected_spot).add_to(m)

# 스트림릿에 지도 표시
st_folium(m, width=700, height=500)
