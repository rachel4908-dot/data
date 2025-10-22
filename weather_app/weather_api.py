import requests
import os
from dotenv import load_dotenv
import streamlit as st

# 환경 변수 로드
load_dotenv()

class WeatherAPI:
    def __init__(self, test_mode=False):
        # API 키 우선순위: st.secrets > 환경변수 > 하드코딩된 키
        self.api_key = None
        
        # 1. Streamlit secrets 시도
        try:
            if hasattr(st, 'secrets') and 'OPENWEATHER_API_KEY' in st.secrets:
                self.api_key = st.secrets["OPENWEATHER_API_KEY"]
        except Exception:
            pass
        
        # 2. 환경변수 시도
        if not self.api_key:
            self.api_key = os.getenv('OPENWEATHER_API_KEY')
        
        # 3. 기본 API 키 (임시)
        if not self.api_key:
            self.api_key = 'f36170a91601f2703f8aa9a36d27b343'
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.test_mode = test_mode
        
        # API 키 유효성 검사
        if not self.test_mode and not self._validate_api_key():
            print(f"API 키 검증 실패, 테스트 모드로 전환합니다. 키: {self.api_key[:10]}...")
            self.test_mode = True
    
    def _validate_api_key(self):
        """API 키가 유효한지 확인하는 함수"""
        try:
            test_url = f"{self.base_url}?q=Seoul&appid={self.api_key}"
            response = requests.get(test_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
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
    
    def get_weekly_forecast(self, city_name):
        """
        도시 이름으로 5일 날씨 예보를 가져오는 함수
        
        Args:
            city_name (str): 도시 이름
            
        Returns:
            dict: 5일 예보 데이터 또는 에러 메시지
        """
        
        # 테스트 모드일 경우 더미 데이터 반환
        if self.test_mode:
            return self._get_test_forecast_data(city_name)
        
        try:
            # API 요청 URL 구성
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric',  # 섭씨 온도
                'lang': 'kr'        # 한국어
            }
            
            # API 요청
            response = requests.get(self.forecast_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # 5일 예보 데이터 처리 (3시간 간격 데이터를 일별로 그룹화)
                forecast_data = []
                current_date = None
                daily_temps = []
                daily_data = {}
                
                for item in data['list']:
                    date_str = item['dt_txt'].split(' ')[0]  # YYYY-MM-DD 형식
                    
                    if current_date != date_str:
                        # 새로운 날짜인 경우, 이전 날짜 데이터 저장
                        if current_date and daily_temps:
                            daily_data['min_temp'] = round(min(daily_temps), 1)
                            daily_data['max_temp'] = round(max(daily_temps), 1)
                            forecast_data.append(daily_data)
                        
                        # 새로운 날짜 데이터 초기화
                        current_date = date_str
                        daily_temps = []
                        daily_data = {
                            'date': date_str,
                            'temperature': round(item['main']['temp'], 1),
                            'description': item['weather'][0]['description'],
                            'main_weather': item['weather'][0]['main'],
                            'icon': item['weather'][0]['icon'],
                            'humidity': item['main']['humidity'],
                            'wind_speed': item['wind']['speed']
                        }
                    
                    daily_temps.append(item['main']['temp'])
                
                # 마지막 날짜 데이터 저장
                if daily_temps:
                    daily_data['min_temp'] = round(min(daily_temps), 1)
                    daily_data['max_temp'] = round(max(daily_temps), 1)
                    forecast_data.append(daily_data)
                
                # 최대 5일만 반환
                forecast_data = forecast_data[:5]
                
                return {'success': True, 'data': forecast_data}
            
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
    
    def _get_test_forecast_data(self, city_name):
        """테스트용 5일 예보 더미 데이터를 생성하는 함수"""
        import random
        from datetime import datetime, timedelta
        
        # 도시별 기본 온도 설정
        city_temps = {
            'Seoul': 15, 'Tokyo': 18, 'New York': 12, 
            'London': 8, 'Paris': 10, 'Sydney': 22
        }
        base_temp = city_temps.get(city_name, 20)
        
        forecast_data = []
        weather_conditions = [
            {'main': 'Clear', 'description': '맑음', 'icon': '01d'},
            {'main': 'Clouds', 'description': '구름 많음', 'icon': '03d'},
            {'main': 'Rain', 'description': '비', 'icon': '10d'},
            {'main': 'Snow', 'description': '눈', 'icon': '13d'},
        ]
        
        for i in range(5):
            date = datetime.now() + timedelta(days=i)
            weather = random.choice(weather_conditions)
            temp_variation = random.uniform(-5, 5)
            base_daily_temp = base_temp + temp_variation
            
            daily_data = {
                'date': date.strftime('%Y-%m-%d'),
                'temperature': round(base_daily_temp, 1),
                'min_temp': round(base_daily_temp - random.uniform(2, 5), 1),
                'max_temp': round(base_daily_temp + random.uniform(2, 5), 1),
                'description': weather['description'],
                'main_weather': weather['main'],
                'icon': weather['icon'],
                'humidity': random.randint(40, 90),
                'wind_speed': round(random.uniform(0, 10), 1)
            }
            forecast_data.append(daily_data)
        
        return {'success': True, 'data': forecast_data}
    
    def get_weather_icon_url(self, icon_code):
        """
        날씨 아이콘 URL을 반환하는 함수
        
        Args:
            icon_code (str): 아이콘 코드
            
        Returns:
            str: 아이콘 URL
        """
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"