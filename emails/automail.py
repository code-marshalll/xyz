import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

TEMPLATES = {
    1: {
        "body": """
        Dear HR,<br><br>
        I am excited to apply for the <b>Developer</b> role. 
        I have recently built a <b>user authentication microservice</b> with signup, login, and token-based authentication, 
        and I am currently working on a mini S3-like storage microservice.<br><br>
        
        I have also worked on full-stack projects including:<br>
        - <b>Django-based Patent Search engine</b>: Leveraging AI APIs for semantic similarity.<br>
        - Developed responsive front-end interfaces using <b>ReactJS</b>.<br><br>
        
        I am confident that my hands-on experience with microservices, React, web development, and AI-powered projects, 
        along with my achievements, make me a strong candidate for this role.<br><br>
        
        Please find my resume attached. I would be grateful for the opportunity to interview and demonstrate how I can contribute to your team.<br><br>
        
        Thank you for your time and consideration.<br><br>
        
        Warm regards,<br>
        Satyam Pathak<br>
        📧 satyampathak67@gmail.com<br>
        📱 +91-6388495727<br>
        🌐 <a href="https://github.com/satyampathakk">GitHub</a> | <a href="https://satyampathakk.github.io/portfolio/">Portfolio</a> | <a href="https://www.linkedin.com/in/satyampathakk/">LinkedIn</a>
        """,
        "resume": "resumes/satyam-pathak.pdf"
    },
    2: {
        "body": """
        Dear HR,<br><br>
        I am a final year B.Tech Computer Science student from Dr. A.P.J. Abdul Kalam Technical University, with hands-on experience in full-stack development and a strong eagerness to learn.<br><br>
        
        I have worked extensively with:<br>
        - Frontend: ReactJS, React Native, Tailwind CSS<br>
        - Backend: Python (Django, FastAPI), Node.js<br>
        - Tools & Database: MySQL, REST APIs, Docker, Jenkins<br><br>
        
        Some of my notable projects include:<br>
        - <b>Django Patent Search</b>: A web application to efficiently search and analyze patent data.<br>
        - <b>OnionTalk</b>: A secure messaging platform leveraging privacy-focused technologies.<br><br>
        
        I am particularly excited about working on-site, remote, collaborating with experienced engineers, and contributing to impactful products at your organization.<br><br>
        
        Please find my resume attached. I would be grateful for the opportunity to interview and demonstrate how I can contribute to your team.<br><br>
        
        Thank you for your time and consideration.<br><br>
        
        Warm regards,<br>
        Satyam Pathak<br>
        📧 satyampathak67@gmail.com<br>
        📱 +91-6388495727<br>
        🌐 <a href="https://github.com/satyampathakk">GitHub</a> | <a href="https://satyampathakk.github.io/portfolio/">Portfolio</a> | <a href="https://www.linkedin.com/in/satyampathakk/">LinkedIn</a>
        """,
        "resume": "resumes/satyam-resume.pdf"
    }
}

def send_email(to_email: str, subject: str, role: int):
    try:
        # Pick template
        template = TEMPLATES.get(role)
        if not template:
            raise ValueError("Invalid role selected")

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        # Body (HTML)
        msg.attach(MIMEText(template["body"], "html"))

        # Attachment
        resume_path = template["resume"]
        if os.path.exists(resume_path):
            with open(resume_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(resume_path)}")
                msg.attach(part)

        # SMTP Send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        return True, "✅ Email sent successfully!"
    except Exception as e:
        return False, f"❌ Failed: {e}"

