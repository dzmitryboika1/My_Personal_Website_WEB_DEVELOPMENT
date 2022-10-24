from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField("Log In")


class CreateProjectForm(FlaskForm):
    name = StringField("Project's Name", validators=[DataRequired()])
    category = SelectField("Category",
                           choices=['Web Development', 'Python Scripting', 'API', 'Scraping Data', 'GUI', 'API',
                                    'Data Science & Machine Learning'])
    img_url = StringField("Image URL", validators=[DataRequired()])
    github_url = StringField("GitHub URL", validators=[DataRequired(), URL()])
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Project")
