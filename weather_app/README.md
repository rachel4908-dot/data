# 🌤️ 실시간 날씨 웹 애플리케이션

Streamlit과 OpenWeather API를 사용한 실시간 날씨 정보 웹 애플리케이션입니다.

## 🚀 라이브 데모
[여기에 배포된 앱 URL이 표시됩니다]

## ✨ 주요 기능
- 🌍 전 세계 도시별 실시간 날씨 조회
- 🌡️ 온도, 체감온도, 습도, 풍속 등 상세 정보 표시
- 📊 시각적 온도 게이지 차트
- ⚡ 인기 도시 빠른 검색
- 📱 반응형 웹 인터페이스

## 🛠️ 사용 기술
- **Frontend**: Streamlit
- **API**: OpenWeather API
- **Data Visualization**: Plotly
- **Styling**: Custom CSS

## 📦 로컬 설치 및 실행

### 1. 저장소 클론
```bash
git clone [저장소 URL]
cd weather_app
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 OpenWeather API 키를 추가하세요:
```env
OPENWEATHER_API_KEY=your_api_key_here
```

### 4. 애플리케이션 실행
```bash
streamlit run app.py
```

## ☁️ Streamlit Cloud 배포 가이드

### 1. GitHub 저장소 준비
- 모든 파일을 GitHub 저장소에 업로드
- `.env` 파일은 업로드하지 마세요 (보안상 중요)

### 2. Streamlit Cloud 설정
1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소와 브랜치 선택
5. 메인 파일 경로: `app.py`

### 3. 환경 변수 설정
Streamlit Cloud의 "Advanced settings" → "Secrets"에서:
```toml
OPENWEATHER_API_KEY = "your_actual_api_key_here"
```

### 4. 배포 완료
배포가 완료되면 자동으로 URL이 생성됩니다.

## 🔧 API 키 발급 방법

1. [OpenWeather](https://openweathermap.org/) 회원가입
2. API Keys 메뉴에서 새 키 생성
3. 무료 플랜으로도 충분히 사용 가능

## 📁 프로젝트 구조
```
weather_app/
├── app.py                 # 메인 Streamlit 애플리케이션
├── weather_api.py         # OpenWeather API 연결 모듈
├── requirements.txt       # Python 패키지 의존성
├── .env                   # 환경 변수 (로컬용, Git에 포함 안 됨)
├── .streamlit/
│   ├── config.toml       # Streamlit 설정
│   └── secrets.toml      # 시크릿 템플릿
└── README.md             # 프로젝트 문서
```

## 🎯 주요 파일 설명

- **app.py**: 메인 Streamlit UI 및 로직
- **weather_api.py**: OpenWeather API 호출 및 데이터 처리
- **requirements.txt**: 배포에 필요한 Python 패키지 목록
- **.streamlit/config.toml**: UI 테마 및 서버 설정

## 🔒 보안 참고사항

- API 키는 절대 코드에 직접 입력하지 마세요
- `.env` 파일은 `.gitignore`에 추가하세요
- Streamlit Cloud에서는 Secrets 기능을 사용하세요

## 📞 문의 및 지원

문제가 발생하거나 개선 사항이 있으시면 GitHub Issues를 통해 알려주세요.

---
Made with ❤️ using Streamlit & OpenWeather API