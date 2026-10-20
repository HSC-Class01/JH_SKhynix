# SK hynix OpenDART Financial Dashboard

[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗-대시보드_바로가기-2456D8?style=for-the-badge)](https://hsc-class01.github.io/JH_SKhynix/)

SK하이닉스(000660)의 OpenDART 사업·반기·분기보고서를 수집하고 재무 수치와 비율을 분석해 GitHub Pages에 게시합니다.

**[🔗 대시보드 바로가기](https://hsc-class01.github.io/JH_SKhynix/)** · [저장소](https://github.com/HSC-Class01/JH_SKhynix)

## 기능

- 매출·영업이익·순이익, 수익성·안정성 지표를 상단 그래프와 핵심 카드로 표시
- Annual, Half-year, Quarterly 세 분류로 각각 상세 수치 테이블 제공
- CFS(연결) 우선 수집, 미제공 시 OFS(별도) 사용
- OpenDART 원자료, 계산 지표, 보고서 수집 현황을 CSV로 보관
- 매월 1일 00:15 UTC (한국시간 09:15)에 수집·분석·Pages 자동 배포
- 수동 실행: 저장소 `Actions → SK hynix DART dashboard → Run workflow`

## API 키 설정 및 첫 배포

1. [OpenDART](https://opendart.fss.or.kr/)에서 인증키를 발급합니다.
2. GitHub 저장소의 `Settings → Secrets and variables → Actions → New repository secret`으로 이동합니다.
3. Secret 이름에 `OPENDART_API_KEY`, 값에 인증키를 입력합니다. API 키를 코드나 README에 직접 넣지 마세요.
4. `Settings → Pages → Build and deployment`에서 Source를 **GitHub Actions**로 설정합니다.
5. `Actions`에서 **SK hynix DART dashboard**를 실행합니다. 이후 매월 자동 갱신됩니다.

기존 `DART_API_KEY` Secret도 지원합니다. API 키는 GitHub Actions 환경변수로 전달됩니다.

## 주요 데이터와 계산 기준

원자료 금액은 원 단위이며 대시보드는 억원 단위로 표시합니다. 매출액, 영업이익, 순이익, 자산, 부채, 자본, 유동자산·부채, 현금, 차입금, 영업현금흐름, 설비투자, FCF, 순차입금과 영업이익률, 순이익률, 부채비율, 유동비율, 자기자본비율, ROA, ROE를 제공합니다. Q3 손익·현금흐름은 반기 누적값을 차감한 단독 분기 값이며, 자산·부채·자본은 기간 말 잔액입니다. ROA·ROE는 기간 말 잔액 기준입니다.

OpenDART에서 제공하지 않거나 계정명이 매칭되지 않는 기간·수치는 비어 있을 수 있으며 수집 상태를 `data/reports.csv`에서 확인할 수 있습니다. 분석은 공시 자료를 재분류한 참고 정보이며 투자 조언이 아닙니다.

## 국내 Peer firms

| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| 삼성전자 | 005930 | 메모리·종합 반도체 직접 비교 |
| 한미반도체 | 042700 | HBM·패키징 장비 투자 사이클 |
| 하나마이크론 | 067310 | 메모리 후공정·패키징 |
| SFA반도체 | 036540 | 후공정 패키징·테스트 |
| DB하이텍 | 000990 | 국내 반도체 제조·파운드리 |

대시보드의 Peer firms 표와 `data/peers.csv`에서 비교 대상과 설명을 확인할 수 있습니다.

## 로컬 실행

```powershell
python -m pip install -r requirements.txt
$env:OPENDART_API_KEY = "발급받은_OpenDART_인증키"
python -m src.collect
python -m src.analyze
python -m src.dashboard
python -m http.server 8000 --directory docs
```

## Agent 개발용 ZIP

[개발용 ZIP](https://github.com/HSC-Class01/JH_SKhynix/raw/main/JH_SKhynix_DART_Agent.zip)은 숨김 파일 없이 배포합니다. ZIP 내부의 `github_workflows/update_dart.yml`은 GitHub 저장소의 `.github/workflows/update_dart.yml` 경로에 복사해야 Actions가 인식합니다. API 키와 GitHub Pages 초기 설정은 `docs/SETUP.md`를 참고하세요.
