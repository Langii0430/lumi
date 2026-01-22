pip install -U streamlit
streamlit run main.py

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
    "ENFP": {"name":"활동가", "mood":"🎉🔥 영감형", "one":"가능성을 발견하고 분위기를 살리는

