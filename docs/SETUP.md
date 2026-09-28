# 배포 및 GitHub 설정

## 1. API Secret

GitHub 저장소에서:

`Settings → Secrets and variables → Actions → New repository secret`

Name: `OPENDART_API_KEY`

Value: OpenDART에서 발급한 40자리 인증키

## 2. 첫 수집

Actions → Update SK hynix DART data → Run workflow → Run workflow

## 3. 월간 실행

현재 workflow는 GitHub Actions의 UTC cron을 사용합니다. 월초 자동 실행은 서버의 UTC 기준으로 동작하므로, 실제 한국시간 1일 새벽 실행이 반드시 필요하면 GitHub Actions cron의 UTC/KST 차이를 고려해 스케줄을 조정하세요. 수동 실행은 언제든 가능합니다.

## 4. Streamlit

Streamlit Community Cloud에서 repository와 `app.py`를 연결합니다.

## 5. GitHub About

Repository → About의 Website에 Streamlit URL을 넣습니다.

## 6. README 배지

`YOUR-STREAMLIT-APP.streamlit.app`를 실제 Streamlit 주소로 바꾸세요. 사용자가 제공한 별도 배지 이미지가 저장소/대화 첨부로 확인되지 않아, ZIP에는 외부 이미지 파일을 포함하지 않고 접근성 있는 shields.io 배지를 사용했습니다.
