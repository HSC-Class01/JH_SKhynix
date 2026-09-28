# SK hynix DART Financial Analysis

[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97-%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C%20%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-0b5fff?style=for-the-badge)](https://YOUR-STREAMLIT-APP.streamlit.app/)

SK하이닉스(000660, OpenDART corp_code `00164779`)의 사업보고서·반기보고서·분기보고서 재무데이터를 OpenDART API로 수집하고, 주요 재무수치와 재무비율을 계산하여 Streamlit 대시보드로 제공합니다.

## Dashboard

배포 후 위 배지와 GitHub 저장소 About의 Website에 Streamlit 앱 주소를 입력하세요.

## 자동 업데이트

- GitHub Actions: 매월 자동 실행 + 수동 `workflow_dispatch`
- Secret: `OPENDART_API_KEY`
- 수집: OpenDART `fnlttSinglAcntAll`
- 기준: 연결재무제표(CFS)
- 보고서: 사업보고서(11011), 반기보고서(11012), 1분기(11013), 3분기(11014)
- 데이터 분석: 매출액, 매출총이익, 영업이익, 세전이익, 당기순이익, 총자산, 현금, 매출채권, 재고, 유형자산, 총부채, 차입금, 자본, CFO/CFI/CFF, CAPEX 및 수익성·유동성·레버리지 지표

## 2010년 데이터 주의

OpenDART의 구조화 정기보고서 재무정보 API는 2015년 이후 자료를 제공합니다. 따라서 이 프로젝트는 2010년부터 수집 범위를 요청하되, **2010~2014년에는 존재하지 않는 API 데이터를 임의로 생성하지 않습니다.** 2015년부터 구조화 재무데이터를 자동 수집합니다.

## 국내 Peer Firms

| 기업 | 종목코드 | 비교 목적 |
|---|---:|---|
| 삼성전자 | 005930 | 메모리·종합반도체 재무 비교 |
| 한미반도체 | 042700 | HBM/패키징 장비 사이클 비교 |
| 하나마이크론 | 067310 | 메모리 후공정·패키징 비교 |
| SFA반도체 | 036540 | 반도체 후공정 비교 |
| DB하이텍 | 000990 | 국내 반도체 제조업 재무구조 비교 |

Peer는 국내 반도체 산업 내 사업영역이 인접한 기업을 비교군으로 제시한 것이며, 순위나 투자판단을 의미하지 않습니다.

## 설치

```bash
pip install -r requirements.txt
```

### API 키 입력

로컬 실행:

```bash
# Windows PowerShell
$env:OPENDART_API_KEY="발급받은_40자리_키"
python src/collect.py
python src/analyze.py
streamlit run app.py
```

GitHub에서는 **Settings → Secrets and variables → Actions → New repository secret**에서
`OPENDART_API_KEY` 이름으로 등록합니다. API 키는 코드나 README에 직접 입력하지 않습니다.

## Streamlit Community Cloud

1. GitHub 저장소를 연결
2. Main file path: `app.py`
3. Python dependencies: `requirements.txt`
4. Deploy
5. 생성된 `https://....streamlit.app` 주소를 README 배지와 GitHub About의 Website에 입력
