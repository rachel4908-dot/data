import requests
import os
from dotenv import load_dotenv
import streamlit as st

# 환경 변수 로드
load_dotenv()

class WeatherAPI:
    def __init__(self, test_mode=False):
        # Streamlit Cloud 환경에서는 st.secrets 사용, 로컬에서는 .env 파일 사용
        try:
            self.api_key = st.secrets["OPENWEATHER_API_KEY"]
        except:
            self.api_key = os.getenv('OPENWEATHER_API_KEY')
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.test_mode = test_mode
    
    def get_weather_data(self, city_name):
        """
        도시 이름으로 날씨 데이터를 가져오는 함수
        
        Args:
            city_name (str): 도시 이름
            
        Returns:
            dict: 날씨 데이터 또는 에러 메시지
        """
        
        # 테스트 모드일 경우 더미 데이터 반환
        if self.test_mode:
            return self._get_test_data(city_name)
        
        try:
            # API 요청 URL 구성
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric',  # 섭씨 온도
                'lang': 'kr'        # 한국어
            }
            
            # API 요청
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # 필요한 데이터만 추출
                weather_data = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'description': data['weather'][0]['description'],
                    'main_weather': data['weather'][0]['main'],
                    'icon': data['weather'][0]['icon'],
                    'visibility': data.get('visibility', 0) / 1000,  # km 단위로 변환
                    'cloudiness': data['clouds']['all']
                }
                
                return {'success': True, 'data': weather_data}
            
            elif response.status_code == 404:
                return {'success': False, 'error': '도시를 찾을 수 없습니다.'}
            elif response.status_code == 401:
                return {'success': False, 'error': 'API 키가 유효하지 않습니다. 테스트 모드로 전환하세요.'}
            else:
                return {'success': False, 'error': f'API 요청 실패: {response.status_code}'}
                
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'네트워크 오류: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'알 수 없는 오류: {str(e)}'}
    
    def _get_test_data(self, city_name):
        """테스트용 더미 데이터를 생성하는 함수"""
        import random
        
        # 도시별 더미 데이터
        city_data = {
            'Seoul': {'base_temp': 15, 'country': 'KR', 'korean_name': '서울'},
            'Tokyo': {'base_temp': 18, 'country': 'JP', 'korean_name': '도쿄'},
            'New York': {'base_temp': 12, 'country': 'US', 'korean_name': '뉴욕'},
            'London': {'base_temp': 8, 'country': 'GB', 'korean_name': '런던'},
            'Paris': {'base_temp': 10, 'country': 'FR', 'korean_name': '파리'},
            'Sydney': {'base_temp': 22, 'country': 'AU', 'korean_name': '시드니'}
        }
        
        # 기본값 설정
        if city_name in city_data:
            city_info = city_data[city_name]
        else:
            city_info = {'base_temp': 20, 'country': 'XX', 'korean_name': city_name}
        
        # 랜덤한 날씨 데이터 생성
        base_temp = city_info['base_temp']
        temperature = round(base_temp + random.uniform(-5, 5), 1)
        feels_like = round(temperature + random.uniform(-2, 2), 1)
        
        weather_conditions = [
            {'main': 'Clear', 'description': '맑음', 'icon': '01d'},
            {'main': 'Clouds', 'description': '구름 많음', 'icon': '03d'},
            {'main': 'Rain', 'description': '비', 'icon': '10d'},
            {'main': 'Snow', 'description': '눈', 'icon': '13d'},
        ]
        
        weather = random.choice(weather_conditions)
        
        weather_data = {
            'city': city_info['korean_name'],
            'country': city_info['country'],
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': random.randint(40, 90),
            'pressure': random.randint(1000, 1025),
            'wind_speed': round(random.uniform(0, 10), 1),
            'wind_direction': random.randint(0, 360),
            'description': weather['description'],
            'main_weather': weather['main'],
            'icon': weather['icon'],
            'visibility': round(random.uniform(5, 20), 1),
            'cloudiness': random.randint(0, 100)
        }
        
        return {'success': True, 'data': weather_data}
    
    def get_weather_icon_url(self, icon_code):
        """
        날씨 아이콘 URL을 반환하는 함수
        
        Args:
            icon_code (str): 아이콘 코드
            
        Returns:
            str: 아이콘 URL
        """
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"