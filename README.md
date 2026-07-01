# testofschool.github.io

KANG JUNG MIN 채용 포트폴리오. 수제 HTML/CSS/vanilla JS — 프레임워크·빌드 스텝·트래커 0.

## 구조

```
index.html          EN (정본)
kr/index.html       KR
assets/
  fonts/pretendard/
    PretendardVariable.site-subset.woff2   ← 페이지가 실제 로드하는 파일 (95KB, 아래 설명)
    pretendardvariable-dynamic-subset.css  ← 예비 (dynamic subset 92청크, 미사용)
    woff2-dynamic-subset/                  ← 예비 (텍스트 대개편 시 폴백용)
  fonts/jetbrains-mono/       JetBrains Mono 400/700 woff2 (라틴+기호 서브셋, 각 ~30KB)
  og.png                      OG 이미지 1200×630
sitemap.xml
robots.txt
```

**프로토타입 대비 승인된 델타:** 근거 레이어 제거 · graphite `#6E6A5E`→`#5B574B` · 폰트 CDN→self-host · MV 링크 카드→click-to-load 임베드 · EN|KR 토글 + JSON-LD/OG/canonical · 초기 뷰포트 reveal 즉시 표시(LCP 보호) · JetBrains Mono 500 웨이트 제거(500→400, 2웨이트 셋 유지) · "13 months"→"14 months"(페이지 내 날짜 2025.03→2026.05와 산술 일치하도록 교정).

**폰트 전략 (성능 측정으로 결정):** 처음엔 스펙대로 dynamic subset(92청크)을 연결했으나, EN/KR 페이지가 한글 글리프 때문에 청크 10–19개(230–490KB)를 당겨 Lighthouse 모바일 Perf가 78–85에 묶였다. 두 페이지의 전체 글리프 유니온(529자)+안전 범위(ASCII·Latin-1·자모·기호)를 하나의 woff2로 서브셋하고 가변 웨이트 축을 실사용 범위(400–800)로 잘라 **95KB 단일 요청**으로 바꿈 → Perf 100/100. dynamic subset 파일들은 예비로 유지.

- 소스 오브 트루스: 콘텐츠(수치·문구) = `master_cv_blueprint_20260702.md` / 형태 = `portfolio_design_decisions_20260702.md` / 시각 기준 = `portfolio_prototype_v1.html`
- **외부 요청은 단 1건**: Case 01의 MV 포스터 `i.ytimg.com/vi/JsT445NqkMk/maxresdefault.jpg` (lazy-load, below-fold). 유튜브 iframe(`youtube-nocookie.com`)은 클릭 시에만 로드되는 click-to-load 패턴이라 초기 로드에 외부 스크립트 0.

## 디자인 토큰

| 토큰 | 값 | 용도 | 대비 (on paper) |
|------|-----|------|------|
| `--paper` | `#F7F5EF` | 배경 | — |
| `--ink` | `#17150F` | 본문 | 16.74:1 |
| `--navy` | `#1C4587` | 유일 악센트 — CV와 동일 값 | 8.56:1 |
| `--graphite` | `#5B574B` | 캡션·보조 | 6.62:1 |
| `--hairline` | `#E0DBCC` | 구분선 | — |

폰트: Pretendard Variable (본문 400 / 디스플레이 800, ls −0.035em) + JetBrains Mono (숫자·캡션·메타·태그·원장).
크기: 히어로 `clamp(42px,7.2vw,92px)` / 케이스 제목 `clamp(26px,3.2vw,40px)` / 본문 17px lh1.65 / 캡션 11.5–13px.
폭: 컨테이너 1040px / EN 본문 66ch / **KR 본문 40em (CJK 별도 기준 — EN 값 복사 금지)**.
여백: 히어로 상단 150px / 섹션 88px / 스탯 그리드 22–26px.
애니메이션 2종만: EFSL 차트 draw-on-scroll(IRT 1.6s + 평균 0.5s 지연 페이드, 1회) + 섹션 reveal(550ms). `prefers-reduced-motion` 시 전부 비활성. reveal은 `.js` 클래스 게이팅이라 JS 꺼도 콘텐츠 전부 보임.

## 수정·재생성 방법

- 페이지는 파일당 완결 (HTML 안에 CSS/JS 인라인). EN 수정 시 KR도 같은 위치를 수정할 것 — 구조·클래스는 1:1 동일.
- 새 수치·문구는 blueprint에 먼저 추가 → 두 페이지에 반영 → 아래 검증 재실행.
- **텍스트를 수정하면 폰트 서브셋 재생성 필수** (서브셋에 없는 새 글자는 시스템 폰트로 폴백됨):
  ```bash
  # 1. 두 HTML의 텍스트를 union.txt로 추출 (태그·style·script 제거 후 유니크 문자)
  # 2. Pretendard 원본(릴리즈 zip의 web/variable/woff2/PretendardVariable.woff2)에서:
  python3 -m fontTools.subset PretendardVariable.woff2 --flavor=woff2 --text-file=union.txt \
    --unicodes="U+0020-007E,U+00A0-00FF,U+2013-2026,U+00D7,U+00B1,U+03C1,U+2264-2265,U+20A9,U+25B6,U+2190-2199,U+3131-314E" \
    --layout-features='*' --name-IDs='*' --output-file=sub.woff2
  python3 -m fontTools.varLib.instancer sub.woff2 wght=400:800 \
    -o assets/fonts/pretendard/PretendardVariable.site-subset.woff2
  ```
- OG 이미지 재생성: 토큰 동일한 1200×630 HTML을 headless Chrome으로 `--window-size=1200,630 --screenshot` 캡처.

## 검증 명령 모음 (10항목)

```bash
# 1. 금지 문자열 (전부 0이어야 함)
for p in "Felix Kang" "under review" "first-authored" "Korea's first" "n8n" "Dify" \
         "PyTorch" "Python" "조연출" "6 papers" "최초의 AI 뮤직비디오" \
         "AI Content Producer" "AI Content Creator"; do
  echo "$p: $(grep -rc "$p" index.html kr/index.html | awk -F: '{s+=$NF} END {print s}')"
done

# 2. 무-JS 판독 (텍스트 추출 후 주장 순서 확인)
npx -y html-to-text < index.html | head -100

# 3–5. Lighthouse (모바일 Perf/A11y ≥ 95, LCP < 1.5s)
python3 -m http.server 8080 &
npx -y lighthouse http://localhost:8080 --form-factor=mobile --screenEmulation.mobile \
  --only-categories=performance,accessibility --view

# 6. 외부 링크 전수 curl
grep -oE 'href="https?://[^"]+"' index.html kr/index.html | sort -u

# 7. reduced-motion — DevTools Rendering 패널에서 에뮬레이션
# 8. 375px 뷰포트 — 가로 스크롤 없어야 함
# 9. 수치 대조 — blueprint와 diff
# 10. JSON-LD — validator.schema.org
```

## 배포 후

`cv_generate.js`의 `PORTFOLIO_EN`/`PORTFOLIO_KR` 변수를 사이트 URL(`https://testofschool.github.io/`, `https://testofschool.github.io/kr/`)로 교체 후 `node cv_generate.js` 재실행 — 이력서의 [Coming Soon]/[준비 중]이 실제 URL로 바뀝니다.
