import streamlit as st
import google.generativeai as genai
import time
import random

# ============================================
# REPLACE YOUR GEMINI API KEY HERE
# ============================================
API_KEY = "AIzaSyBzdTF2WCGD7ecSz887e8HfknQQGZ5vbeI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")   

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="CrisisSync - Hotel Emergency Response",
    page_icon="🚨",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main { background-color: #0a0a1a; color: white; }
    .crisis-header {
        background: linear-gradient(135deg, #cc0000, #ff4444);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .alert-box {
        background: #1a1a2e;
        border-left: 5px solid #ff4444;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .safe-box {
        background: #1a2e1a;
        border-left: 5px solid #44ff44;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stat-box {
        background: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="crisis-header">
    <h1>🚨 CrisisSync</h1>
    <p>AI-Powered Hotel Emergency Response System</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - EMERGENCY TRIGGER
# ============================================
st.sidebar.header("🆘 Emergency Panel")
st.sidebar.markdown("---")

emergency_type = st.sidebar.selectbox(
    "Select Emergency Type",
    ["🔥 Fire", "🏥 Medical Emergency", "⚡ Power Failure", 
     "🌊 Flood", "🔫 Security Threat", "💨 Gas Leak"]
)

floor = st.sidebar.selectbox("Floor / Location", 
    ["Lobby", "Floor 1", "Floor 2", "Floor 3", "Rooftop", "Pool Area", "Restaurant"])

severity = st.sidebar.radio("Severity Level", ["🟡 Low", "🟠 Medium", "🔴 Critical"])

guest_name = st.sidebar.text_input("Guest/Staff Name", placeholder="Enter name")

trigger = st.sidebar.button("🚨 TRIGGER EMERGENCY ALERT", use_container_width=True)

# ============================================
# MAIN DASHBOARD
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-box"><h2>12</h2><p>Guests On-Site</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-box"><h2>5</h2><p>Staff Available</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><h2>3</h2><p>Active Alerts</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-box"><h2>2 min</h2><p>Avg Response Time</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# AI RESPONSE SECTION
# ============================================
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Active Alerts")
    
    st.markdown("""
    <div class="alert-box">
        🔴 <b>CRITICAL</b> - Fire reported at Floor 3 Room 302<br>
        <small>⏰ 2 mins ago | Staff: Ravi Kumar dispatched</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert-box">
        🟠 <b>MEDIUM</b> - Medical Emergency at Restaurant<br>
        <small>⏰ 5 mins ago | Ambulance called</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="safe-box">
        🟢 <b>RESOLVED</b> - Power Failure at Lobby<br>
        <small>⏰ 15 mins ago | Issue fixed</small>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("🤖 Gemini AI Response Guide")
    
    if trigger:
        if not guest_name:
            guest_name = "Guest"
        
        with st.spinner("🧠 Gemini AI analyzing emergency..."):
            prompt = f"""
You are an emergency response AI for a hotel.
Emergency: {emergency_type}
Location: {floor}
Severity: {severity}
Person involved: {guest_name}

Provide:
1. Immediate action steps (3 steps)
2. Staff instructions
3. Guest safety message (calm, short)
4. Emergency services to call

Keep response concise and actionable.
"""
            try:
                response = model.generate_content(prompt)
                ai_response = response.text
            except Exception as e:
                ai_response = f"AI Response Error: {str(e)}\nPlease check your API key."
        
        st.markdown(f"""
        <div class="alert-box">
            <b>🚨 EMERGENCY TRIGGERED!</b><br>
            Type: {emergency_type} | Location: {floor} | Severity: {severity}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🤖 Gemini AI Response Plan:**")
        st.write(ai_response)
        
        # Simulate notifications
        st.success("✅ Staff Notified via SMS")
        st.success("✅ Emergency Services Alerted")
        st.success("✅ Guest Safety Message Sent")
        st.info("📍 Staff dispatched to location")
        
    else:
        st.info("👈 Use the Emergency Panel on the left to trigger an alert.\n\nGemini AI will instantly generate a response plan for staff and guests.")

# ============================================
# REAL-TIME STAFF COORDINATION
# ============================================
st.markdown("---")
st.subheader("👥 Staff Coordination Dashboard")

staff_data = {
    "Staff": ["Ravi Kumar", "Priya S", "Ahmed K", "Meena R", "John D"],
    "Role": ["Security", "Medical", "Maintenance", "Front Desk", "Manager"],
    "Status": ["🔴 On Emergency", "🟢 Available", "🟡 On Break", "🟢 Available", "🟢 Available"],
    "Floor": ["Floor 3", "Lobby", "Floor 1", "Reception", "Office"]
}

st.table(staff_data)

# ============================================
# AI CHATBOT FOR GUESTS
# ============================================
st.markdown("---")
st.subheader("💬 Guest Emergency Chatbot (Powered by Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm CrisisSync AI. If you're in an emergency, please describe your situation and I'll guide you to safety immediately. 🚨"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Describe your emergency or ask for help..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("AI thinking..."):
            try:
                chat_prompt = f"""
You are a calm, helpful emergency assistant for hotel guests.
Guest message: {user_input}
Provide immediate, clear safety instructions. Be calm and reassuring.
Keep response under 100 words.
"""
                response = model.generate_content(chat_prompt)
                reply = response.text
            except:
                reply = "Please stay calm. Contact the front desk immediately at extension 0 or press the emergency button in your room."
        
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Footer
st.markdown("---")
st.markdown("<center><small>CrisisSync | Powered by Google Gemini AI | Solution Challenge 2026</small></center>", unsafe_allow_html=True)