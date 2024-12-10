from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Applicant, Awardee
from forms import ApplicationForm
from utils import calculate_age, check_eligibility, find_awardee
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
mail = Mail(app)

# Mock Registrar Office Data (replace with database queries in a real scenario)
REGISTRAR_DATA = {
    "12345": {"status": "Junior", "cumulative_gpa": 3.5, "credit_hours": 15},
    "67890": {"status": "Senior", "cumulative_gpa": 3.8, "credit_hours": 18},
}

@app.route('/')
def home():
    return render_template('base.html', current_year=datetime.now().year)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        student_data = REGISTRAR_DATA.get(form.student_number.data)
        if not student_data:
            flash("Student data could not be verified with the Registrar Office.", "danger")
            return redirect(url_for('apply'))

        # Save applicant data to the database
        applicant = Applicant(
            student_number=form.student_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            status=student_data["status"],
            cumulative_gpa=student_data["cumulative_gpa"],
            credit_hours=student_data["credit_hours"],
            eligible=False  # Eligibility checked later
        )
        db.session.add(applicant)
        db.session.commit()
        flash("Application submitted successfully.", "success")
        return redirect(url_for('home'))

    return render_template('apply.html', form=form)

@app.route('/review')
def review_applications():
    applicants = Applicant.query.all()
    for applicant in applicants:
        # Update eligibility based on rules
        age = calculate_age(applicant.date_of_birth)
        applicant.eligible = check_eligibility(
            gpa=applicant.cumulative_gpa,
            credit_hours=applicant.credit_hours,
            age=age
        )
        db.session.commit()

        # Notify ineligible applicants via email
        if not applicant.eligible:
            send_ineligibility_email(applicant.email, f"{applicant.first_name} {applicant.last_name}")
    
    eligible_applicants = [a for a in applicants if a.eligible]
    return render_template('review.html', applicants=eligible_applicants)

@app.route('/award')
def award_scholarship():
    eligible_applicants = Applicant.query.filter_by(eligible=True).all()
    if not eligible_applicants:
        flash("No eligible applicants available for awarding.", "warning")
        return redirect(url_for('home'))

    awardee = find_awardee(eligible_applicants)
    if awardee:
        # Save awardee details
        awarded = Awardee(
            student_id=awardee.student_number,
            full_name=f"{awardee.first_name} {awardee.last_name}",
            awarded_amount=0  # Placeholder; update with balance calculation
        )
        db.session.add(awarded)
        db.session.commit()

        # Notify awardee via email
        send_awardee_email(
            awardee.email,
            f"{awardee.first_name} {awardee.last_name}",
            awarded.awarded_amount
        )
        flash(f"Scholarship awarded to {awardee.first_name} {awardee.last_name}.", "success")
    else:
        flash("Could not determine awardee due to selection criteria conflicts.", "warning")

    return redirect(url_for('home'))

def send_ineligibility_email(recipient_email, full_name):
    """Sends an email to ineligible applicants."""
    subject = "Scholarship Application Update"
    sender_email = "scholarship@domain.com"
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.html = render_template('eligibility_email.html', full_name=full_name)
    mail.send(msg)

def send_awardee_email(recipient_email, full_name, awarded_amount):
    """Sends an email to the scholarship awardee."""
    subject = "Congratulations on Receiving the Scholarship!"
    sender_email = "scholarship@domain.com"
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.html = render_template('awardee_email.html', full_name=full_name, awarded_amount=awarded_amount)
    mail.send(msg)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures database tables are created
    app.run(debug=True)

