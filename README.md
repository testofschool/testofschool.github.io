# testofschool.github.io

강정민 채용 포트폴리오. 삼일PwC 검토자가 연구와 작업을 확인하고 면접 연락으로 이어갈 수 있도록 구성한 정적 사이트다. 외부 런타임, 프레임워크, 트래커가 없다.

## 구성

- `kr/index.html`: 한국어 정본
- `index.html`: 같은 구조의 영어판
- `assets/proof/`: 실제 삼일 본선 명찰, 원본 논문, 공식 채택 기록, 실제 연구 데이터의 시각화, MV 장면
- `assets/icons/`: Lucide/Feather 탐색 아이콘과 GitHub 식별 아이콘. 라이선스 동봉.
- `assets/fonts/`: 자체 호스팅 Pretendard 가변 폰트와 JetBrains Mono 서브셋
- `assets/og.png`: 1200×630 공유 이미지

## 읽는 순서

2026-11-04 사용자 승인 방향: “좋다, 이 방향성으로 정리해줘”. 기준은 `portfolio-contract.json`과 `AGENTS.md`에 보존한다. 내용·순서 수정 후 `python3 scripts/check_portfolio.py`로 구조 회귀를 확인하고, 배치 변경은 실제 화면도 확인한다.

이름과 아이콘 연락처 → **삼일PwC 트랙 본선 진출 + 실제 명찰을 크게 보여주는 첫 화면** → NeurIPS 2026 워크숍 포스터 채택 연구 → 작은 MV 썸네일 → 접힌 이력 → 면접 연락.

삼일 본선 경험은 검토자와 공감대를 만드는 메인이다. 본선 진출 사실에서 문구를 멈추며 후속 구현, 피드백, 내부 테스트 수치는 페이지에 노출하지 않는다. 연구는 두 번째 근거로 배치하고, MV는 작은 보조 항목으로 둔다. 실제 명찰 사진은 카메라 방향을 정규화하고 비율을 유지해 웹용으로 인코딩했으며 EXIF/GPS 메타데이터는 포함하지 않는다. 생성 이미지나 재제작 명찰이 아니다. 원문 논문과 공식 채택 기록은 바로 열 수 있으며, 연구 요약은 네이티브 `<details>`로 펼친다. 모든 연락/언어/원문 링크와 펼치기는 JavaScript 없이 동작한다.

## 근거와 해석

대표 논문은 **Ranking Under Biased Missingness: When Model Rank Is Not Identifiable from Sparse Leaderboards**, 단독 저자 Jung Min Kang. NeurIPS 2026 워크숍 **Can We Trust AI Evaluation?** 포스터 채택이다. 메인 컨퍼런스 논문 채택이나 수상으로 표현하지 않는다. [공식 채택 기록](https://neurips.cc/virtual/2026/178314).

큰 그림은 원본 분석 데이터에서 다시 그린 순위 비교다. 같은 정규화된 관측 점수 행렬의 단순 평균 순위와 2PL 잠재특성 추정 순위를 비교한다. 162개 모델 중 ProGAL-VLA가 99위와 22위로 77칸 차이를 보였다. 이는 집계 모형에 따른 불일치이며 정확도 개선·정답 순위 회복을 의미하지 않는다. 논문에 실린 원본 그림으로 표시하지 않는다. 별도 EFSL 논문 결과를 이 채택 연구와 합치지 않는다.

뮤직비디오는 2인 팀 공동 제작 이력이며 [실제 영상](https://www.youtube.com/watch?v=JsT445NqkMk)과 [SBS 보도](https://news.sbs.co.kr/news/endPage.do?news_id=N1008024859)로 연결한다. 트랙션을 추정하지 않는다. Upstage MABC 결선과 언어 이력은 기본 닫힘 상태다.

## 유지보수와 검증

- 한국어/영어의 구조, 링크, 공개 범위를 함께 수정한다.
- 새 문자를 넣으면 두 페이지의 실제 문자로 Pretendard 서브셋을 다시 생성하고 cmap을 대조한다. JetBrains Mono는 언어 전환 EN/KR에만 사용한다.
- 375px·390px 모바일과 데스크톱에서 가로 넘침, 그림 가독성, 아이콘 이름, 접기/펼치기, 언어 전환을 확인한다.
- 연락은 `mailto:gangjeongmin23@gmail.com`이며 전송을 자동 실행하지 않는다.
- Lighthouse 모바일 성능·접근성 목표는 각각95이상, LCP는1.5초 미만이다. 요구 조건과 실제 측정 결과는 구분한다.
- 실제 면접 검토, 체류, 선정 효과는 관찰 전까지 미측정이다. 미리보기의 기술 검증으로 대체하지 않는다.

## 배포

사용자가 완성본 비교를 보고 배포를 승인한 뒤에만 push한다. 배포 후 원격 커밋과 실제 `/kr/`·`/` 응답을 다시 읽어 반영을 확인한다. 저장·로컬 검증·push·라이브 반영은 별도 상태로 기록한다.

로컬 커밋 전 검사는 `.githooks/pre-commit`에서 스테이징된 파일을 대상으로 실행한다. 새 clone에서는 `git config --local core.hooksPath .githooks`로 연결한다. 현재 저장소에는 연결되어 있다. 명시적인 새 방향 승인이 있으면 기준과 검사를 함께 갱신한다.
