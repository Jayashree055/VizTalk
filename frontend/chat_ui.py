import streamlit as st
import streamlit.components.v1 as components
import os
# import json
import requests
import pandas as pd 
import random
from database import SessionLocal
from models import Message
try:
    from streamlit_mic_recorder import mic_recorder
except:
    mic_recorder = None
import whisper

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

# CHAT_DIR = "saved_chats"
API_URL = "https://viztalk-backend.onrender.com/query"


# ---------- LOAD WHISPER ----------
@st.cache_resource
def load_model():
    return whisper.load_model("base")


# ---------- AUTO VOICE ----------
def auto_speak(text):
    safe_text = text.replace('"', "'")
    components.html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{safe_text}");
        msg.rate = 1;
        msg.pitch = 1;
        msg.lang = "en-US";
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )


# ---------- GENERATE INSIGHTS ----------
def generate_insight(df, x, y):
    if df.empty or x not in df.columns or y not in df.columns:
        return ["I generated your dashboard."]
    insights = []
    try:
        top_row = df.sort_values(by=y, ascending=False).iloc[0]
        bottom_row = df.sort_values(by=y, ascending=True).iloc[0]
        insights.append(f"{top_row[x]} has the highest {y} with a value of {top_row[y]}.")
        insights.append(f"{bottom_row[x]} has the lowest {y} with a value of {bottom_row[y]}.")
        insights.append(f"This chart compares {y} across different {x} categories.")
    except Exception:
        insights.append(f"The dashboard shows {y} grouped by {x}.")
    return insights


def save_message(username, role, content):

    db = SessionLocal()

    msg = Message(
        username=username,
        role=role,
        content=content
    )

    db.add(msg)
    db.commit()


# ---------- RUN QUERY ----------
def run_query(prompt, from_voice=False):
    st.session_state.messages.append({
        "role": "user",
        "content": str(prompt)
    })
    save_message(st.session_state.user, "user", prompt)
    with st.spinner("Processing your request..."):
        try:
            response = requests.post(
                API_URL,
                json={"prompt": prompt},
                timeout=60
            )
            result = response.json()
            sql = result.get("sql")
            data = result.get("data")
            chart = result.get("chart")
            x = result.get("x")
            y = result.get("y")
        except Exception as e:
            st.error(f"Backend error: {e}")
            return
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Here is the generated dashboard",
        "sql": sql,
        "data": data,
        "chart": chart,
        "x": x,
        "y": y
    })


# ---------- MAIN CHAT ----------
def render_chat():
    model = load_model()

    # ── INJECT ALL STYLES ──
    st.markdown("""
    <style>
    /* ── BASE ── */
    [data-testid="stAppViewContainer"] {
        background: #080C14 !important;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }
    [data-testid="stAppViewBlockContainer"] { background: transparent !important; }
    header[data-testid="stHeader"]          { background: transparent !important; }
    # [data-testid="stToolbar"]               { display: none !important; }
    #MainMenu, footer                       { visibility: hidden; }

    /* ── GREETING ── */
    .greeting-block {
        padding: 32px 0 24px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 24px;
    }
    .greeting-name {
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #F1F5F9;
        letter-spacing: -0.3px;
        margin-bottom: 6px;
    }
    .greeting-sub {
        font-size: 15px;
        color: #94A3B8;
        font-weight: 400;
    }

    /* ── CHAT MESSAGES ── */
    .stChatMessage p {
        color: #E2E8F0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
    }

    /* ── DATA TABLE ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    [data-testid="stDataFrame"] * {
        color: #CBD5E1 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
    }
                
    [data-testid="collapsedControl"] {
    display: flex !important;
    background: rgba(59,130,246,0.2) !important;
    border-radius: 0 8px 8px 0 !important;
    width: 24px !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #60A5FA !important;
    }

    /* ── HIDE DATAFRAME COLUMN MENU (3 dots) ── */
    [data-testid="stDataFrame"] [data-testid="column-header-menu-button"],
    [data-testid="stDataFrame"] button[aria-label="More options"],
    [data-testid="stDataFrame"] .glideDataEditor button,
    .dvn-scroller [data-testid="column-header-menu"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
    }


             
    
    /* ── SQL & TABLE SECTION LABELS ── */
    .section-block-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #475569;
        margin: 18px 0 8px 0;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }

    /* ── CUSTOM SQL TOGGLE (pure HTML — no Streamlit expander, no keyboard icon) ── */
    details.sql-toggle {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        margin: 14px 0 4px 0;
        overflow: hidden;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }
    details.sql-toggle summary {
        list-style: none;
        padding: 11px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        user-select: none;
        transition: color 0.2s, background 0.2s;
    }
    details.sql-toggle summary::-webkit-details-marker { display: none; }
    details.sql-toggle summary::before {
        content: '›';
        font-size: 16px;
        font-weight: 600;
        color: #3B82F6;
        transition: transform 0.2s ease;
        display: inline-block;
        line-height: 1;
    }
    details.sql-toggle[open] summary::before { transform: rotate(90deg); }
    details.sql-toggle summary:hover {
        color: #94A3B8;
        background: rgba(255,255,255,0.03);
    }
    details.sql-toggle pre {
        margin: 0;
        padding: 14px 16px;
        background: rgba(255,255,255,0.02);
        border-top: 1px solid rgba(255,255,255,0.05);
        overflow-x: auto;
    }
    details.sql-toggle pre code {
        color: #7DD3FC;
        font-size: 13px;
        font-family: 'Fira Code', 'Cascadia Code', monospace;
        background: transparent;
        border: none;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* ── INSIGHT CARDS ── */
    .insights-wrap  { margin-top: 20px; }
    .insights-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #3B82F6;
        margin-bottom: 12px;
    }
    .insight-card {
        background: rgba(59,130,246,0.05);
        border: 1px solid rgba(59,130,246,0.15);
        border-left: 3px solid #3B82F6;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #CBD5E1 !important;
        line-height: 1.65;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }

    /* ── CHART SECTION LABEL ── */
    .chart-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #475569;
        margin: 20px 0 10px;
    }

    /* ── RESULT HEADER ── */
    .result-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .result-dot {
        width: 8px;
        height: 8px;
        background: #3B82F6;
        border-radius: 50%;
        animation: resultPulse 2s ease-in-out infinite;
    }
    @keyframes resultPulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }
    .result-title {
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: #E2E8F0 !important;
    }

    /* ── CHAT INPUT ── */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #E2E8F0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        background: transparent !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #334155 !important; }
    [data-testid="stBottomBlockContainer"] {
        background: #080C14 !important;
        border-top: 1px solid rgba(255,255,255,0.05) !important;
        padding-top: 12px !important;
    }

    /* ── SPINNER ── */
    [data-testid="stSpinner"] > div { border-top-color: #3B82F6 !important; }
    [data-testid="stSpinner"] p {
        color: #475569 !important;
        font-size: 13px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── ALERTS ── */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
    }

    /* ── CHART SVG ── */
    svg text { fill: #64748B !important; font-family: 'DM Sans', sans-serif !important; }

    /* ── HIDE CHART TOOLBAR & ALL ELEMENT TOOLBARS ── */
    [data-testid="stVegaLiteChart"] details,
    [data-testid="stVegaLiteChart"] summary,
    .vega-embed .vega-actions,
    .vega-embed details,
    .vega-embed summary {
        display: none !important;
        visibility: hidden !important;
    }
    # [data-testid="stElementToolbar"],
    # [data-testid="stElementToolbarButton"],
    # [data-testid="StyledFullScreenButton"],
    # button[title="View fullscreen"],
    # button[title="Show data"],
    # button[title="Copy to clipboard"],
    # button[aria-label="View fullscreen"],
    # button[aria-label="Copy to clipboard"] {
    #     display: none !important;
    #     visibility: hidden !important;
    #     opacity: 0 !important;
    #     pointer-events: none !important;
    # }

    /* ── ALL BUTTONS ── */
    .stButton > button {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #94A3B8 !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: rgba(59,130,246,0.1) !important;
        border-color: rgba(59,130,246,0.3) !important;
        color: #93C5FD !important;
        transform: translateY(-1px) !important;
    }

    /* ── HOME BUTTON ── */
    .home-btn-wrap .stButton > button {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        color: #E2E8F0 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        letter-spacing: 0.3px !important;
        backdrop-filter: blur(8px) !important;
        white-space: nowrap !important;
        border-radius: 10px !important;
    }
    .home-btn-wrap .stButton > button:hover {
        background: rgba(59,130,246,0.14) !important;
        border-color: rgba(59,130,246,0.45) !important;
        color: #93C5FD !important;
        box-shadow: 0 0 22px rgba(59,130,246,0.2) !important;
    }

    </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("user")

    # ── GREETING + HOME BUTTON ──
    greet_col, home_col = st.columns([8, 1])
    with greet_col:
        name = username if username else "there"
        st.markdown(f"""
        <div class="greeting-block">
            <div class="greeting-name">Hello, {name} 👋</div>
            <div class="greeting-sub">How can I help you?</div>
        </div>
        """, unsafe_allow_html=True)
    with home_col:
        st.markdown("<div class='home-btn-wrap' style='padding-top:32px;'>", unsafe_allow_html=True)
        if st.button("Home"):
            st.session_state.page = "landing"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_chat_file" not in st.session_state:
        st.session_state.current_chat_file = None

    left, right = st.columns([8, 2])

    # ---------- VOICE INPUT ----------
    with right:
        if mic_recorder:
            audio = mic_recorder(
                start_prompt="🎤 Speak",
                stop_prompt="⏹ Stop",
                just_once=True,
                use_container_width=True,
                key="voice_recorder"
            )
        else:
            st.warning("Microphone feature not available.")
            audio = None

        if audio is not None:
            audio_bytes = audio["bytes"]
            temp_audio_path = "temp_audio.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)
            if os.path.exists(temp_audio_path):
                result = model.transcribe(
                    temp_audio_path,
                    fp16=False,
                    language="en"
                )
                text = result["text"].strip()
                if text:
                    st.info(f"🎤 You said: {text}")
                    run_query(text, from_voice=True)
                    auto_speak("Processing your request")
                os.remove(temp_audio_path)

    # ---------- DISPLAY CHAT ----------
    # for msg in st.session_state.messages:
    #     with st.chat_message(msg["role"]):
    #         st.write(msg["content"])
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
            if "data" in msg:
                df = pd.DataFrame(msg["data"])
                if not df.empty:
                    st.dataframe(df)
                    chart = msg.get("chart")
                    x = msg.get("x")
                    y = msg.get("y")
                    if x in df.columns and y in df.columns:
                        if chart == "bar":
                            st.bar_chart(df.set_index(x)[y])
                        elif chart == "line":
                            st.line_chart(df.set_index(x)[y])
                        elif chart == "pie":
                            pie_data = df.set_index(x)[y]
                            fig = pie_data.plot.pie(autopct="%1.1f%%", ylabel="", figsize=(5,5)).figure
                            st.pyplot(fig)
                        elif chart == "hbar":
                            st.write("Horizontal Bar Chart")
                            st.bar_chart(df.set_index(x)[y].sort_values())
                        elif chart == "area":
                            st.area_chart(df.set_index(x)[y])
                        elif chart == "scatter":
                            scatter_df = df[[x, y]]
                            st.scatter_chart(scatter_df)
                else:
                    st.warning("No data returned from this query.")

    # ---------- CHAT INPUT ----------
    prompt = st.chat_input("Ask a question about your data")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        save_message(st.session_state.user, "user", prompt)

        loading_phrases = [
            "Analyzing your data.",
            "Let me check the dataset.",
            "Generating your dashboard."
        ]

        auto_speak(random.choice(loading_phrases))

        with st.spinner("Generating dashboard..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"prompt": prompt},
                    timeout=60
                )
                result = response.json()
                sql   = result.get("sql")
                data  = result.get("data")
                chart = result.get("chart")
                x     = result.get("x")
                y     = result.get("y")
                df    = pd.DataFrame(data)

                if df.empty:
                    message = "I couldn't find data for that query. Please try a different question."
                    st.warning(message)
                    auto_speak(message)
                    st.session_state.messages.append({"role": "assistant", "content": message})
                    save_message(st.session_state.user, "assistant", insights[0])
                    return

            except Exception:
                message = "I couldn't understand that query. Try asking about revenue, region, product, or month."
                st.error(message)
                auto_speak(message)
                return

        with st.chat_message("assistant"):

            # Result header
            st.markdown("""
            <div class="result-header">
                <div class="result-dot"></div>
                <div class="result-title">Dashboard Ready</div>
            </div>
            """, unsafe_allow_html=True)

            # SQL toggle (pure HTML — no Streamlit expander, no keyboard icon)
            st.markdown(f"""
            <details class="sql-toggle">
                <summary>View Generated SQL</summary>
                <pre><code>{sql}</code></pre>
            </details>
            """, unsafe_allow_html=True)

            # Data table
            st.markdown('<div class="section-block-label">Data Table</div>', unsafe_allow_html=True)
            st.dataframe(df)

            if x not in df.columns or y not in df.columns:
                message = "The requested data fields do not exist in this dataset."
                st.error(message)
                auto_speak(message)
                return

            # Chart
            st.markdown('<div class="chart-label">Visualization</div>', unsafe_allow_html=True)
            if x in df.columns and y in df.columns:
                if chart == "bar":
                    st.bar_chart(df.set_index(x)[y])
                elif chart == "line":
                    st.line_chart(df.set_index(x)[y])
                elif chart == "pie":
                    pie_data = df.set_index(x)[y]
                    fig = pie_data.plot.pie(autopct="%1.1f%%", ylabel="", figsize=(5,5)).figure
                    st.pyplot(fig)
                elif chart == "hbar":
                    st.bar_chart(df.set_index(x)[y].sort_values())
                elif chart == "area":
                    st.area_chart(df.set_index(x)[y])
                elif chart == "scatter":
                    scatter_df = df[[x, y]]
                    st.scatter_chart(scatter_df)

            # Insights
            insights = generate_insight(df, x, y)
            st.markdown("""
            <div class="insights-wrap">
                <div class="insights-label">Key Insights</div>
            </div>
            """, unsafe_allow_html=True)
            for insight in insights:
                st.markdown(f'<div class="insight-card">💡 {insight}</div>', unsafe_allow_html=True)

            auto_speak(insights[0])

        st.session_state.messages.append({
            "role": "assistant",
            "content": insights[0],
            "data": data,
            "chart": chart,
            "x": x,
            "y": y
        })

        save_message(st.session_state.user, "user", prompt)