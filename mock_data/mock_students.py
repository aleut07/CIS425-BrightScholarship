from app.models import Applicant
from datetime import date

# Create 7 more students to put into the database

def populate_mock_data(db):
    """Populate the database with mock students."""
    if not Applicant.query.first():
        mock_students = [
            Applicant(
                student_number="S001",
                first_name="Alice",
                last_name="Smith",
                email="alice.smith@example.com",
                phone_number="1234567890",
                gender="Female",
                dob=date(2003, 5, 20),
                status="Junior",
                gpa=3.9,
                credit_hours=15,
                eligible=None
            ),
            Applicant(
                student_number="S002",
                first_name="Bob",
                last_name="Johnson",
                email="bob.johnson@example.com",
                phone_number="9876543210",
                gender="Male",
                dob=date(2002, 3, 10),
                status="Senior",
                gpa=3.8,
                credit_hours=14,
                eligible=None
            ),
            Applicant(
                student_number="S003",
                first_name="Charlie",
                last_name="Brown",
                email="charlie.brown@example.com",
                phone_number="5555555555",
                gender="Male",
                dob=date(2004, 11, 25),
                status="Sophomore",
                gpa=3.5,
                credit_hours=16,
                eligible=None
            ),
            Applicant(
                student_number="S004",
                first_name="Diana",
                last_name="Prince",
                email="diana.prince@example.com",
                phone_number="4444444444",
                gender="Female",
                dob=date(2001, 7, 15),
                status="Junior",
                gpa=3.7,
                credit_hours=18,
                eligible=None
            )
        ]

        db.session.bulk_save_objects(mock_students)
        db.session.commit()
