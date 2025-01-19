import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")

# Constants for LangFlow API
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "df620f54-5c1a-42a9-8fa4-e7b3d95f46cf"
ENDPOINT = "astrology"

# Function to fetch data from the AI component
def run_flow(message: str, endpoint: str = ENDPOINT, application_token: str = APPLICATION_TOKEN) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {"input_value": message, "output_type": "chat", "input_type": "chat"}
    headers = {"Authorization": f"Bearer {application_token}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Function to create the 12 Houses Birth Chart
def create_birth_chart(data):
    houses = ["Self", "Wealth", "Communication", "Home and Family", "Creativity", "Health",
              "Partnerships", "Transformation", "Philosophy", "Career", "Friendships", "Spirituality"]
    values = [data.get(house, 0) for house in houses]
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=houses,
        fill='toself',
        line_color='#FFD700',
        marker=dict(size=8),
    ))
    fig.update_layout(
        title="12 Houses Birth Chart",
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        margin=dict(t=50, b=0, l=0, r=0),
        title_font=dict(size=22, color="#FFD700"),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="#FFFFFF"),
    )
    return fig

# Main App Function
def main():
    st.set_page_config(page_title="SoulBuddy Dashboard", page_icon="🔮", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
    body {
        background: url('https://cdn.pixabay.com/photo/2017/10/06/15/33/star-2823526_1280.jpg') no-repeat center center fixed;
        background-size: cover;
        color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
    }

    .tab-header {
        text-align: center;
        margin-bottom: 20px;
    }

    .section {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .section:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    .section h3 {
        color: #FFD700;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
    }

    .section p, ul {
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .highlight {
        font-weight: bold;
        color: #FFD700;
    }

    .stButton button {
        background-color: #FFD700;
        color: black;
        font-size: 1.1rem;
        padding: 12px 24px;
        border-radius: 30px;
        transition: transform 0.2s ease, box-shadow 0.2s ease; /* Reduced transition time */
        box-shadow: 0px 6px 15px rgba(255, 215, 0, 0.6);
    }

    .stButton button:hover {
        transform: scale(1.05); /* Reduced scale */
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 1);
    }

    .tab-container {
        margin-top: 20px;
    }

    .tab-label {
        font-size: 1.3rem;
        color: #FFD700;
    }

    </style>
    """, unsafe_allow_html=True)

    # Session state to handle page navigation
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    # Landing Page
    if st.session_state.page == "landing":
        st.markdown("""
        <div class="landing">
            <h1>Welcome to SoulBuddy 🔮</h1>
            <p>Your AI-powered spiritual guide for personalized insights, horoscopes, and wellness recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Get Started", key="get_started"):
            st.session_state.page = "form"

    # Input Section for User Details
    elif st.session_state.page == "form":
        st.markdown("<div class='section'><h3>Enter Your Details</h3></div>", unsafe_allow_html=True)
        with st.form(key="user_details_form"):
            name = st.text_input("Name:")
            dob = st.date_input("Date of Birth:", min_value=datetime(1900, 1, 1), max_value=datetime.today())
            time_of_birth = st.time_input("Time of Birth:")
            gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
            state = st.text_input("State:")
            city = st.text_input("City:")
            submit_button = st.form_submit_button("✨ Get Spiritual Insights")

        if submit_button:
            if all([name, dob, time_of_birth, gender, state, city]):
                with st.spinner("Generating your spiritual insights..."):
                    message = f"""
                    Name: {name}
                    DOB: {dob}
                    Time of Birth: {time_of_birth}
                    Gender: {gender}
                    State: {state}
                    City: {city}
                    """
                    response = run_flow(message)
                    if "error" in response:
                        st.error(f"Error: {response['message']}")
                    else:
                        outputs = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "")
                        if outputs:
                            sections = outputs.split("####")
                            birth_chart_data = {"Self": 8, "Wealth": 7, "Communication": 6, "Career": 10}
                            insights = sections[1] if len(sections) > 1 else "No insights available."
                            horoscope = sections[2] if len(sections) > 2 else "No horoscope available."
                            recommendations = sections[3] if len(sections) > 3 else "No recommendations available."
                            spiritual_content = sections[4] if len(sections) > 4 else "No spiritual content available."

                            tabs = st.tabs([
                                "Astrology Dashboard: Birth Chart & Insights", 
                                "Horoscope Forecasts", 
                                "Personalized Spiritual Recommendations", 
                                "Spiritual Wellness Guide", 
                                "Spiritual Advisor Recommendations"
                            ])
                            with tabs[0]:
                                st.markdown(f"<div class='section'><h3>Birth Chart & Personalized Insights</h3></div>", unsafe_allow_html=True)
                                st.plotly_chart(create_birth_chart(birth_chart_data), use_container_width=True)
                                st.markdown(f"<div class='section'><p>{insights}</p></div>", unsafe_allow_html=True)
                            with tabs[1]:
                                st.markdown(f"<div class='section'><h3>Horoscope Forecasts</h3><p>{horoscope}</p></div>", unsafe_allow_html=True)
                            with tabs[2]:
                                st.markdown(f"<div class='section'><h3>Personalized Spiritual Recommendations</h3><ul><li>{recommendations}</li></ul></div>", unsafe_allow_html=True)
                            with tabs[3]:
                                st.markdown(f"<div class='section'><h3>Spiritual Wellness Guide</h3><p>{spiritual_content}</p></div>", unsafe_allow_html=True)
                            with tabs[4]:
                                st.markdown("<div class='section'><h3>Spiritual Advisor Recommendations</h3></div>", unsafe_allow_html=True)
                                st.markdown("<div class='section'>", unsafe_allow_html=True)

                                if horoscope:
                                    st.markdown(f"<p><b>Horoscope:</b> {horoscope}</p>", unsafe_allow_html=True)
                                else:
                                    st.warning("Horoscope data is not available.")

                                if recommendations:
                                    st.markdown(f"<p><b>Personalized Recommendations:</b> {recommendations}</p>", unsafe_allow_html=True)
                                else:
                                    st.warning("Recommendations data is not available.")

                                if spiritual_content:
                                    st.markdown(f"<p><b>Spiritual Content:</b> {spiritual_content}</p>", unsafe_allow_html=True)
                                else:
                                    st.warning("Spiritual content is not available.")

                                st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.warning("No insights available from the API.")
            else:
                st.warning("Please fill out all fields.")

if __name__ == "__main__":
    main()
