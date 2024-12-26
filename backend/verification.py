from config import app, db
from models import VerificationCodes

from flask_mail import Mail, Message
from datetime import datetime, timedelta
import random
from os import environ

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'noreply.zeviberlin@gmail.com'
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSKEY')
mail = Mail(app)

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
    msg = Message('Email Verification',
                  sender='noreply.zeviberlin@gmail.com',
                  recipients=[email])

    msg.html = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #333;">Verify Your Email</h2>
        <p style="color: #666;">Thank you for registering! Please use the following code to verify your email address:</p>
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h1 style="color: #333; text-align: center; letter-spacing: 5px;">{code}</h1>
        </div>
        <p style="color: #666;">This code will expire in 1 hour.</p>
        <p style="color: #999; font-size: 12px;">If you didn't request this verification, please ignore this email.</p>
    </div>
    '''

    mail.send(msg)

def send_verify(email):
    code = gen_save_code()
    print(code)

    print("about to send email")
    send_email(email, code)
    print("email sent")
    return {'message': 'Verification email sent', 'code': code}, 200

def check_verify(code):
    code_check = VerificationCodes.query.filter_by(code=code).first()
    print(code_check)
    if code_check:
        return True
    else:
        return False