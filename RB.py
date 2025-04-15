import streamlit as st
import requests
from io import StringIO
import os
MISTRAL_API_KEY =  "kikzWsaFDjKcHiV6gUCkp3jyUx6ojNqt"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
st.set_page_config(page_title="AI Resume Builder", layout="wide")

st.markdown("""
<style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    .resume-form {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .stButton>button {
        background-color: #4a8cff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #3a7be0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
    }
    
    .education-item {
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


if 'resume' not in st.session_state:
    st.session_state.resume = {
        'name': '',
        'email': '',
        'phone': '',
        'summary': '',
        'education': [{'degree': '', 'school': '', 'years': ''}],
        'experience': [{'title': '', 'company': '', 'years': '', 'description': ''}],
        'skills': [],
        'projects': [{'name': '', 'description': ''}]
    }

def get_ai_suggestion(prompt, context=""):
    if not MISTRAL_API_KEY:
        st.error("API key not configured")
        return ""
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": "You are a helpful resume assistant."},
        {"role": "user", "content": f"{context}\n\n{prompt}"}
    ]
    
    try:
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json={
                "model": "mistral-tiny",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 200
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"AI suggestion failed: {str(e)}")
        return ""


with st.container():
    st.title("Thunder Resume Builder")


with st.container():
    with st.form("resume_form"):
       
        st.header("1. Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.resume['name'] = st.text_input("Full Name", st.session_state.resume['name'])
            st.session_state.resume['email'] = st.text_input("Email", st.session_state.resume['email'])
        with col2:
            st.session_state.resume['phone'] = st.text_input("Phone", st.session_state.resume['phone'])

        
        st.header(" 2. Professional Summary")
        summary = st.text_area("Tell us about yourself", st.session_state.resume['summary'], height=100)
        st.session_state.resume['summary'] = summary

        
        st.header(" 3. Education")
        for i, edu in enumerate(st.session_state.resume['education']):
            cols = st.columns([2, 2, 1])
            with cols[0]:
                st.session_state.resume['education'][i]['degree'] = st.text_input(
                    f"Degree {i+1}", 
                    edu['degree'],
                    key=f"degree_{i}"
                )
            with cols[1]:
                st.session_state.resume['education'][i]['school'] = st.text_input(
                    f"School {i+1}", 
                    edu['school'],
                    key=f"school_{i}"
                )
            with cols[2]:
                st.session_state.resume['education'][i]['years'] = st.text_input(
                    f"Years {i+1}", 
                    edu['years'],
                    key=f"edu_years_{i}"
                )
            st.markdown("---")

        # Work Experience Section
        st.header("4. Work Experience")
        for i, exp in enumerate(st.session_state.resume['experience']):
            cols = st.columns([2, 2, 1])
            with cols[0]:
                st.session_state.resume['experience'][i]['title'] = st.text_input(
                    f"Job Title {i+1}", 
                    exp['title'],
                    key=f"title_{i}"
                )
            with cols[1]:
                st.session_state.resume['experience'][i]['company'] = st.text_input(
                    f"Company {i+1}", 
                    exp['company'],
                    key=f"company_{i}"
                )
            with cols[2]:
                st.session_state.resume['experience'][i]['years'] = st.text_input(
                    f"Years {i+1}", 
                    exp['years'],
                    key=f"exp_years_{i}"
                )
            st.session_state.resume['experience'][i]['description'] = st.text_area(
                f"Job Description {i+1}", 
                exp['description'],
                key=f"desc_{i}"
            )
            st.markdown("---")

       
        st.header(" 5. Skills")
        skills = st.text_input(
            "List your skills (comma separated)", 
            ", ".join(st.session_state.resume['skills'])
        )
        st.session_state.resume['skills'] = [s.strip() for s in skills.split(",") if s.strip()]

       
        st.header(" 6. Projects")
        for i, proj in enumerate(st.session_state.resume['projects']):
            st.session_state.resume['projects'][i]['name'] = st.text_input(
                f"Project Name {i+1}", 
                proj['name'],
                key=f"proj_name_{i}"
            )
            st.session_state.resume['projects'][i]['description'] = st.text_area(
                f"Project Description {i+1}", 
                proj['description'],
                key=f"proj_desc_{i}"
            )
            st.markdown("---")

        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.form_submit_button(" AI Summary Suggestion"):
                suggestion = get_ai_suggestion(
                    "Write a concise professional resume summary (3-4 sentences max):",
                    f"Name: {st.session_state.resume['name']}\nCurrent summary: {summary}"
                )
                if suggestion and not suggestion.startswith("AI suggestion failed"):
                    st.session_state.resume['summary'] = suggestion
                    st.rerun()
        
        with col2:
            if st.form_submit_button(" Skill Suggestions"):
                context = f"Education: {', '.join([edu['degree'] for edu in st.session_state.resume['education'] if edu['degree']])}"
                suggestion = get_ai_suggestion("Suggest 8-10 relevant technical skills for this education background as a comma-separated list:", context)
                if suggestion and not suggestion.startswith("AI suggestion failed"):
                    st.session_state.resume['skills'] = [s.strip() for s in suggestion.split(",")][:10]
                    st.rerun()
        
        with col3:
            if st.form_submit_button(" Save Resume Data"):
                st.success("Resume data saved!")

# Buttons outside the form
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Add Education"):
        st.session_state.resume['education'].append({'degree': '', 'school': '', 'years': ''})
        st.rerun()

with col2:
    if st.button("Add Experience"):
        st.session_state.resume['experience'].append({'title': '', 'company': '', 'years': '', 'description': ''})
        st.rerun()

with col3:
    if st.button(" Add Project"):
        st.session_state.resume['projects'].append({'name': '', 'description': ''})
        st.rerun()

with col4:
    if st.button("Clear All"):
        st.session_state.resume = {
            'name': '',
            'email': '',
            'phone': '',
            'summary': '',
            'education': [{'degree': '', 'school': '', 'years': ''}],
            'experience': [{'title': '', 'company': '', 'years': '', 'description': ''}],
            'skills': [],
            'projects': [{'name': '', 'description': ''}]
        }
        st.rerun()


def generate_html_file(resume_data):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_data['name']} - Resume</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .resume-container {{
            background-color: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 1px solid #3498db;
            padding-bottom: 5px;
            margin-top: 25px;
        }}
        .contact-info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 16px;
        }}
        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .skill {{
            background-color: #e8f4fc;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 14px;
        }}
        .education-item, .experience-item, .project-item {{
            margin-bottom: 15px;
        }}
        .section-header {{
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }}
        .summary {{
            font-size: 16px;
            line-height: 1.5;
        }}
        .job-description {{
            margin-top: 5px;
            padding-left: 15px;
        }}
    </style>
</head>
<body>
    <div class="resume-container">
        <h1>{resume_data['name']}</h1>
        
        <div class="contact-info">
            <div> {resume_data['email']}</div>
            <div> {resume_data['phone']}</div>
        </div>
        
        <h2>Professional Summary</h2>
        <div class="summary">{resume_data['summary']}</div>
        
        <h2>Education</h2>
"""
    
    for edu in resume_data['education']:
        if edu['degree'] or edu['school']:
            html_content += f"""
        <div class="education-item">
            <div class="section-header">
                <div>{edu['degree']}</div>
                <div>{edu['years']}</div>
            </div>
            <div>{edu['school']}</div>
        </div>
            """
    
    if any(exp['title'] for exp in resume_data['experience']):
        html_content += """
        <h2>Work Experience</h2>
"""
        for exp in resume_data['experience']:
            if exp['title']:
                html_content += f"""
        <div class="experience-item">
            <div class="section-header">
                <div>{exp['title']} at {exp['company']}</div>
                <div>{exp['years']}</div>
            </div>
            <div class="job-description">{exp['description']}</div>
        </div>
                """
    
    if resume_data['skills']:
        html_content += """
        <h2>Skills</h2>
        <div class="skills-container">
"""
        for skill in resume_data['skills']:
            html_content += f"""
            <div class="skill">{skill}</div>
"""
        html_content += """
        </div>
"""
    
    if any(proj['name'] for proj in resume_data['projects']):
        html_content += """
        <h2>Projects</h2>
"""
        for proj in resume_data['projects']:
            if proj['name']:
                html_content += f"""
        <div class="project-item">
            <div class="section-header">
                <div>{proj['name']}</div>
            </div>
            <div>{proj['description']}</div>
        </div>
                """
    
    html_content += """
    </div>
</body>
</html>
"""
    return html_content

# Download Section
st.header("Download Resume")
if st.button(" Generate HTML Resume"):
    if not st.session_state.resume['name']:
        st.warning("Please enter your name before generating the resume")
    elif not st.session_state.resume['summary']:
        st.warning("Please add a professional summary")
    else:
        html_content = generate_html_file(st.session_state.resume)
        
        st.download_button(
            label="⬇ Download HTML Resume",
            data=html_content,
            file_name="resume.html",
            mime="text/html"
        )
        
        st.success("Your HTML resume is ready!")
        st.info("After downloading, open the file in any web browser to view your resume.")


if st.checkbox("Show Resume Preview"):
    st.markdown("---")
    st.header("Resume Preview")
    if st.session_state.resume['name'] or st.session_state.resume['summary']:
        html_content = generate_html_file(st.session_state.resume)
        st.components.v1.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("Please fill in some resume details first")
