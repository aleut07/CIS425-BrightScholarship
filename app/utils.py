from datetime import date
from flask_mail import Message
from . import mail

def calculate_age(birth_date):
    """Calculate the age of an applicant given their date of birth."""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def check_eligibility(applicant):
    """
    Check if an applicant meets the scholarship eligibility criteria:
    - Minimum cumulative GPA of 3.2
    - At least 12 credit hours during the semester
    - Age must not exceed 23 at the time of application
    """
    age = calculate_age(applicant.dob)
    return (
        applicant.gpa >= 3.2 and
        applicant.credit_hours >= 12 and
        age <= 23
    )

def send_email(subject, recipients, body):
    """
    Send an email using Flask-Mail.
    
    Parameters:
    - subject: Subject line of the email
    - recipients: List of recipient email addresses
    - body: Content of the email
    """
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)
