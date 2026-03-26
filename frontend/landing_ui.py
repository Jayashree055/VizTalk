
import streamlit as st
import streamlit.components.v1 as components


def render_landing():

    st.markdown("""
    <style>
    

    /* ── RESET & BASE ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    [data-testid="stAppViewContainer"] {
        background: #080C14 !important;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }
    [data-testid="stAppViewBlockContainer"] {
        background: transparent !important;
        padding-top: 0 !important;
        max-width: 1100px;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    # [data-testid="stToolbar"] { display: none !important; }

    /* Noise grain overlay */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.6;
    }

    /* ── GLOW BLOBS ── */
    .bg-blobs {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .blob {
        position: absolute;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.18;
        animation: blobDrift 20s ease-in-out infinite alternate;
    }
    .blob-1 { width: 600px; height: 600px; background: #3B82F6; top: -200px; left: -150px; animation-delay: 0s; }
    .blob-2 { width: 500px; height: 500px; background: #8B5CF6; top: 20%; right: -200px; animation-delay: -7s; }
    .blob-3 { width: 400px; height: 400px; background: #06B6D4; bottom: 10%; left: 30%; animation-delay: -14s; }

    @keyframes blobDrift {
        0%   { transform: translate(0, 0) scale(1); }
        100% { transform: translate(40px, 30px) scale(1.08); }
    }

    /* ── NAV ── */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0;
        position: relative;
        z-index: 10;
    }
    .nav-logo {
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .nav-btn {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #E2E8F0 !important;
        padding: 8px 20px;
        border-radius: 8px;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        backdrop-filter: blur(8px);
    }
    .nav-btn:hover {
        background: rgba(255,255,255,0.12);
        border-color: rgba(255,255,255,0.22);
        transform: translateY(-1px);
    }

    /* ── HERO ── */
    .hero-section {
        text-align: center;
        padding: 20px 0 60px;
        position: relative;
        z-index: 5;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(59,130,246,0.12);
        border: 1px solid rgba(59,130,246,0.3);
        color: #93C5FD;
        font-size: 13px;
        font-weight: 500;
        padding: 6px 16px;
        border-radius: 100px;
        margin-bottom: 32px;
        letter-spacing: 0.3px;
    }
    .badge-dot {
        width: 6px;
        height: 6px;
        background: #3B82F6;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: 0.5; transform: scale(0.85); }
    }
    .hero-title {
        font-family: Segoe UI, Arial, sans-serif;
        font-size: clamp(42px, 7vw, 72px);
        font-weight: 800;
        line-height: 1.08;
        letter-spacing: -2px;
        color: #F8FAFC;
        margin-bottom: 24px;
    }
    .hero-title .accent {
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .hero-subtitle {
        font-size: 20px;
        font-weight: 400;
        color: #CBD5E1;
        max-width: 520px;
        margin: 0 auto 48px;
        line-height: 1.7;
        letter-spacing: 0.1px;
    }
    .hero-cta-row {
        display: flex;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .cta-primary {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        color: white !important;
        border: none;
        padding: 14px 32px;
        border-radius: 10px;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        letter-spacing: 0.2px;
        box-shadow: 0 0 40px rgba(59,130,246,0.3);
        transition: all 0.25s ease;
        display: inline-block;
    }
    .cta-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 60px rgba(59,130,246,0.45);
    }

    /* ── SCROLLING TICKER ── */
    .ticker-wrap {
        overflow: hidden;
        white-space: nowrap;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 14px 0;
        margin: 40px 0;
        position: relative;
        z-index: 5;
    }
    .ticker-track {
        display: inline-flex;
        gap: 48px;
        animation: ticker 22s linear infinite;
    }
    .ticker-item {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .ticker-item::before {
        content: '';
        width: 4px;
        height: 4px;
        background: #60A5FA;
        border-radius: 50%;
        display: inline-block;
    }
    @keyframes ticker {
        0%   { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* ── SECTION LABEL ── */
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #3B82F6;
        margin-bottom: 12px;
    }
    .section-title {
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #F1F5F9;
        letter-spacing: -0.8px;
        margin-bottom: 8px;
    }
    .section-sub {
        font-size: 16px;
        color: #94A3B8;
        font-weight: 400;
    }

    /* ── FEATURE CARDS ── */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-top: 32px;
        position: relative;
        z-index: 5;
    }
    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(59,130,246,0.06), transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .feature-card:hover::before { opacity: 1; }
    .feature-card:hover {
        border-color: rgba(59,130,246,0.25);
        transform: translateY(-3px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .feature-icon {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-bottom: 16px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .feature-name {
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #E2E8F0;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 15px;
        color: #94A3B8;
        line-height: 1.65;
        font-weight: 400;
    }

    /* ── PIPELINE ── */
    .pipeline-section {
        position: relative;
        z-index: 5;
        margin: 60px 0;
    }
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 32px;
    }
    .pipeline-step {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        transition: border-color 0.3s;
    }
    .pipeline-step:hover { border-color: rgba(59,130,246,0.2); }
    .step-num {
        width: 28px;
        height: 28px;
        min-width: 28px;
        background: rgba(59,130,246,0.15);
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        color: #60A5FA;
        font-family: Segoe UI, Arial, sans-serif;
    }
    .step-text {
        font-size: 14px;
        font-weight: 400;
        color: #CBD5E1;
        line-height: 1.4;
    }

    /* ── QUERY EXAMPLES ── */
    .queries-section {
        position: relative;
        z-index: 5;
        margin: 60px 0;
    }
    .query-scroll {
        overflow: hidden;
        margin-top: 28px;
    }
    .query-track {
        display: inline-flex;
        gap: 12px;
        animation: queryScroll 20s linear infinite;
    }
    @keyframes queryScroll {
        0%   { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .query-pill {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: #CBD5E1;
        padding: 10px 18px;
        border-radius: 100px;
        font-size: 14px;
        white-space: nowrap;
        font-weight: 400;
        transition: all 0.2s;
    }
    .query-pill:hover {
        background: rgba(59,130,246,0.1);
        border-color: rgba(59,130,246,0.3);
        color: #93C5FD;
    }

    /* ── CTA BANNER ── */
    .cta-banner {
        background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 56px 40px;
        text-align: center;
        position: relative;
        z-index: 5;
        margin: 40px 0 60px;
        overflow: hidden;
    }
    .cta-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.12), transparent 70%);
        pointer-events: none;
    }
    .cta-banner-title {
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        margin-bottom: 12px;
    }
    .cta-banner-sub {
        font-size: 17px;
        color: #94A3B8;
        font-weight: 400;
        margin-bottom: 32px;
    }

    /* ── DIVIDER ── */
    .elegant-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 48px 0;
    }

    /* ── STREAMLIT BUTTON OVERRIDE ── */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 0 30px rgba(59,130,246,0.25) !important;
        transition: all 0.25s ease !important;
        width: auto !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 50px rgba(59,130,246,0.4) !important;
    }

    /* hide default streamlit chrome */
    #MainMenu, footer { visibility: hidden; }

    /* Hide Streamlit element toolbar (copy icon, fullscreen, etc.) everywhere */
    # [data-testid="stElementToolbar"],
    [data-testid="stElementToolbarButton"],
    [data-testid="StyledFullScreenButton"],
    button[title="Copy to clipboard"],
    button[aria-label="Copy to clipboard"],
    button[title="View fullscreen"],
    button[aria-label="View fullscreen"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    </style>

    <!-- Background blobs -->
    <div class="bg-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── NAV BAR ──
    nav_col, _, btn_col = st.columns([6, 3, 1])
    with nav_col:
        st.markdown('<div class="nav-bar"><span class="nav-logo">⬡ VizTalk</span></div>', unsafe_allow_html=True)
    with btn_col:
        st.markdown("<div style='padding-top:18px'>", unsafe_allow_html=True)
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">
            <span class="badge-dot"></span>
            Powered by LLM · SQL · Real-time Charts
        </div>
        <h1 class="hero-title">
            Ask your data.<br>
            <span class="accent">Anything.</span>
        </h1>
        <p class="hero-subtitle" style="text-align:center; margin-left:auto; margin-right:auto;">
            Turn plain English into interactive dashboards instantly — no SQL, no BI tools, no waiting.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA button via Streamlit
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Get Started"):
            st.session_state.page = "chat"
            st.rerun()

    # ── TICKER ──
    st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker-track">
            <span class="ticker-item">Natural Language Queries</span>
            <span class="ticker-item">Auto Chart Selection</span>
            <span class="ticker-item">Voice Input</span>
            <span class="ticker-item">CSV Upload</span>
            <span class="ticker-item">SQL Generation</span>
            <span class="ticker-item">Real-time Dashboards</span>
            <span class="ticker-item">Chat History</span>
            <span class="ticker-item">Key Insights</span>
            <span class="ticker-item">Natural Language Queries</span>
            <span class="ticker-item">Auto Chart Selection</span>
            <span class="ticker-item">Voice Input</span>
            <span class="ticker-item">CSV Upload</span>
            <span class="ticker-item">SQL Generation</span>
            <span class="ticker-item">Real-time Dashboards</span>
            <span class="ticker-item">Chat History</span>
            <span class="ticker-item">Key Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURES ──
    st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="position:relative; z-index:5;">
        <div class="section-label">Features</div>
        <div class="section-title">Everything you need to explore data</div>
        <div class="section-sub">Built for executives who want answers, not queries.</div>
    </div>

    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-name">Natural Language Queries</div>
            <div class="feature-desc">Ask questions in plain English. No SQL knowledge required — just describe what you want to see.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-name">Smart Chart Selection</div>
            <div class="feature-desc">The system automatically picks the best chart type — bar, line, pie, scatter — based on your data.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎤</div>
            <div class="feature-name">Voice Queries</div>
            <div class="feature-desc">Speak your question and get instant results. Hands-free dashboard generation powered by Whisper.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📁</div>
            <div class="feature-name">Upload Your Data</div>
            <div class="feature-desc">Drag and drop any CSV file and start querying it instantly. No configuration needed.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PIPELINE ──
    st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline-section">
        <div class="section-label">How It Works</div>
        <div class="section-title">From question to dashboard in seconds</div>
        <div class="pipeline-grid">
            <div class="pipeline-step">
                <div class="step-num">1</div>
                <div class="step-text">Login & upload your dataset or use the default</div>
            </div>
            <div class="pipeline-step">
                <div class="step-num">2</div>
                <div class="step-text">Type or speak your business question</div>
            </div>
            <div class="pipeline-step">
                <div class="step-num">3</div>
                <div class="step-text">LLM generates the SQL query automatically</div>
            </div>
            <div class="pipeline-step">
                <div class="step-num">4</div>
                <div class="step-text">Data is fetched and the right chart is selected</div>
            </div>
            <div class="pipeline-step">
                <div class="step-num">5</div>
                <div class="step-text">Interactive dashboard renders with key insights</div>
            </div>
            <div class="pipeline-step">
                <div class="step-num">6</div>
                <div class="step-text">Chat history is saved for follow-up questions</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── EXAMPLE QUERIES ──
    st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="queries-section">
        <div class="section-label">Try Asking</div>
        <div class="section-title">Example prompts to get you started</div>
        <div class="query-scroll">
            <div class="query-track">
                <div class="query-pill">📈 Show monthly revenue trends for Q3</div>
                <div class="query-pill">🗺️ Break down sales by region</div>
                <div class="query-pill">🏆 What are the top 5 performing products?</div>
                <div class="query-pill">📣 Compare marketing channel performance</div>
                <div class="query-pill">💰 Show revenue by campaign type</div>
                <div class="query-pill">📅 Monthly active users this year</div>
                <div class="query-pill">📉 Which region had the lowest growth?</div>
                <div class="query-pill">🔄 Show conversion rate by channel</div>
                <div class="query-pill">📈 Show monthly revenue trends for Q3</div>
                <div class="query-pill">🗺️ Break down sales by region</div>
                <div class="query-pill">🏆 What are the top 5 performing products?</div>
                <div class="query-pill">📣 Compare marketing channel performance</div>
                <div class="query-pill">💰 Show revenue by campaign type</div>
                <div class="query-pill">📅 Monthly active users this year</div>
                <div class="query-pill">📉 Which region had the lowest growth?</div>
                <div class="query-pill">🔄 Show conversion rate by channel</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA BANNER ──
    st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-banner-title">Ready to explore your data?</div>
        <div class="cta-banner-sub">No SQL. No setup. Just ask.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Start Now →"):
            st.session_state.page = "chat"
            st.rerun()