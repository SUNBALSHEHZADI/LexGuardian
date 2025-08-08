# app.py
import streamlit as st
import os
import time
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
import pycountry

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except:
    st.error("Failed to initialize Groq client. Please check your API key.")
    st.stop()

# Set up Streamlit page
st.set_page_config(
    page_title="LexGuardian",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    :root {
        --primary: #2c3e50;
        --secondary: #3498db;
        --accent: #e74c3c;
        --light: #ecf0f1;
        --dark: #2c3e50;
        --success: #27ae60;
        --card-shadow: 0 6px 20px rgba(0,0,0,0.08);
        --transition: all 0.3s ease;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .header {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 0 0 25px 25px;
        box-shadow: var(--card-shadow);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.8rem;
        box-shadow: var(--card-shadow);
        margin-bottom: 1.8rem;
        transition: var(--transition);
        border-left: 4px solid var(--accent);
    }
    
    .scenario-btn {
        width: 100%;
        padding: 1.1rem;
        background: white;
        color: var(--primary);
        border: 2px solid var(--secondary);
        border-radius: 12px;
        font-weight: 600;
        margin: 0.7rem 0;
        cursor: pointer;
        transition: var(--transition);
        text-align: center;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .scenario-btn:hover {
        background: linear-gradient(135deg, var(--secondary) 0%, #2980b9 100%);
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }
    
    .response-card {
        background: white;
        border-left: 5px solid var(--success);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: var(--card-shadow);
        animation: fadeIn 0.8s ease;
    }
    
    .country-card {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 12px;
        width: 100%;
        padding: 1rem;
        border-radius: 12px;
        background: white;
        box-shadow: var(--card-shadow);
        margin-bottom: 12px;
        cursor: pointer;
        transition: var(--transition);
        border: 2px solid #e0e0e0;
        font-weight: 500;
        font-size: 1rem;
        text-align: left;
    }
    
    .country-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border-color: var(--secondary);
    }
    
    .country-card.selected {
        background: linear-gradient(135deg, var(--light) 0%, #d6eaf8 100%);
        border: 2px solid var(--accent);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    
    .country-flag {
        font-size: 1.5rem;
        min-width: 35px;
        text-align: center;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: var(--dark);
        font-size: 0.9rem;
        background: rgba(236, 240, 241, 0.7);
        border-radius: 15px;
        box-shadow: var(--card-shadow);
    }
    
    .section-title {
        font-size: 1.4rem;
        color: var(--primary);
        margin-bottom: 1.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent);
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        margin-bottom: 1.5rem;
        transition: var(--transition);
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        color: var(--accent);
        margin-bottom: 1rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @media (max-width: 768px) {
        .header {
            padding: 1.5rem 1rem;
        }
        
        .card {
            padding: 1.2rem;
        }
        
        .country-card {
            padding: 0.8rem;
            font-size: 0.95rem;
        }
        
        .country-flag {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Country data with flags
COUNTRIES = {
    "🇺🇸 United States": "US",
    "🇬🇧 United Kingdom": "GB",
    "🇨🇦 Canada": "CA",
    "🇦🇺 Australia": "AU",
    "🇮🇳 India": "IN",
    "🇩🇪 Germany": "DE",
    "🇫🇷 France": "FR",
    "🇯🇵 Japan": "JP",
    "🇧🇷 Brazil": "BR",
    "🇿🇦 South Africa": "ZA",
    "🇪🇸 Spain": "ES",
    "🇸🇬 Singapore": "SG"
}

# Common legal scenarios for students
STUDENT_SCENARIOS = [
    "Academic Rights & Responsibilities",
    "Campus Housing Issues",
    "Discrimination & Harassment",
    "Freedom of Speech on Campus",
    "Student Privacy Rights",
    "Disciplinary Proceedings",
    "Financial Aid & Scholarships",
    "Intellectual Property Rights",
    "Internship & Employment Rights",
    "Student Loan Concerns",
    "Campus Safety & Security",
    "Consumer Protection as a Student"
]

# Student legal topics
LEGAL_TOPICS = [
    "Academic Integrity Policies",
    "Title IX & Gender Equity",
    "Disability Accommodations",
    "Student Privacy (FERPA)",
    "Campus Free Speech",
    "Student Organization Rights",
    "Financial Aid Regulations",
    "Plagiarism & Copyright",
    "Tenant Rights for Students",
    "Student Employment Laws",
    "Campus Police Interactions",
    "Student Loan Borrower Rights"
]

# LLM models available on Groq
MODELS = {
    "Llama3-70b (Highest Accuracy)": "llama3-70b-8192",
    "Llama3-8b (Fast Response)": "llama3-8b-8192",
    "Mixtral-8x7b (Balanced)": "mixtral-8x7b-32768"
}

# Function to get country name from code
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

# Function to get rights information from Groq API
def get_legal_rights(country, scenario, model_name):
    """Get legal rights information using Groq API"""
    country_name = get_country_name(country)
    
    system_prompt = f"""
    You are an expert legal assistant specializing in student rights in {country_name}. 
    Provide clear, accurate information about student rights in the given scenario.
    
    Guidelines:
    - Focus specifically on student rights and responsibilities
    - List 5-7 key points as bullet points
    - Use plain language understandable to students
    - Include relevant legal references when appropriate
    - Highlight practical steps students can take
    - Mention any country-specific variations
    - Keep response under 300 words
    - Format with emojis for readability
    - End with important disclaimers
    """
    
    user_prompt = f"""
    Scenario: {scenario}
    Country: {country_name}
    
    Please provide student-specific rights information for this situation in {country_name}.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model_name,
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Function to display response with animation
def display_response(response):
    """Display the response with typing animation effect"""
    message_placeholder = st.empty()
    full_response = ""
    
    # Simulate stream of response with milliseconds delay
    for chunk in response.split():
        full_response += chunk + " "
        time.sleep(0.03)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(f'<div class="response-card">{full_response}▌</div>', unsafe_allow_html=True)
    
    # Display final message without the cursor
    message_placeholder.markdown(f'<div class="response-card">{response}</div>', unsafe_allow_html=True)

# Main app
def main():
    # Header section
    st.markdown("""
    <div class="header">
        <h1 style="margin:0;font-size:2.5rem;">LexGuardian</h1>
        <p style="margin:0;font-size:1.2rem;opacity:0.9;margin-top:10px;">Empowering Students with Legal Knowledge</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = "🇺🇸 United States"
    
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = None
        
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "explorer"
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["Rights Explorer", "Legal Topics", "Student Resources"])
    
    with tab1:
        st.markdown("### ⚖️ Know Your Rights")
        st.markdown("Select your country and a situation to understand your legal rights as a student")
        
        # Model selection
        model_col = st.columns([1,1,2])
        with model_col[0]:
            selected_model = st.selectbox("Choose AI Model", list(MODELS.keys()), index=0)
        with model_col[1]:
            st.markdown(f"**Selected Country:** {st.session_state.selected_country}")
        
        # Main content columns
        col1, col2 = st.columns([1, 1.3], gap="large")
        
        with col1:
            st.markdown("#### 🌍 Select Your Country")
            
            # Country selection cards
            for country_display in COUNTRIES.keys():
                is_selected = st.session_state.selected_country == country_display
                card_class = "country-card selected" if is_selected else "country-card"
                flag, name = country_display.split(" ", 1)
                
                if st.button(
                    f'{flag} {name}',
                    key=f"btn_{country_display}",
                    use_container_width=True
                ):
                    st.session_state.selected_country = country_display
                    st.session_state.selected_scenario = None
                    st.rerun()
            
            st.markdown("#### 📊 Student Rights Awareness")
            countries = list(COUNTRIES.values())
            awareness = [85, 82, 80, 78, 75, 83, 81, 79, 76, 74, 80, 77]  # Simulated data
            
            fig = px.pie(
                names=[get_country_name(code) for code in countries],
                values=awareness,
                title="Global Student Rights Awareness",
                height=300
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=0),
                showlegend=False
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("#### 🎓 Student Scenarios")
            st.markdown("Select a situation relevant to student life")
            
            # Create buttons for each scenario in 2 columns
            scenario_cols = st.columns(2)
            for i, scenario in enumerate(STUDENT_SCENARIOS):
                with scenario_cols[i % 2]:
                    if st.button(
                        f"{scenario}",
                        key=f"scen_{scenario}",
                        use_container_width=True,
                        help=f"Click to see student rights for {scenario}"
                    ):
                        st.session_state.selected_scenario = scenario
            
            # Custom scenario input
            custom_scenario = st.text_input(
                "**Describe your specific concern:**",
                placeholder="e.g., 'Rights during campus protest', 'Academic appeal process'"
            )
            if custom_scenario:
                st.session_state.selected_scenario = custom_scenario
            
            # Response area
            if st.session_state.selected_scenario:
                country_code = COUNTRIES[st.session_state.selected_country]
                
                with st.spinner(f"🔍 Analyzing student rights for '{st.session_state.selected_scenario}'..."):
                    response = get_legal_rights(
                        country_code, 
                        st.session_state.selected_scenario,
                        MODELS[selected_model]
                    )
                    
                    if response:
                        display_response(response)
                    else:
                        st.error("Failed to get response. Please try again.")
            else:
                st.info("👆 Select a student scenario to see your rights information")
                st.markdown("""
                <div style="text-align:center; margin:20px 0;">
                    <img src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=600&h=400" 
                         style="width:100%; border-radius:15px; box-shadow:0 6px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top:10px;font-style:italic;color:#666;">Knowledge is your best legal defense</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📚 Essential Legal Topics for Students")
        st.markdown("Explore key legal concepts every student should understand")
        
        # Topics in 3 columns
        cols = st.columns(3)
        for i, topic in enumerate(LEGAL_TOPICS):
            with cols[i % 3]:
                with st.expander(f"**{topic}**", expanded=True):
                    st.info(f"Learn about your rights and responsibilities regarding {topic.lower()}")
                    if st.button("Explore Topic", key=f"topic_{topic}"):
                        st.session_state.active_tab = "explorer"
                        st.session_state.selected_scenario = topic
                        st.rerun()
        
        st.markdown("### 🧠 Legal Knowledge Quiz")
        st.markdown("Test your understanding of student rights")
        
        quiz_cols = st.columns(2)
        with quiz_cols[0]:
            st.markdown("""
            **Question 1:** Can your college share your academic records without permission?  
            A) Always  
            B) Only with parents  
            C) Only with your consent  
            D) Only in emergencies  
            """)
            
            answer1 = st.radio("Select answer:", ["A", "B", "C", "D"], key="q1", index=None)
            if answer1 == "C":
                st.success("Correct! FERPA requires your consent for most record disclosures.")
            elif answer1:
                st.error("Incorrect. The correct answer is C - Only with your consent.")
        
        with quiz_cols[1]:
            st.markdown("""
            **Question 2:** What should you do if you face discrimination on campus?  
            A) Ignore it  
            B) Report to Title IX coordinator  
            C) Post about it on social media  
            D) Confront the person directly  
            """)
            
            answer2 = st.radio("Select answer:", ["A", "B", "C", "D"], key="q2", index=None)
            if answer2 == "B":
                st.success("Correct! Reporting to the Title IX coordinator is the proper step.")
            elif answer2:
                st.error("Incorrect. The correct answer is B - Report to Title IX coordinator.")
    
    with tab3:
        st.markdown("### 🛡️ Student Legal Resources")
        st.markdown("Essential tools and information for student legal matters")
        
        # Resources in cards
        resource_cols = st.columns(3)
        resources = [
            {"icon": "📝", "title": "Legal Templates", "desc": "Downloadable templates for common student legal documents"},
            {"icon": "📚", "title": "Legal Glossary", "desc": "Understand legal terminology with our student-friendly dictionary"},
            {"icon": "📱", "title": "Campus Legal Apps", "desc": "Mobile applications for legal assistance on campus"},
            {"icon": "👨‍⚖️", "title": "Find Legal Aid", "desc": "Locate free or low-cost legal services for students"},
            {"icon": "📅", "title": "Workshops & Events", "desc": "Upcoming legal education sessions on campus"},
            {"icon": "📖", "title": "Legal Handbook", "desc": "Comprehensive guide to student rights and responsibilities"}
        ]
        
        for i, resource in enumerate(resources):
            with resource_cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{resource['icon']}</div>
                    <h3>{resource['title']}</h3>
                    <p>{resource['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 📞 Emergency Contacts")
        st.markdown("Important contacts for immediate legal assistance")
        
        contacts = st.columns(3)
        with contacts[0]:
            st.markdown("""
            **Campus Security**  
            Emergency: (555) 123-4567  
            Non-emergency: (555) 123-4000  
            """)
        with contacts[1]:
            st.markdown("""
            **Student Legal Services**  
            Phone: (555) 987-6543  
            Email: legal@university.edu  
            """)
        with contacts[2]:
            st.markdown("""
            **National Legal Aid**  
            Hotline: 1-800-LEGAL-AID  
            Website: legalaid.org  
            """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h4>LexGuardian - Student Legal Empowerment</h4>
        <p>© 2023 • For Educational Purposes Only • Not Legal Advice</p>
        <p style="font-size:0.9rem;margin-top:10px;">Always consult qualified legal counsel for your specific situation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
