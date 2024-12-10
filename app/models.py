from . import db
from datetime import datetime

class Applicant(db.Model):
    """Represents a student applying for the scholarship."""
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Male or Female
    dob = db.Column(db.Date, nullable=False)  # Date of Birth
    status = db.Column(db.String(20), nullable=False)  # Freshman, Sophomore, Junior, Senior
    gpa = db.Column(db.Float, nullable=False)  # Cumulative GPA
    credit_hours = db.Column(db.Integer, nullable=False)  # Credit hours taken in the semester
    eligible = db.Column(db.Boolean, default=None)  # Eligibility status (True/False/None)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date of application submission

    def __repr__(self):
        return f"<Applicant {self.first_name} {self.last_name}, GPA: {self.gpa}, Status: {self.status}>"

class Awardee(db.Model):
    """Represents the student awarded the scholarship."""
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Full name of the awardee
    awarded_amount = db.Column(db.Float, nullable=False)  # Scholarship amount
    awarded_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date when scholarship was awarded

    def __repr__(self):
        return f"<Awardee {self.name}, Amount: {self.awarded_amount}>"
