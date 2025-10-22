# Streamlit Cloud 배포 체크리스트

## ✅ 필수 파일 확인
- [x] app.py (메인 애플리케이션)
- [x] requirements.txt (의존성)
- [x] .streamlit/config.toml (설정)
- [x] README.md (문서)
- [x] .gitignore (보안)

## ✅ 배포 전 확인사항
- [ ] OpenWeather API 키 발급 완료
- [ ] GitHub 저장소 생성 및 코드 업로드
- [ ] .env 파일이 .gitignore에 포함되어 있는지 확인
- [ ] 로컬에서 정상 동작 확인

## ✅ Streamlit Cloud 설정
1. https://streamlit.io/cloud 접속
2. GitHub 연동
3. 저장소 선택
4. Main file path: app.py
5. Secrets에 API 키 추가:
   ```
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```

## 🎯 배포 후 확인사항
- [ ] 앱이 정상적으로 로드되는지 확인
- [ ] 도시 검색 기능 동작 확인
- [ ] 실시간 날씨 데이터 표시 확인
- [ ] 모바일 반응형 확인