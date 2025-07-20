from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Portfolio credentials 
PORTFOLIO_EMAIL = os.getenv("PORTFOLIO_EMAIL")
PORTFOLIO_PASSWORD = os.getenv("PORTFOLIO_PASSWORD")

# Lab credentials
LAB_EMAIL = os.getenv("LAB_EMAIL")
LAB_PASSWORD = os.getenv("LAB_PASSWORD")

# Real Estate credentials
REALESTATE_EMAIL = os.getenv("REALESTATE_EMAIL")
REALESTATE_PASSWORD = os.getenv("REALESTATE_PASSWORD")

app = FastAPI()

# --- Pydantic Models ---

class PortfolioContactForm(BaseModel):
    name: str
    email: str
    message: str

class LabContactForm(BaseModel):
    name: str
    email: str
    phone: str
    medicare_id: str

class RealEstateContactForm(BaseModel):
    name: str
    email: str
    phone: str
    message: str

# --- Helper function ---

def send_email(subject: str, body: str, sender_email: str, sender_password: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = sender_email 
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# --- Routes ---

@app.post("/portfolio-contact")
def portfolio_contact(form: PortfolioContactForm):
    try:
        subject = f"Portfolio Message from {form.name}"
        body = f"Name: {form.name}\nEmail: {form.email}\n\nMessage:\n{form.message}"
        send_email(subject, body, PORTFOLIO_EMAIL, PORTFOLIO_PASSWORD)
        return JSONResponse(content={"message": "Portfolio message sent successfully!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/lab-contact")
def lab_contact(form: LabContactForm):
    try:
        subject = f"Lab Contact from {form.name}"
        body = (
            f"Name: {form.name}\nEmail: {form.email}\nPhone: {form.phone}\n"
            f"Medicare ID: {form.medicare_id}"
        )
        send_email(subject, body, LAB_EMAIL, LAB_PASSWORD)
        return JSONResponse(content={"message": "Lab contact submitted successfully!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/real-estate-contact")
def real_estate_contact(form: RealEstateContactForm):
    try:
        subject = f"Real Estate Contact from {form.name}"
        body = (
            f"Name: {form.name}\nEmail: {form.email}\nPhone: {form.phone}\n\n"
            f"Message:\n{form.message}"
        )
        send_email(subject, body, REALESTATE_EMAIL, REALESTATE_PASSWORD)
        return JSONResponse(content={"message": "Real estate contact submitted successfully!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
