from flask import render_template, redirect, url_for, flash, request
from . import db, mail
from .models import Applicant, Awardee
from .forms import ApplicationForm
from flask_mail import Message
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def check_eligibility(applicant):
    if applicant.gpa >= 3.2 and applicant.credit_hours >= 12 and calculate_age(applicant.dob) <= 23:
        return True
    return False

@routes.route('/', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        applicant = Applicant(
            student_number=form.student_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            gender=form.gender.data,
            dob=form.dob.data,
            status=form.status.data,
            gpa=form.gpa.data,
            credit_hours=form.credit_hours.data
        )
        db.session.add(applicant)
        db.session.commit()
        return redirect(url_for('review_applicants'))
    return render_template('apply.html', form=form)

@routes.route('/review')
def review_applicants():
    applicants = Applicant.query.all()
    for applicant in applicants:
        applicant.eligible = check_eligibility(applicant)
        db.session.commit()

    # Email non-eligible applicants
    non_eligible = Applicant.query.filter_by(eligible=False).all()
    for app in non_eligible:
        msg = Message("Scholarship Eligibility", recipients=[app.email])
        msg.body = f"Dear {app.first_name}, you are not eligible for the scholarship."
        mail.send(msg)

    return render_template('review.html', applicants=applicants)
