"""
ExamZen AI - Ultimate Mobile Ecosystem
Features: Mentor, Fixer, Smart Planner, QuickQuiz, Analytics Vault.
Powered by Google Gemini 2.5 Flash
"""
import streamlit as st
import os
import json
from datetime import datetime
from google import genai
from google.genai import types
# ─── PAGE CONFIGURATION ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExamZen | Ultimate AI Coach",
    page_icon="⚛️",
    layout="centered",
    initial_sidebar_state="collapsed",
)
# ─── PREMIUM CSS & ANIMATIONS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
:root {
  --bg: #030712;
  --surface: #111827;
  --card: #1F2937;
  --border: #374151;
  --primary: #38BDF8;
  --primary-glow: rgba(56, 189, 248, 0.3);
  --secondary: #818CF8;
  --success: #10B981;
  --warning: #F59E0B;
  --danger: #EF4444;
  --text: #F9FAFB;
  --muted: #9CA3AF;
}
html, body, [class*="css"], .stApp {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}
/* Hide Streamlit elements */
#MainMenu, footer, header, [data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 0 1rem 6rem 1rem !important; max-width: 650px !important; margin: 0 auto !important; }
/* Dynamic Animated Background */
.stApp::before {
  content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background:
    radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.05), transparent 30%),
    radial-gradient(circle at 90% 80%, rgba(129, 140, 248, 0.05), transparent 30%);
  z-index: 0; pointer-events: none;
}
/* Keyframes */
@keyframes slideUp { 0% { opacity: 0; transform: translateY(15px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes popIn { 0% { opacity: 0; transform: scale(0.95); } 100% { opacity: 1; transform: scale(1); } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
/* Top Header */
.top-header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(3, 7, 18, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  padding: 1rem; margin: 0 -1rem 1.5rem -1rem; border-bottom: 1px solid rgba(255,255,255,0.05);
  display: flex; justify-content: space-between; align-items: center;
}
.logo-text { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.status-badge { background: rgba(16, 185, 129, 0.1); color: var(--success); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.2); display: flex; align-items: center; gap: 5px; }
.status-badge.error { background: rgba(239, 68, 68, 0.1); color: var(--danger); border-color: rgba(239, 68, 68, 0.2); }
.pulse-dot { width: 6px; height: 6px; background-color: currentColor; border-radius: 50%; box-shadow: 0 0 8px currentColor; animation: pulse 2s infinite; }
/* 5-Tab Bottom Navigation */
.bottom-nav-container {
  position: fixed; bottom: 0; left: 0; width: 100%; z-index: 100;
  background: rgba(17, 24, 39, 0.95); backdrop-filter: blur(20px); border-top: 1px solid rgba(255,255,255,0.05);
  display: flex; justify-content: space-around; padding: 0.6rem 0; padding-bottom: env(safe-area-inset-bottom, 0.6rem);
}
.nav-btn { display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--muted); padding: 8px; border-radius: 12px; transition: 0.3s ease; width: 20%; }
.nav-btn.active { color: var(--primary); }
.nav-btn.active .nav-icon { transform: translateY(-2px); text-shadow: 0 0 15px var(--primary-glow); }
.nav-icon { font-size: 1.3rem; transition: 0.3s; }
.nav-text { font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
/* Invisible Click Overlay for Nav */
.click-overlay { position: fixed; bottom: 0; left: 0; width: 100%; height: 75px; z-index: 101; display: flex; justify-content: space-around; }
.click-overlay .stButton, .click-overlay .stButton > button { width: 100% !important; height: 100% !important; opacity: 0 !important; cursor: pointer !important; margin: 0!important; padding: 0!important; }
/* Glass Cards & Containers */
.glass-card { background: rgba(31, 41, 55, 0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; animation: slideUp 0.5s ease-out forwards; backdrop-filter: blur(10px); }
.glass-card:hover { border-color: rgba(56, 189, 248, 0.4); transform: translateY(-2px); transition: 0.3s; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 700; line-height: 1.1; margin-bottom: 1rem; color: white; }
.hero-subtitle { color: var(--muted); font-size: 1.05rem; line-height: 1.5; margin-bottom: 1.5rem; }
/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-bottom: 1.5rem; animation: popIn 0.5s ease-out forwards; }
.stat-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 1rem 0.5rem; text-align: center; }
.stat-num { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; color: var(--text); }
.stat-label { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; margin-top: 4px; }
/* Inputs and Buttons */
.stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] { background: rgba(17, 24, 39, 0.8) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: white !important; padding: 0.75rem !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px var(--primary-glow) !important; }
.stButton > button { background: linear-gradient(135deg, var(--primary), var(--secondary)) !important; color: #000 !important; border: none !important; border-radius: 12px !important; font-weight: 700 !important; padding: 0.75rem !important; width: 100% !important; transition: 0.3s !important; text-transform: uppercase; letter-spacing: 0.5px; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(56, 189, 248, 0.4) !important; }
/* Chat Bubbles */
.chat-user { background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); color: white; padding: 1rem; border-radius: 16px 16px 4px 16px; margin: 0.5rem 0 0.5rem auto; max-width: 85%; font-size: 0.95rem; animation: slideUp 0.3s ease-out; }
.chat-ai { background: rgba(31, 41, 55, 0.5); border: 1px solid rgba(255,255,255,0.05); color: var(--text); padding: 1rem; border-radius: 4px 16px 16px 16px; margin: 0.5rem auto 0.5rem 0; max-width: 90%; font-size: 0.95rem; line-height: 1.6; animation: slideUp 0.3s ease-out; }
.chat-avatar { font-size: 1.2rem; margin-right: 8px; vertical-align: middle; }
/* Interactive Quiz Cards */
.quiz-card { background: rgba(31,41,55,0.7); border-radius: 16px; border: 1px solid var(--border); padding: 1.5rem; margin-bottom: 1.5rem; }
.quiz-badge { background: rgba(129, 140, 248, 0.15); color: var(--secondary); padding: 4px 10px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-bottom: 1rem; display: inline-block; }
.stRadio > div { background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
hr { border-color: rgba(255,255,255,0.1); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)
# ─── AI ENGINE CONNECTION ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def initialize_ai():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: return None
        return genai.Client(api_key=api_key)
    except Exception:
        return None
def ask_gemini(client, user_prompt, system_prompt, json_mode=False):
    try:
        config_args = {
            "system_instruction": system_prompt,
            "temperature": 0.7,
        }
        if json_mode:
            config_args["response_mime_type"] = "application/json"
           
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_args)
        )
        return response.text
    except Exception as e:
        return f"🚨 API Error: {str(e)}"
# ─── STATE MANAGEMENT ─────────────────────────────────────────────────────────
if "active_tab" not in st.session_state: st.session_state.active_tab = "home"
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "mistake_vault" not in st.session_state: st.session_state.mistake_vault = []
if "quiz_state" not in st.session_state: st.session_state.quiz_state = {}
if "stats" not in st.session_state: st.session_state.stats = {"questions": 0, "fixed": 0, "quizzes_taken": 0, "score": 0}
# ─── HEADER ───────────────────────────────────────────────────────────────────
client = initialize_ai()
status_html = "<span class='status-badge'><div class='pulse-dot'></div> Live</span>" if client else "<span class='status-badge error'><div class='pulse-dot'></div> No Key</span>"
st.markdown(f"""
<div class='top-header'>
    <div class='logo-text'>⚛️ ExamZen</div>
    <div>{status_html}</div>
</div>
""", unsafe_allow_html=True)
# ─── 5-TAB NAVIGATION OVERLAY ─────────────────────────────────────────────────
tabs = [
    ("home", "🏠", "Home"),
    ("mentor", "🧑‍🏫", "Mentor"),
    ("fixer", "🔬", "Fixer"),
    ("quiz", "⚡", "Quiz"),
    ("dash", "📊", "Vault")
]
nav_ui = "<div class='bottom-nav-container'>"
for tab_id, icon, label in tabs:
    active_class = "active" if st.session_state.active_tab == tab_id else ""
    nav_ui += f"<div class='nav-btn {active_class}'><span class='nav-icon'>{icon}</span><span class='nav-text'>{label}</span></div>"
nav_ui += "</div>"
st.markdown(nav_ui, unsafe_allow_html=True)
st.markdown("<div class='click-overlay'>", unsafe_allow_html=True)
cols = st.columns(5)
for i, (tab_id, _, _) in enumerate(tabs):
    with cols[i]:
        if st.button(" ", key=f"nav_{tab_id}", use_container_width=True):
            st.session_state.active_tab = tab_id
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
current_tab = st.session_state.active_tab
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: HOME DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if current_tab == "home":
    st.markdown("<div class='hero-title'>Master JEE & NEET<br><span style='color:var(--primary)'>with AI.</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Your ultimate study ecosystem. Chat, diagnose, test, and plan — all in your pocket.</div>", unsafe_allow_html=True)
   
    # Quick Stats
    st.markdown(f"""
    <div class='stats-grid'>
        <div class='stat-box'><div class='stat-num' style='color:var(--primary)'>{st.session_state.stats['questions']}</div><div class='stat-label'>Qs Asked</div></div>
        <div class='stat-box'><div class='stat-num' style='color:var(--secondary)'>{st.session_state.stats['fixed']}</div><div class='stat-label'>Errors Fixed</div></div>
        <div class='stat-box'><div class='stat-num' style='color:var(--success)'>{st.session_state.stats['quizzes_taken']}</div><div class='stat-label'>Quizzes Done</div></div>
    </div>
    """, unsafe_allow_html=True)
   
    st.markdown("""
    <div class='glass-card'>
        <h3 style='margin:0 0 5px 0; color: #38BDF8; font-size: 1.1rem;'>🧑‍🏫 Interactive Mentor</h3>
        <p style='color: var(--muted); font-size: 0.85rem; margin:0;'>Chat with Arya. Explains complex physics and chemistry using real-world analogies.</p>
    </div>
    <div class='glass-card' style='animation-delay: 0.1s;'>
        <h3 style='margin:0 0 5px 0; color: #818CF8; font-size: 1.1rem;'>🔬 Deep Correctify</h3>
        <p style='color: var(--muted); font-size: 0.85rem; margin:0;'>Paste your wrong answer. The AI pinpoints your exact conceptual misunderstanding.</p>
    </div>
    <div class='glass-card' style='animation-delay: 0.2s;'>
        <h3 style='margin:0 0 5px 0; color: #10B981; font-size: 1.1rem;'>⚡ Infinite Quizzes</h3>
        <p style='color: var(--muted); font-size: 0.85rem; margin:0;'>Generate custom MCQs on any topic instantly and get real-time AI grading.</p>
    </div>
    """, unsafe_allow_html=True)
   
    if not client: st.error("⚠️ Setup Required: Add your GEMINI_API_KEY in the app secrets.")
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: MENTOR
# ══════════════════════════════════════════════════════════════════════════════
elif current_tab == "mentor":
    st.markdown("<h2 style='color: white; margin:0;'>Arya Mentor 🧑‍🏫</h2><p style='color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem;'>Your 24/7 personal IITian tutor.</p>", unsafe_allow_html=True)
   
    if not client: st.error("API Key required.")
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user": st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else: st.markdown(f"<div class='chat-ai'><span class='chat-avatar'>⚡</span>{msg['content']}</div>", unsafe_allow_html=True)
       
        user_q = st.chat_input("Ask about Mechanics, Organic Chem, Genetics...")
       
        if user_q:
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            st.session_state.stats['questions'] += 1
            st.markdown(f"<div class='chat-user'>{user_q}</div>", unsafe_allow_html=True)
           
            with st.spinner("Arya is analyzing..."):
                sys_prompt = "You are Arya, an elite JEE/NEET tutor. 1. Use ONE vivid real-world analogy. 2. Explain the core concept. 3. Provide the formula if applicable. 4. Give one 'Exam Trap' warning. Format neatly with Markdown."
                reply = ask_gemini(client, user_q, sys_prompt)
               
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: FIXER
# ══════════════════════════════════════════════════════════════════════════════
elif current_tab == "fixer":
    st.markdown("<h2 style='color: white; margin:0;'>Correctify 🔬</h2><p style='color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem;'>Find the exact gap in your logic.</p>", unsafe_allow_html=True)
   
    if not client: st.error("API Key required.")
    else:
        q_text = st.text_area("The Question", placeholder="Paste the original question here...")
        ans_text = st.text_area("Your Wrong Answer / Reasoning ✱", placeholder="Explain how you tried to solve it. E.g., 'I used v=u+at but got the wrong sign for gravity.'")
       
        if st.button("Diagnose Logic Error"):
            if not ans_text: st.warning("Please enter your wrong reasoning!")
            else:
                with st.spinner("Scanning your logic..."):
                    sys = "You are a diagnostic tutor for JEE/NEET. 1) Pinpoint the exact logical error. 2) Show the correct step-by-step approach. 3) Provide a Memory Hook to never forget this. Use clear headings."
                    prompt = f"Question: {q_text}\nStudent's attempt: {ans_text}"
                    result = ask_gemini(client, prompt, sys)
               
                st.session_state.stats['fixed'] += 1
                st.session_state.mistake_vault.append({"date": datetime.now().strftime("%b %d"), "topic": q_text[:30]+"...", "fix": result})
                st.balloons()
                st.markdown(f"<div class='glass-card' style='border-top: 3px solid var(--success);'>{result}</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: QUICK QUIZ (NEW)
# ══════════════════════════════════════════════════════════════════════════════
elif current_tab == "quiz":
    st.markdown("<h2 style='color: white; margin:0;'>QuickQuiz ⚡</h2><p style='color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem;'>Generate instant MCQs on any topic.</p>", unsafe_allow_html=True)
   
    if not client: st.error("API Key required.")
    else:
        topic = st.text_input("Enter Topic to Test", placeholder="e.g. Bohr's Atomic Model")
        if st.button("Generate Mini-Test"):
            if not topic: st.warning("Enter a topic first!")
            else:
                with st.spinner("Generating targeted questions..."):
                    sys = """You are a JEE/NEET examiner. Generate EXACTLY 3 multiple choice questions on the requested topic.
                    Return ONLY a valid JSON array of objects. Schema:
                    [{"q": "Question text", "options": ["A", "B", "C", "D"], "correct_idx": 0, "explanation": "Why this is correct."}]"""
                    raw_json = ask_gemini(client, topic, sys, json_mode=True)
                    try:
                        q_data = json.loads(raw_json)
                        st.session_state.quiz_state = {"active": True, "data": q_data, "submitted": False, "score": 0, "answers": [0,0,0]}
                        st.session_state.stats['quizzes_taken'] += 1
                        st.rerun()
                    except:
                        st.error("Failed to generate quiz. Try a different topic.")
       
        qs = st.session_state.quiz_state
        if qs.get("active"):
            st.markdown("<hr>", unsafe_allow_html=True)
            with st.form("quiz_form"):
                for i, q in enumerate(qs["data"]):
                    st.markdown(f"<div class='quiz-badge'>Question {i+1}</div>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='color:white;'>{q['q']}</h4>", unsafe_allow_html=True)
                    qs["answers"][i] = st.radio(f"Select answer for Q{i+1}", q["options"], key=f"q_{i}", label_visibility="collapsed")
                    st.markdown("<br>", unsafe_allow_html=True)
               
                if st.form_submit_button("Submit Answers"):
                    qs["submitted"] = True
                    st.rerun()
           
            if qs.get("submitted"):
                st.markdown("### 📝 Results")
                score = 0
                for i, q in enumerate(qs["data"]):
                    student_ans = qs["answers"][i]
                    correct_ans = q["options"][q["correct_idx"]]
                    if student_ans == correct_ans:
                        score += 1
                        st.success(f"**Q{i+1}: Correct!** {q['explanation']}")
                    else:
                        st.error(f"**Q{i+1}: Incorrect.** You chose {student_ans}. Correct was {correct_ans}. \n\n*Explanation:* {q['explanation']}")
                st.info(f"🏆 Final Score: {score}/3")
                if st.button("Reset Quiz"):
                    st.session_state.quiz_state = {}
                    st.rerun()
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: PLANNER & VAULT
# ══════════════════════════════════════════════════════════════════════════════
elif current_tab == "dash":
    st.markdown("<h2 style='color: white; margin:0;'>Dashboard 📊</h2><p style='color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem;'>Your Planner and Mistake Vault.</p>", unsafe_allow_html=True)
   
    tab1, tab2 = st.tabs(["📅 Timetable", "🗄️ Mistake Vault"])
   
    with tab1:
        st.markdown("#### Smart Schedule Generator")
        exam = st.selectbox("Exam", ["JEE Main", "NEET UG", "JEE Advanced"], label_visibility="collapsed")
        weak_t = st.text_area("Weak Topics", placeholder="e.g. Fluids, Integration")
        if st.button("Create 7-Day Plan"):
            if not weak_t: st.warning("Enter weak topics.")
            else:
                with st.spinner("Optimizing schedule..."):
                    sys = "Act as a JEE/NEET study planner. Output a beautiful Markdown table for a 7-day study plan focusing heavily on the provided weak topics using spaced repetition."
                    plan = ask_gemini(client, f"Exam: {exam}. Focus: {weak_t}.", sys)
                st.markdown(f"<div class='glass-card'>{plan}</div>", unsafe_allow_html=True)
               
    with tab2:
        st.markdown("#### Logged Mistakes")
        if not st.session_state.mistake_vault:
            st.info("You haven't logged any mistakes yet. Use the Fixer tool to populate this vault!")
        else:
            for entry in reversed(st.session_state.mistake_vault):
                with st.expander(f"🔴 {entry['date']} - {entry['topic']}"):
                    st.markdown(entry["fix"])
            if st.button("Clear Vault"):
                st.session_state.mistake_vault = []
                st.rerun()
