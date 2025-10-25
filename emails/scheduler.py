import asyncio
import random
from automail import send_email
from notifier import broadcast_progress_update  

progress = {
    "total": 0,
    "sent": 0,
    "pending": [],
    "completed": [],
    "running": False
}

# High-impact subject lines (can also vary per role if needed)
SUBJECT_LINES = [
    "Application for Software Developer – Experienced in FastAPI & React",
    "Proactive Backend Developer (FastAPI / Django / Spring Boot) Seeking Role",
    "Building Scalable Systems – Application for Developer Position",
    "Skilled Full-Stack Developer – Ready to Contribute from Day One",
    "Application for Backend Engineer – Expertise in Python, Java & REST APIs",
    "Innovative Developer Interested in Your Engineering Team",
    "FastAPI | Django | React Developer Interested in Open Roles",
    "Passionate Developer Looking to Add Value to Your Tech Team",
    "Experienced Java + Python Developer – Excited to Join Your Team",
    "Software Engineer Application – Delivering Clean & Scalable Code"
]

async def send_random_emails(email_list):
    progress["running"] = True
    progress["total"] = len(email_list)
    progress["sent"] = 0
    progress["pending"] = email_list.copy()
    progress["completed"] = []

    for email in email_list:
        # 🔹 Randomly pick role/template
        role = random.choice([1, 2])

        # 🔹 Randomly pick a strong subject line
        subject = random.choice(SUBJECT_LINES)

        # Send email using chosen role and subject
        success, message = send_email(email, subject, role)

        # Update progress
        progress["sent"] += 1
        progress["pending"].remove(email)
        progress["completed"].append({
            "email": email,
            "role": role,
            "subject": subject,
            "success": success,
            "message": message
        })

        # Broadcast live update to connected clients
        await broadcast_progress_update(progress)

        # Wait before sending next email (~2 minutes)
        await asyncio.sleep(10)

    # Job finished
    progress["running"] = False
    await broadcast_progress_update(progress)
