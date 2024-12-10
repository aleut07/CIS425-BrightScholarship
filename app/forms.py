from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class ApplicationForm(FlaskForm):
    """Form for students to apply for the scholarship."""
    student_number = StringField(
        'Student Number', 
        validators=[DataRequired(), Length(max=10, message="Student Number must be at most 10 characters.")]
    )
    first_name = StringField(
        'First Name', 
        validators=[DataRequired(), Length(max=50, message="First Name must be at most 50 characters.")]
    )
    last_name = StringField(
        'Last Name', 
        validators=[DataRequired(), Length(max=50, message="Last Name must be at most 50 characters.")]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email(message="Invalid email address.")]
    )
    phone_number = StringField(
        'Phone Number', 
        validators=[DataRequired(), Length(max=15, message="Phone Number must be at most 15 characters.")]
    )
    gender = SelectField(
        'Gender', 
        choices=[('Male', 'Male'), ('Female', 'Female')], 
        validators=[DataRequired()]
    )
    dob = DateField(
        'Date of Birth', 
        validators=[DataRequired(message="Please provide a valid date.")]
    )
    status = SelectField(
        'Academic Status', 
        choices=[
            ('Freshman', 'Freshman'), 
            ('Sophomore', 'Sophomore'), 
            ('Junior', 'Junior'), 
            ('Senior', 'Senior')
        ], 
        validators=[DataRequired()]
    )
    gpa = FloatField(
        'Cumulative GPA', 
        validators=[
            DataRequired(), 
            NumberRange(min=0.0, max=4.0, message="GPA must be between 0.0 and 4.0.")
        ]
    )
    credit_hours = IntegerField(
        'Credit Hours Taken This Semester', 
        validators=[
            DataRequired(), 
            NumberRange(min=0, message="Credit Hours must be a positive number.")
        ]
    )
    submit = SubmitField('Submit Application')
