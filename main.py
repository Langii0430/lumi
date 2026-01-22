import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="MBTI 무드 탐험소 ✨",
    page_icon="✨",
    layout="wide",
)

# -----------------------------
# Fancy CSS
# -----------------------------
CSS = """
<style>
:root{
  --bg1:#0b1020;
  --bg2:#120a2a;
  --card:rgba(255,255,255,0.08);
  --card2:rgba(255,255,255,0.12);
  --stroke:rgba(255,255,255,0.18);
  --txt:rgba(255,255,255,0.92);
  --muted:rgba(255,255,255,0.70);
  --accent1:#7c3aed; /* purple */
  --accent2:#22d3ee; /* cyan */
  --accent3:#fb7185; /* pink */
  --accent4:#a3e635; /* lime */
}

.stApp{
  background:
    radial-gradient(1200px 700px at 10% 5%, rgba(124,58,237,0.35), transparent 55%),
    radial-gradient(900px 600px at 90% 20%, rgba(34,211,238,0.28), transparent 55%),
    radial-gradient(900px 600px at 60% 90%, rgba(251,113,133,0.22), transparent 55%),
    linear-gradient(160deg, var(--bg1), var(--bg2));
  color: var(--txt);
}

.block-container { padding-top: 2.2rem; padding-bottom: 3rem; }

.header-wrap{
  border: 1px solid var(--stroke);
  background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(34,211,238,0.14));
  box-shadow
