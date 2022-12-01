from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, ValidationError, EqualTo
from flask_ckeditor import CKEditorField

from app.models import User


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Me Up!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")


class CreateProjectForm(FlaskForm):
    name = StringField("Project's Name", validators=[DataRequired()])
    category = SelectField("Category",
                           choices=['Web Development', 'Python Scripting', 'API', 'Scraping Data', 'GUI', 'API',
                                    'Data Science & Machine Learning'])
    used_technology = StringField("Technology", validators=[DataRequired()])
    img_fg_path = StringField("Image fg path", validators=[DataRequired()])
    img_bg_path = StringField("Image bg path", validators=[DataRequired()])
    github_url = StringField("GitHub URL", validators=[DataRequired(), URL()])
    description = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Project")
