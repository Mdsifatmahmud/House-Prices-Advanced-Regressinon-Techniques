import streamlit as st
import util


st.set_page_config(
    page_title="Home Price Prediction",
    page_icon=":house:",
    layout="centered",
)


try:
    util.load_saved_artifacts()
except ModuleNotFoundError as error:
    st.error(
        "Model load kora jacche na. requirements.txt file-e missing package add kore app redeploy korte hobe."
    )
    st.code(f"Missing module: {error.name}")
    st.stop()


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fbf7ef 0%, #f2eadf 100%);
        color: #233129;
    }

    .block-container {
        max-width: 820px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero-card {
        background: #ffffff;
        border: 1px solid #eadfce;
        border-radius: 14px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 18px 45px rgba(85, 64, 38, 0.12);
        border-top: 7px solid #2f6f5e;
    }

    .hero-title {
        color: #233129;
        font-size: 42px;
        line-height: 1.12;
        font-weight: 800;
        text-align: center;
        margin: 0;
    }

    .hero-subtitle {
        color: #756a5d;
        font-size: 16px;
        line-height: 1.7;
        text-align: center;
        margin: 12px auto 0;
        max-width: 620px;
    }

    .input-card {
        background: #fffdf8;
        border: 1px solid #eadfce;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 12px 32px rgba(85, 64, 38, 0.08);
    }

    .section-title {
        color: #233129;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #756a5d;
        font-size: 14px;
        margin-bottom: 18px;
    }

    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        color: #31443a;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        background: #2f6f5e;
        color: white;
        min-height: 48px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 800;
        border: none;
        box-shadow: 0 10px 22px rgba(47, 111, 94, 0.24);
    }

    .stButton > button:hover {
        background: #25594b;
        color: white;
    }

    .result-box {
        padding: 24px;
        border-radius: 14px;
        background: linear-gradient(135deg, #2f6f5e 0%, #25594b 100%);
        color: #ffffff;
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        box-shadow: 0 16px 34px rgba(47, 111, 94, 0.25);
        margin-top: 22px;
    }

    .result-location {
        color: #e8f5ef;
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
    }

    footer,
    #MainMenu {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero-card">
        <h1 class="hero-title">Bangalore Home Price Prediction</h1>
        <p class="hero-subtitle">
            Select property details below and estimate the expected home price in lakh.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Property Details</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Area, BHK, bath and location select kore estimate koro.</div>',
    unsafe_allow_html=True,
)

sqft = st.number_input(
    "Area (Square Feet)",
    min_value=100,
    max_value=10000,
    value=1000,
    step=50,
)

col1, col2 = st.columns(2)
with col1:
    bhk = st.selectbox("BHK", [1, 2, 3, 4, 5])
with col2:
    bath = st.selectbox("Bath", [1, 2, 3, 4, 5])

location_names = util.get_location_names()
if location_names is None:
    st.error("Location data load hoy nai. App restart kore abar try koro.")
    st.stop()

locations = sorted(list(location_names))

location = st.selectbox(
    "Location",
    options=locations,
    index=0,
    key="location_select",
)

estimate_clicked = st.button("Estimate Price")
st.markdown("</div>", unsafe_allow_html=True)


if estimate_clicked:
    estimated_price = util.get_estimated_price(
        location,
        sqft,
        bath,
        bhk,
    )

    st.markdown(
        f"""
        <div class="result-box">
            Estimated Price: Rs. {estimated_price} Lakh
            <div class="result-location">{location.title()} | {sqft:,} sqft | {bhk} BHK | {bath} bath</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
