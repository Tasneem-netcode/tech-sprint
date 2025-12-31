import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
# Your API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCLFgiiZbCgoyXYlr88CrJ8RjysoYaUZ8k" 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- THE MASTER PROMPT ---
SYSTEM_PROMPT = """
You are 'EcoSphere AI', an advanced environmental intelligence engine designed for a hackathon project. 
Your goal is to interpret raw user data and convert it into actionable, simple advice.

There are two modes you must handle:
1. INDIVIDUAL MODE (EcoTrack):
   - Input: Transport habits, Food choices, Electricity usage.
   - Output: Estimate a relative Carbon Footprint (Low/Medium/High), explain the main contributor, and give 1 specific, realistic lifestyle change.

2. INDUSTRY MODE (EcoGuard):
   - Input: Industry Type, Fuel Source, Waste Type.
   - Output: Assess Emission Risk (Low/Medium/High), explain the root cause of pollution based on the fuel/waste, and suggest 1 technical mitigation step (e.g., "Install wet scrubbers", "Switch to biofuels").

Tone: Professional, insightful, and encouraging. Keep answers short and demo-friendly (under 100 words).
"""

# --- APP LAYOUT ---
st.set_page_config(page_title="EcoSphere AI", page_icon="🌱", layout="wide")

# Header Section (UPDATED FOR TECH SPRINT)
st.title("🌱 EcoSphere AI: Unified Environmental Intelligence")
st.markdown("**Team TECOS | Tech Sprint Hackathon 2025**") 
st.markdown("---")

# Sidebar for Navigation
mode = st.sidebar.radio("Select User Mode:", ["Individual (EcoTrack)", "Industry (EcoGuard)"])

# ==========================================
# MODE 1: INDIVIDUAL (EcoTrack)
# ==========================================
if mode == "Individual (EcoTrack)":
    st.header("👤 Individual Carbon Footprint Tracker")
    st.caption("Helping urban citizens and students understand their impact.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Enter Your Habits")
        transport = st.selectbox("Primary Transport", ["Bicycle/Walk", "Public Bus/Metro", "Motorbike", "Car (Petrol/Diesel)"])
        food = st.selectbox("Dietary Habit", ["Vegetarian", "Mixed", "Heavy Meat Eater"])
        electricity = st.slider("Daily Electricity Usage (Hours of AC/Heater)", 0, 24, 4)

    with col2:
        st.subheader("2. AI Impact Analysis")
        if st.button("Calculate Impact"):
            # Simple Math Logic
            score = 0
            if transport == "Car (Petrol/Diesel)": score += 50
            elif transport == "Motorbike": score += 30
            else: score += 5
            
            if food == "Heavy Meat Eater": score += 40
            elif food == "Mixed": score += 20
            
            score += electricity * 2

            # Display Score
            if score > 80:
                st.metric(label="Estimated Footprint", value="HIGH", delta="-Needs Action", delta_color="inverse")
            elif score > 40:
                st.metric(label="Estimated Footprint", value="MEDIUM", delta="Ok", delta_color="off")
            else:
                st.metric(label="Estimated Footprint", value="LOW", delta="+Great Job!")

            # Gemini Analysis
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            user_input = f"Mode: INDIVIDUAL. Transport: {transport}, Food: {food}, Electricity: {electricity} hours. Calculated Score: {score}."
            
            with st.spinner("EcoSphere AI is analyzing your lifestyle..."):
                try:
                    response = model.generate_content(SYSTEM_PROMPT + user_input)
                    st.success("💡 AI Recommendation:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")

# ==========================================
# MODE 2: INDUSTRY (EcoGuard)
# ==========================================
elif mode == "Industry (EcoGuard)":
    st.header("🏭 Industry Emission Monitor (EcoGuard)")
    st.caption("Helping small/mid-scale industries monitor risk without expensive sensors.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Facility Data Inputs")
        # Pre-filling Coal (Index 3) for faster demo
        ind_type = st.selectbox("Industry Type", ["Textile Unit", "Food Processing", "Chemical Plant", "Cement Factory"])
        fuel = st.selectbox("Primary Fuel Used", ["Solar/Electric", "Natural Gas", "Diesel", "Coal"], index=3) 
        waste = st.radio("Primary Waste Type", ["Solid (Packaging)", "Liquid (Chemical Effluents)", "Gaseous (Smoke/Exhaust)"])

    with col2:
        st.subheader("2. Risk & Compliance")
        if st.button("Analyze Risk"):
            # Risk Logic
            risk_level = "Low"
            if fuel == "Coal" or waste == "Gaseous (Smoke/Exhaust)":
                risk_level = "High"
            elif fuel == "Diesel" or waste == "Liquid (Chemical Effluents)":
                risk_level = "Medium"
            
            # Dashboard Metrics
            st.metric(label="Emission Risk Level", value=risk_level, delta="Regulatory Check Required" if risk_level=="High" else "Safe")

            # Gemini Technical Advice
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            user_input = f"Mode: INDUSTRY. Industry: {ind_type}, Fuel: {fuel}, Waste: {waste}. Calculated Risk: {risk_level}."
            
            with st.spinner("EcoGuard is analyzing compliance protocols..."):
                try:
                    response = model.generate_content(SYSTEM_PROMPT + user_input)
                    st.info("🛠️ Mitigation Strategy:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")

st.markdown("---")
st.caption("Powered by Google Gemini | Built for Tech Sprint Hackathon 2025")