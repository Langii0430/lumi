import streamlit as st
from typing import Dict, List
import random

# -----------------------------
# 반드시 최상단에 있어야 합니다.
# -----------------------------
st.set_page_config(
    page_title="MBTI 무드 탐험소 ✨",
    page_icon="✨",
    layout="wide",
)

# -----------------------------
# 스타일 (과도한 f-string HTML 조합을 피하고, 단순/안정형으로 구성)
# -----------------------------
st.markdown(
    """
<style>
:root{
  --bg1:#0b1020;
  --bg2:#120a2a;
  --card:rgba(255,255,255,0.08);
  --stroke:rgba(255,255,255,0.18);
  --txt:rgba(255,255,255,0.92);
  --muted:rgba(255,255,255,0.70);
  --a1:#7c3aed;
  --a2:#22d3ee;
  --a3:#fb7185;
  --a4:#a3e635;
}
.stApp{
  background:
    radial-gradient(1200px 700px at 10% 5%, rgba(124,58,237,0.35), transparent 55%),
    radial-gradient(900px 600px at 90% 20%, rgba(34,211,238,0.28), transparent 55%),
    radial-gradient(900px 600px at 60% 90%, rgba(251,113,133,0.22), transparent 55%),
    linear-gradient(160deg, var(--bg1), var(--bg2));
  color: var(--txt);
}
.block-container { padding-top: 2.0rem; padding-bottom: 2.5rem; }
.hero{
  border:1px solid var(--stroke);
  background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(34,211,238,0.14));
  border-radius: 22px;
  padding: 20px 22px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}
.hero .title{
  font-size: 2.2rem;
  font-weight: 900;
  letter-spacing:-0.02em;
  margin: 0;
  text-shadow: 0 0 28px rgba(124,58,237,0.30);
}
.hero .sub{
  margin-top: 6px;
  color: var(--muted);
  font-size: 1rem;
}
.pills{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 14px; }
.pill{
  border:1px solid var(--stroke);
  background: rgba(255,255,255,0.06);
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 0.92rem;
}
.card{
  border:1px solid var(--stroke);
  background: rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 18px 55px rgba(0,0,0,0.40);
}
.bigtype{
  font-size: 3.0rem;
  font-weight: 1000;
  letter-spacing:-0.05em;
  margin: 4px 0 0 0;
  background: linear-gradient(90deg, var(--a2), var(--a1), var(--a3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.muted{ color: var(--muted); line-height: 1.55; }
.tags{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 10px; }
.tag{
  border:1px solid var(--stroke);
  background: rgba(255,255,255,0.06);
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 0.9rem;
}
.hr{ height:1px; background: rgba(255,255,255,0.10); margin: 12px 0; }
.badges{ display:flex; flex-wrap:wrap; gap:8px; margin-top: 10px; }
.badge{
  border:1px solid var(--stroke);
  background: rgba(0,0,0,0.18);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.85rem;
}
.stButton>button{
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.20) !important;
  background: linear-gradient(135deg, rgba(124,58,237,0.85), rgba(34,211,238,0.75)) !important;
  color: white !important;
  font-weight: 800 !important;
  padding: 0.65rem 1.0rem !important;
  box-shadow: 0 16px 38px rgba(0,0,0,0.35) !important;
}
.small-note{ font-size:0.9rem; color: rgba(255,255,255,0.62); }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 데이터 (안정형: dict 기반)
# -----------------------------
MBTI: Dict[str, Dict] = {
    "INTJ": {"name":"전략가", "mood":"🧠✨ 설계형", "one":"큰 그림을 설계하고 최적화를 즐깁니다.",
             "strength":["전략/기획","독립적 몰입","장기적 관점"],
             "watch":["감정 표현이 건조해 보일 수 있음","완벽주의 경향"],
             "jobs":["전략기획","데이터/AI","R&D","프로덕트 매니저","컨설턴트"],
             "emoji":"🧠"},
    "INTP": {"name":"논리술사", "mood":"🧪🧠 탐구형", "one":"원리와 구조를 파고들며 새로운 관점을 만듭니다.",
             "strength":["분석력","개념화","호기심"],
             "watch":["결정 지연","현실 실행이 느릴 수 있음"],
             "jobs":["개발자","리서처","데이터 분석가","아키텍트","시스템 기획"],
             "emoji":"🧪"},
    "ENTJ": {"name":"통솔자", "mood":"👑🚀 추진형", "one":"목표를 정하고 밀어붙이는 리더십이 강합니다.",
             "strength":["결단력","조직화","성과 지향"],
             "watch":["강해 보이는 톤","휴식 부족"],
             "jobs":["경영/리더","사업개발","PM","영업 리더","전략 컨설턴트"],
             "emoji":"👑"},
    "ENTP": {"name":"변론가", "mood":"⚡🗣️ 아이디어형", "one":"아이디어를 던지고 실험하며 판을 바꿉니다.",
             "strength":["창의적 발상","순발력","토론/설득"],
             "watch":["산만함","마무리 약함"],
             "jobs":["스타트업","마케팅","기획","프로듀서","크리에이터"],
             "emoji":"⚡"},

    "INFJ": {"name":"옹호자", "mood":"🌙💡 통찰형", "one":"사람과 의미를 깊게 읽고 조용히 세상을 바꿉니다.",
             "strength":["공감+통찰","비전","깊은 관계"],
             "watch":["과몰입/번아웃","경계가 흐려질 수 있음"],
             "jobs":["상담/코칭","콘텐츠 기획","브랜딩","UX 리서처","교육/비영리"],
             "emoji":"🌙"},
    "INFP": {"name":"중재자", "mood":"🕊️🎨 가치형", "one":"가치와 감성을 중심으로 진정성을 추구합니다.",
             "strength":["창작/표현","공감","의미 추구"],
             "watch":["현실 피로","자기비판"],
             "jobs":["작가/디자이너","콘텐츠","상담","브랜딩","교육"],
             "emoji":"🕊️"},
    "ENFJ": {"name":"선도자", "mood":"🌟🤝 성장촉진형", "one":"사람을 연결하고 성장시키는 힘이 큽니다.",
             "strength":["사람 중심 리더십","커뮤니케이션","동기부여"],
             "watch":["과책임","자기 시간 부족"],
             "jobs":["HR/조직문화","교육","PR","세일즈","커뮤니티 운영"],
             "emoji":"🌟"},
    "ENFP": {"name":"활동가", "mood":"🎉🔥 영감형", "one":"가능성을 발견하고 분위기를 살리는 에너지가 있습니다.",
             "strength":["아이디어","관계 형성","적응력"],
             "watch":["집중 분산","감정 기복"],
             "jobs":["마케팅","미디어/콘텐츠","기획","창업","교육"],
             "emoji":"🎉"},

    "ISTJ": {"name":"현실주의자", "mood":"🧱✅ 안정형", "one":"규칙과 책임을 지키며 믿음을 쌓습니다.",
             "strength":["성실함","정확성","신뢰"],
             "watch":["융통성 부족해 보일 수 있음","감정 표현 적음"],
             "jobs":["회계/재무","운영/관리","행정","품질관리","PMO"],
             "emoji":"🧱"},
    "ISFJ": {"name":"수호자", "mood":"🧸🫶 케어형", "one":"세심하게 챙기고 안전한 분위기를 만듭니다.",
             "strength":["배려","성실","세부 관리"],
             "watch":["거절 어려움","자기 희생"],
             "jobs":["간호/보건","교육","CS/운영","인사","서비스 기획"],
             "emoji":"🧸"},
    "ESTJ": {"name":"경영자", "mood":"📣📊 관리형", "one":"현실적인 기준으로 시스템을 세웁니다.",
             "strength":["실행력","관리","책임감"],
             "watch":["강한 직설","융통성 부족"],
             "jobs":["관리자","운영 총괄","영업관리","프로젝트 리드","조직 리더"],
             "emoji":"📣"},
    "ESFJ": {"name":"집정관", "mood":"💐🤗 사교케어형", "one":"관계를 따뜻하게 유지하고 팀을 살핍니다.",
             "strength":["친화력","조율","돌봄"],
             "watch":["타인 시선 과의식","갈등 회피"],
             "jobs":["서비스/CS","교육","커뮤니티 매니저","인사","코디네이터"],
             "emoji":"💐"},

    "ISTP": {"name":"장인", "mood":"🛠️😎 실전형", "one":"필요하면 바로 해결하는 실용주의자입니다.",
             "strength":["문제 해결","침착함","도구/기술"],
             "watch":["감정 표현 최소","계획이 느슨할 수 있음"],
             "jobs":["엔지니어","개발","보안","영상/촬영(테크)","메이커"],
             "emoji":"🛠️"},
    "ISFP": {"name":"모험가", "mood":"🌿🎧 감각예술형", "one":"감각과 취향으로 분위기를 만들고 표현합니다.",
             "strength":["미적 감각","공감","유연함"],
             "watch":["우유부단","갈등 회피"],
             "jobs":["디자이너","사진/영상","브랜드/굿즈","공예","플로리스트"],
             "emoji":"🌿"},
    "ESTP": {"name":"사업가", "mood":"🏎️💥 액션형", "one":"현장에서 빠르게 판단하고 기회를 잡습니다.",
             "strength":["순발력","대담함","현장 적응"],
             "watch":["충동","루틴 유지 어려움"],
             "jobs":["영업","창업","이벤트/프로모션","트레이너","현장 운영"],
             "emoji":"🏎️"},
    "ESFP": {"name":"연예인", "mood":"🎈🌈 분위기메이커형", "one":"사람을 즐겁게 하고 경험을 풍성하게 만듭니다.",
             "strength":["표현력","친화력","현장 에너지"],
             "watch":["계획 약함","집중 분산"],
             "jobs":["크리에이터","MC/진행","서비스","세일즈","공연/이벤트"],
             "emoji":"🎈"},
}

GROUPS = {
    "분석가(Analysts) 🧠": ["INTJ", "INTP", "ENTJ", "ENTP"],
    "외교관(Diplomats) 🌙": ["INFJ", "INFP", "ENFJ", "ENFP"],
    "관리자(Sentinels) 🧱": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    "탐험가(Explorers) 🛠️": ["ISTP", "ISFP", "ESTP", "ESFP"],
}

# 재미용 궁합(추천) 테이블
COMPAT: Dict[str, List[str]] = {
    "INTJ": ["ENFP", "ENTP", "INFJ"],
    "INTP": ["ENTJ", "ENFJ", "ISTJ"],
    "ENTJ": ["INTP", "INFP", "ISFP"],
    "ENTP": ["INFJ", "INTJ", "ISFJ"],
    "INFJ": ["ENFP", "ENTP", "ISFJ"],
    "INFP": ["ENFJ", "ENTJ", "ISFP"],
    "ENFJ": ["INFP", "INTP", "ISTP"],
    "ENFP": ["INFJ", "INTJ", "ISTJ"],
    "ISTJ": ["ENFP", "ESFP", "INTP"],
    "ISFJ": ["ENTP", "ESFP", "INFJ"],
    "ESTJ": ["ISFP", "INFP", "ISTP"],
    "ESFJ": ["ISTP", "INTP", "ISFP"],
    "ISTP": ["ENFJ", "ESFJ", "INTJ"],
    "ISFP": ["ENTJ", "ESTJ", "INFP"],
    "ESTP": ["ISFJ", "INFJ", "ISTJ"],
    "ESFP": ["ISTJ", "ISFJ", "INTJ"],
}

VIBES = [
    "✨ 오늘은 ‘반짝 모드’입니다",
    "🌙 오늘은 ‘잔잔+깊이’ 모드입니다",
    "🔥 오늘은 ‘추진력’ 모드입니다",
    "🌿 오늘은 ‘안정/감성’ 모드입니다",
    "⚡ 오늘은 ‘아이디어’ 모드입니다",
    "🎉 오늘은 ‘사교/즐거움’ 모드입니다",
]

def render_tags(items: List[str], icon: str) -> str:
    safe = []
    for x in items:
        safe.append(f'<div class="tag">{icon} {x}</div>')
    return '<div class="tags">' + "".join(safe) + "</div>"

# -----------------------------
# 헤더
# -----------------------------
st.markdown(
    """
<div class="hero">
  <div class="title">MBTI 무드 탐험소 ✨</div>
  <div class="sub">MBTI를 선택하시면 성향 · 직업 · 친구 추천을 “재미용”으로 화려하게 보여드립니다.</div>
  <div class="pills">
    <div class="pill">💡 성향 한 문장</div>
    <div class="pill">💎 강점</div>
    <div class="pill">🧯 주의 포인트</div>
    <div class="pill">💼 직업 추천</div>
    <div class="pill">🫶 친구 MBTI 추천</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("### 🎛️ 설정")
    group = st.selectbox("카테고리", list(GROUPS.keys()), index=1)
    selected = st.selectbox("MBTI", GROUPS[group], index=0)
    st.markdown("---")
    vibe_mode = st.radio("오늘의 무드", ["랜덤 🎲"] + [v.split()[0] for v in VIBES], index=0)
    show_extra = st.toggle("추가(감정 번역기) 표시", value=True)
    st.markdown("---")
    st.markdown('<div class="small-note">※ 본 앱은 재미용이며, 개인차가 있습니다.</div>', unsafe_allow_html=True)

# 무드 라인
if vibe_mode == "랜덤 🎲":
    vibe_line = random.choice(VIBES)
else:
    mapping = {v.split()[0]: v for v in VIBES}
    vibe_line = mapping.get(vibe_mode, random.choice(VIBES))

info = MBTI.get(selected, None)
if info is None:
    st.error("선택된 MBTI 데이터를 찾을 수 없습니다. 데이터 테이블을 확인해 주세요.")
    st.stop()

friends = COMPAT.get(selected, [])
if not friends:
    # 혹시라도 누락되면 랜덤 3개
    friends = random.sample(list(MBTI.keys()), 3)

# -----------------------------
# 본문 레이아웃
# -----------------------------
left, right = st.columns([1.05, 1.0], gap="large")

with left:
    st.markdown(
        f"""
<div class="card">
  <div class="badges">
    <div class="badge">{info["emoji"]} 타입</div>
    <div class="badge">{info["mood"]}</div>
    <div class="badge">{vibe_line}</div>
  </div>

  <div class="bigtype">{selected}</div>
  <div class="muted"><b>{info["name"]}</b> · {info["one"]}</div>

  <div class="hr"></div>
  <h3>🌈 성향 요약</h3>
  <div class="muted">{info["mood"]}<br/>“{info["one"]}”</div>

  <div class="hr"></div>
  <h3>💎 강점</h3>
  {render_tags(info["strength"], "✅")}

  <div class="hr"></div>
  <h3>🧯 주의 포인트</h3>
  {render_tags(info["watch"], "⚠️")}
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    friend_html = []
    for t in friends:
        ti = MBTI[t]
        friend_html.append(f'<div class="tag">🫶 <b>{t}</b> · {ti["name"]} · {ti["mood"]}</div>')
    friend_html = '<div class="tags">' + "".join(friend_html) + "</div>"

    st.markdown(
        f"""
<div class="card">
  <h3>💼 어울리는 직업 추천</h3>
  <div class="muted">재미용 추천입니다. 팀 문화/업무 환경에 따라 체감이 달라질 수 있습니다 🙂</div>
  <div class="hr"></div>
  {render_tags(info["jobs"], "💼")}

  <div class="hr"></div>
  <h3>🧡 친해지면 좋은 사람(성향) 추천</h3>
  <div class="muted">서로의 차이를 보완해 주는 조합을 우선으로 제안드립니다.</div>
  <div class="hr"></div>
  {friend_html}
</div>
""",
        unsafe_allow_html=True,
    )

# -----------------------------
# 추가 섹션
# -----------------------------
if show_extra:
    st.write("")
    a, b = st.columns(2, gap="large")

    FEEL_HURT = "😶‍🌫️ 겉은 괜찮아 보여도, 속으로는 정리 시간이 필요하실 수 있습니다."
    FEEL_HAPPY = "🥳 기분이 좋을 때는 ‘좋은 에너지’를 주변에 나누고 싶어지는 경향이 있습니다."

    with a:
        st.markdown(
            f"""
<div class="card">
  <h3>🎭 한 줄 감정 번역기: 상했을 때</h3>
  <div class="muted">{FEEL_HURT}</div>
  <div class="hr"></div>
  <div class="muted">추천 대처 🧩: “지금 어떤 도움이 필요하세요?”라고 물어보시면 회복이 빨라질 수 있습니다.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            f"""
<div class="card">
  <h3>🎭 한 줄 감정 번역기: 좋을 때</h3>
  <div class="muted">{FEEL_HAPPY}</div>
  <div class="hr"></div>
  <div class="muted">친해지는 팁 🌈: 칭찬은 “구체적으로” 해주시면 친밀감이 빠르게 올라갈 수 있습니다.</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.write("")
st.caption("⚠️ 본 앱은 재미용이며, MBTI는 개인을 단정하기보다 대화의 소재로 활용하시는 편이 안전합니다.")
