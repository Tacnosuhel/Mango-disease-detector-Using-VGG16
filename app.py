import streamlit as st
from PIL import Image
from src.predict import predict_disease

st.set_page_config(
    page_title="Mango Disease Detector",
    page_icon="🥭",
    layout="wide"
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --leaf: #14532d;
        --leaf-deep: #0b3a1f;
        --mango: #f5a524;
        --mango-soft: #fff1d0;
        --paper: #f4f8f0;
        --ink: #17261c;
        --muted: #5d7064;
        --line: #d9e5d3;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--paper); }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem; }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        background: var(--leaf);
        border-radius: 28px;
        padding: 3rem 3rem 2.8rem;
        margin-bottom: 2rem;
        color: #f4f8f0;
    }
    .hero::after {
        content: "";
        position: absolute;
        right: -70px; top: -90px;
        width: 320px; height: 320px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ffd27a, var(--mango) 60%, #e48a0c);
    }
    .hero::before {
        content: "🥭";
        position: absolute;
        right: 70px; top: 55px;
        font-size: 108px;
        z-index: 2;
        transform: rotate(-12deg);
    }
    .hero h1 {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 800;
        font-size: clamp(2.2rem, 5vw, 3.6rem);
        line-height: 1.02;
        letter-spacing: -0.03em;
        margin: 0 0 .9rem 0;
        padding: 0;
        color: #f4f8f0;
        max-width: 560px;
    }
    .hero p {
        font-size: 1.08rem;
        color: #cfe3d3;
        max-width: 460px;
        margin: 0;
        line-height: 1.55;
    }

    /* Panels */
    .panel-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 700;
        font-size: 1.35rem;
        letter-spacing: -0.01em;
        margin-bottom: .6rem;
    }

    /* Uploader */
    [data-testid="stFileUploader"] section {
        background: #ffffff;
        border: 2px dashed #9dbf9f;
        border-radius: 20px;
        padding: 1.6rem;
        transition: border-color .2s, background .2s;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: var(--mango);
        background: #fffaf0;
    }
    [data-testid="stFileUploader"] button {
        border-radius: 999px;
        border: 1.5px solid var(--leaf);
        color: var(--leaf);
        font-weight: 700;
    }

    /* Image */
    [data-testid="stImage"] img {
        border-radius: 20px;
        border: 6px solid #ffffff;
        box-shadow: 0 10px 30px rgba(20, 83, 45, .15);
    }
    [data-testid="stImage"] figcaption { color: var(--muted); }

    /* Button */
    .stButton > button {
        width: 100%;
        background: var(--mango);
        color: #2b1a00;
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 16px;
        padding: .85rem 1rem;
        box-shadow: 0 6px 0 #c98410;
        transition: transform .1s, box-shadow .1s;
    }
    .stButton > button:hover {
        background: #ffb83a;
        color: #2b1a00;
        border: none;
    }
    .stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0 #c98410;
    }
    .stButton > button:focus-visible { outline: 3px solid var(--leaf); outline-offset: 3px; }

    /* Result */
    .result-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 14px 40px rgba(20, 83, 45, .10);
    }
    .pill {
        display: inline-block;
        background: var(--mango-soft);
        color: #7a4b00;
        font-weight: 700;
        font-size: .85rem;
        padding: .3rem .8rem;
        border-radius: 999px;
        margin-bottom: 1rem;
    }
    .disease {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 800;
        font-size: clamp(2rem, 4vw, 2.9rem);
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: var(--leaf-deep);
        margin-bottom: 1.6rem;
        word-break: break-word;
    }
    .conf-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: .5rem;
        color: var(--muted);
        font-weight: 500;
    }
    .conf-value {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 800;
        font-size: 1.9rem;
        color: var(--ink);
    }
    .bar {
        height: 14px;
        background: #e7efe2;
        border-radius: 999px;
        overflow: hidden;
    }
    .bar > span {
        display: block;
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--leaf), var(--mango));
        animation: fill 1s ease-out;
    }
    @keyframes fill { from { width: 0; } }

    /* Empty state */
    .empty {
        border: 2px dashed var(--line);
        border-radius: 24px;
        padding: 3rem 1.5rem;
        text-align: center;
        color: var(--muted);
    }
    .empty .big { font-size: 2.6rem; }

    @media (prefers-reduced-motion: reduce) {
        .bar > span { animation: none; }
    }
    @media (max-width: 700px) {
        .hero { padding: 2rem 1.5rem; }
        .hero::after, .hero::before { opacity: .25; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero ----------
st.markdown(
    """
    <div class="hero">
        <h1>Mango Disease Detector</h1>
        <p>Upload a mango leaf image to detect its disease.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Main layout ----------
left, right = st.columns(2, gap="large")
result = None

with left:
    st.markdown('<div class="panel-title">Your leaf</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a mango leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Mango Leaf",
                 use_container_width=True)

        if st.button("Detect Disease"):

            with st.spinner("Analyzing image..."):

                result = predict_disease(image)

with right:
    st.markdown('<div class="panel-title">Result</div>', unsafe_allow_html=True)

    if result is not None:
        conf = max(0.0, min(100.0, float(result["confidence"])))

        st.toast("Prediction Completed!", icon="✅")

        st.markdown(
            f"""
            <div class="result-card">
                <span class="pill">Prediction Completed</span>
                <div class="disease">{result["disease"]}</div>
                <div class="conf-row">
                    <span>Confidence</span>
                    <span class="conf-value">{conf:.2f}%</span>
                </div>
                <div class="bar"><span style="width:{conf}%"></span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="empty">
                <div class="big">🍃</div>
                <p>Upload a leaf image and press <b>Detect Disease</b> to see the result here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )