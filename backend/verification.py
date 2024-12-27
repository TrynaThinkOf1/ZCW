from config import app, db
from models import VerificationCodes

from flask_mail import Mail, Message
from datetime import datetime, timedelta
import random
from os import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent


SENDGRID_API_KEY = environ['user_auth_api_MAIL_API_KEY']
SENDER_EMAIL = environ['user_auth_api_MAIL_HOST_EMAIL']

def cleanup():
    expiration_cutoff = datetime.utcnow() - timedelta(minutes=15)
    expired_codes = VerificationCodes.query.filter(VerificationCodes.time_created <= expiration_cutoff).all()

    for code in expired_codes:
        db.session.delete(code)

    db.session.commit()


def gen_save_code():
    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    code = ''.join(random.choice(characters) for _ in range(6))
    print(code)
    saved_code = VerificationCodes(code=code)
    db.session.add(saved_code)
    db.session.commit()
    print("code saved: ", saved_code.code)
    return code

def send_email(email, code):
    html = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #333;">Verify Your Email</h2>
        <p style="color: #666;">Thank you for registering! Please use the following code to verify your email address:</p>
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h1 style="color: #333; text-align: center; letter-spacing: 5px;">{code}</h1>
        </div>
        <p style="color: #666;">This code will expire in 15 minutes.</p>
        <p style="color: #999; font-size: 12px;">If you didn't request this verification, please ignore this email.</p>
    </div>
    '''

    try:
        message = Mail(
            from_email=Email(SENDER_EMAIL),
            to_emails=To(email),
            subject='Email Verification',
            html_content=HtmlContent(html)
        )

        # Send email using SendGrid
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # Log success or handle any issues
        if response.status_code not in [200, 201, 202]:
            print(f"SendGrid API response: {response.status_code}")
            return {"message": f"Failed to send email: {response.status_code}"}

    except Exception as e:
        print(f"SendGrid error: {str(e)}")
        return {"message": str(e)}

def send_verify(email):
    code = gen_save_code()
    print(code)

    print("about to send email")
    send_email(email, code)
    print("email sent")
    return {'message': 'Verification email sent', 'code': code}, 200

def check_verify(code):
    cleanup()

    code_check = VerificationCodes.query.filter_by(code=code).first()
    print(code_check)
    if code_check:
        db.session.delete(code_check)
        db.session.commit()
        return True
    else:
        return False