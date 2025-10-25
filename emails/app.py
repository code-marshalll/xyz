from fastapi import FastAPI, Form, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from automail import send_email
from scheduler import send_random_emails, progress
from notifier import connected_clients, broadcast_progress_update  # ✅ centralized notifier
import asyncio
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static assets (CSS, JS)
app.mount("/static", StaticFiles(directory="templates"), name="static")


# ===============================
#  MAIN DASHBOARD (Unified Page)
# ===============================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ===============================
#  SINGLE EMAIL ENDPOINT
# ===============================
@app.post("/send-single")
def send_single(
    request: Request,
    hr_email: str = Form(...),
    subject: str = Form(...),
    role: int = Form(...),
):
    success, message = send_email(hr_email, subject, role)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "success": success, "message": message},
    )


# ===============================
#  MULTIPLE EMAIL ENDPOINT
# ===============================
@app.post("/send-multiple")
def send_multiple(
    hr_emails: List[str] = Form(...),
    subject: str = Form(...),
    role: int = Form(...),
):
    results = []
    for email in hr_emails:
        success, message = send_email(email, subject, role)
        results.append({email: message})
    return {"results": results}


# ===============================
#  AUTO RANDOM EMAILING
# ===============================
@app.post("/auto-random-start")
async def auto_random_start(emails: str = Form(...)):
    email_list = [e.strip() for e in emails.split(",") if e.strip()]
    if not email_list:
        return JSONResponse({"error": "No emails provided."}, status_code=400)

    if progress["running"]:
        return JSONResponse({"message": "A job is already running."}, status_code=409)

    asyncio.create_task(send_random_emails(email_list))
    return JSONResponse(
        {"message": "Started automated random cold emailing.", "total": len(email_list)}
    )


# ===============================
#  WEBSOCKET: REAL-TIME UPDATES
# ===============================
@app.websocket("/auto-random-updates")
async def auto_random_updates(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        # Send current progress immediately upon connect
        await websocket.send_text(json.dumps(progress))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"WebSocket error: {e}")
