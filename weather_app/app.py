import streamlit as st
import plotly.graph_objects as go
from weather_api import WeatherAPI
import datetime

# 페이지 설정
st.set_page_config(
    page_title="🌤️ 실시간 날씨 정보",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/weather-app',
        'Report a bug': 'https://github.com/your-username/weather-app/issues',
        'About': """
        # 🌤️ 실시간 날씨 정보 앱
        
        OpenWeather API를 사용하여 전 세계 도시의 실시간 날씨 정보를 제공합니다.
        
        **개발자**: Your Name
        **소스코드**: [GitHub](https://github.com/your-username/weather-app)
        """
    }
)

# CSS 스타일 추가
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .temperature {
        font-size: 4rem;
        font-weight: bold;
        color: #FFD700;
    }
    .description {
        font-size: 1.2rem;
        color: #E8E8E8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 헤더
    st.markdown('<h1 class="main-header">🌤️ 실시간 날씨 정보</h1>', unsafe_allow_html=True)
    
    # WeatherAPI 인스턴스 생성 (실제 API 사용)
    weather_api = WeatherAPI(test_mode=False)
    
    # API 상태 표시
    if weather_api.test_mode:
        st.warning("⚠️ 현재 데모 모드로 실행 중입니다. 실제 날씨 데이터가 아닌 샘플 데이터를 표시합니다.")
    else:
        st.success("✅ 실시간 날씨 데이터를 제공하고 있습니다.")
    
    # 사이드바
    with st.sidebar:
        st.header("🔍 도시 검색")
        
        # 도시 입력
        city_name = st.text_input(
            "도시 이름을 입력하세요",
            placeholder="예: Seoul, Tokyo, New York",
            help="영어나 한글로 도시 이름을 입력하세요"
        )
        
        # 검색 버튼
        search_button = st.button("🔍 날씨 조회", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # 인기 도시 목록
        st.subheader("🏙️ 인기 도시")
        popular_cities = ["Seoul", "Tokyo", "New York", "London", "Paris", "Sydney"]
        
        for city in popular_cities:
            if st.button(city, use_container_width=True, key=f"btn_{city}"):
                city_name = city
                search_button = True
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")
    
    # 메인 컨텐츠
    if search_button and city_name:
        with st.spinner('날씨 정보를 가져오는 중...'):
            try:
                result = weather_api.get_weather_data(city_name)
                
                # 디버깅 정보 (개발 시에만 표시)
                debug_mode = st.checkbox("🔧 디버깅 정보 표시", value=False, key="debug_checkbox")
                if debug_mode:
                    st.session_state['show_debug'] = True
                    st.write("**API 응답:**", result)
                    st.write("**테스트 모드:**", weather_api.test_mode)
                    st.write("**API 키 상태:**", "설정됨" if weather_api.api_key else "설정되지 않음")
                else:
                    st.session_state['show_debug'] = False
                
            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                result = {'success': False, 'error': f'시스템 오류: {str(e)}'}
        
        if result['success']:
            data = result['data']
            
            # 날씨 정보 메인 카드
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="weather-card">
                    <h2>📍 {data['city']}, {data['country']}</h2>
                    <div class="temperature">{data['temperature']}°C</div>
                    <div class="description">🌡️ 체감온도: {data['feels_like']}°C</div>
                    <div class="description">☁️ {data['description']}</div>
                    <div class="description">🕐 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # 날씨 아이콘
                icon_url = weather_api.get_weather_icon_url(data['icon'])
                st.image(icon_url, width=150)
            
            # 상세 정보 카드들
            st.subheader("📊 상세 날씨 정보")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="💧 습도",
                    value=f"{data['humidity']}%",
                    help="공기 중 수분의 양"
                )
            
            with col2:
                st.metric(
                    label="🌪️ 풍속",
                    value=f"{data['wind_speed']} m/s",
                    help="바람의 속도"
                )
            
            with col3:
                st.metric(
                    label="🗜️ 기압",
                    value=f"{data['pressure']} hPa",
                    help="대기압"
                )
            
            with col4:
                st.metric(
                    label="👁️ 가시거리",
                    value=f"{data['visibility']} km",
                    help="시야 거리"
                )
            
            # 온도 게이지 차트
            st.subheader("🌡️ 온도 게이지")
            
            import plotly.graph_objects as plotly_go
            
            fig = plotly_go.Figure(plotly_go.Indicator(
                mode = "gauge+number+delta",
                value = data['temperature'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "온도 (°C)"},
                delta = {'reference': 20},
                gauge = {
                    'axis': {'range': [None, 50]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 10], 'color': "lightgray"},
                        {'range': [10, 25], 'color': "gray"},
                        {'range': [25, 50], 'color': "orange"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 35
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # 추가 정보
            st.subheader("ℹ️ 추가 정보")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**날씨 상태**: {data['main_weather']}")
                st.info(f"**구름량**: {data['cloudiness']}%")
            
            with col2:
                st.info(f"**풍향**: {data['wind_direction']}°")
                
                # 날씨 조언
                temp = data['temperature']
                if temp < 0:
                    advice = "❄️ 매우 추워요! 두꺼운 외투를 입으세요."
                elif temp < 10:
                    advice = "🧥 추워요! 따뜻한 옷을 입으세요."
                elif temp < 20:
                    advice = "🍂 선선해요! 가벼운 겉옷을 준비하세요."
                elif temp < 30:
                    advice = "☀️ 좋은 날씨예요! 외출하기 좋아요."
                else:
                    advice = "🔥 매우 더워요! 시원한 곳에 있으세요."
                
                st.success(advice)
            
            # 주간 날씨 예보 섹션
            st.subheader("📅 5일 날씨 예보")
            
            with st.spinner('주간 예보를 가져오는 중...'):
                try:
                    forecast_result = weather_api.get_weekly_forecast(city_name)
                    
                    # 디버깅 정보
                    if st.session_state.get('show_debug', False):
                        st.write("**예보 API 응답:**", forecast_result)
                        
                except Exception as e:
                    st.error(f"❌ 주간 예보 오류: {str(e)}")
                    forecast_result = {'success': False, 'error': f'예보 시스템 오류: {str(e)}'}
            
            if forecast_result['success']:
                forecast_data = forecast_result['data']
                
                # 5개 컬럼으로 나누어 각 날짜별 예보 표시
                cols = st.columns(5)
                
                for i, day_data in enumerate(forecast_data):
                    with cols[i]:
                        # 날짜 포맷팅
                        date_obj = datetime.datetime.strptime(day_data['date'], '%Y-%m-%d')
                        day_name = ['월', '화', '수', '목', '금', '토', '일'][date_obj.weekday()]
                        date_str = f"{date_obj.month}/{date_obj.day}"
                        
                        # 날씨 아이콘
                        icon_url = weather_api.get_weather_icon_url(day_data['icon'])
                        
                        # 카드 스타일로 표시
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem;
                            border-radius: 10px;
                            text-align: center;
                            color: white;
                            margin-bottom: 1rem;
                        ">
                            <div style="font-weight: bold; font-size: 0.9rem;">{day_name}</div>
                            <div style="font-size: 0.8rem; opacity: 0.8;">{date_str}</div>
                            <img src="{icon_url}" width="50" style="margin: 0.5rem 0;">
                            <div style="font-size: 1.2rem; font-weight: bold;">{day_data['max_temp']}°</div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">{day_data['min_temp']}°</div>
                            <div style="font-size: 0.8rem; margin-top: 0.5rem;">{day_data['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # 온도 변화 차트
                st.subheader("📈 주간 온도 변화")
                
                dates = []
                max_temps = []
                min_temps = []
                
                for day_data in forecast_data:
                    date_obj = datetime.datetime.strptime(day_data['date'], '%Y-%m-%d')
                    day_name = ['월', '화', '수', '목', '금', '토', '일'][date_obj.weekday()]
                    dates.append(f"{date_obj.month}/{date_obj.day} ({day_name})")
                    max_temps.append(day_data['max_temp'])
                    min_temps.append(day_data['min_temp'])
                
                import plotly.graph_objects as plotly_go
                fig = plotly_go.Figure()
                
                # 최고 온도 라인
                fig.add_trace(plotly_go.Scatter(
                    x=dates,
                    y=max_temps,
                    mode='lines+markers',
                    name='최고 온도',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=8)
                ))
                
                # 최저 온도 라인
                fig.add_trace(plotly_go.Scatter(
                    x=dates,
                    y=min_temps,
                    mode='lines+markers',
                    name='최저 온도',
                    line=dict(color='#4ECDC4', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="5일간 온도 변화",
                    xaxis_title="날짜",
                    yaxis_title="온도 (°C)",
                    hovermode='x unified',
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.error(f"❌ 주간 예보를 가져올 수 없습니다: {forecast_result['error']}")
        
        else:
            st.error(f"❌ {result['error']}")
            st.info("💡 팁: 영어나 한글로 정확한 도시 이름을 입력해보세요.")
    
    elif not city_name and not search_button:
        # 초기 화면
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h2>🌍 전 세계 날씨 정보를 확인하세요!</h2>
            <p style="font-size: 1.2rem; color: #666;">
                좌측 사이드바에서 도시 이름을 입력하거나<br>
                인기 도시 중 하나를 선택해보세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 예시 이미지나 추가 정보
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🌡️ 실시간 데이터
            OpenWeather API를 통해  
            정확한 실시간 날씨 정보를  
            제공합니다.
            """)
        
        with col2:
            st.markdown("""
            ### 🌍 전 세계 지원
            전 세계 주요 도시의  
            날씨 정보를 한눈에  
            확인할 수 있습니다.
            """)
        
        with col3:
            st.markdown("""
            ### 📊 상세 정보
            온도, 습도, 풍속 등  
            다양한 날씨 정보를  
            시각적으로 표시합니다.
            """)

if __name__ == "__main__":
    main()