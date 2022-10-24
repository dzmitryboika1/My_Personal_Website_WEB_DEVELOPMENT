from datetime import date
import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, CreateProjectForm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
Bootstrap(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLES IN DB
class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    github_url = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Project %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))


# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', all_projects=projects)


@app.route('/portfolio-details/<int:project_id>')
def portfolio_details(project_id):
    requested_project = Project.query.get(project_id)
    return render_template('portfolio-details.html', project=requested_project)


@app.route("/new-project", methods=["GET", "POST"])
def add_new_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        new_post = Project(name=form.name.data, category=form.category.data, date=date.today().strftime("%B %d, %Y"),
                           img_url=form.img_url.data, github_url=form.github_url.data, title=form.title.data,
                           description=form.description.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("portfolio"))
    return render_template("add-new-project.html", form=form)


@app.route("/edit-post/<int:project_id>", methods=["GET", "POST"])
def edit_post(project_id):
    project = Project.query.get(project_id)
    edit_form = CreateProjectForm(name=project.name, category=project.category, img_url=project.img_url,
                                  github_url=project.github_url, title=project.title, description=project.description)
    if edit_form.validate_on_submit():
        project.name = edit_form.name.data
        project.category = edit_form.category.data
        project.img_url = edit_form.img_url.data
        project.github_url = edit_form.github_url.data
        project.title = edit_form.title.data
        project.description = edit_form.description.data
        db.session.commit()

        return redirect(url_for("portfolio_details", post_id=project.id))

    return render_template("add-new-project.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:project_id>")
def delete_project(project_id):
    project_to_delete = Project.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('portfolio'))


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/download')
def download():
    return send_from_directory(directory='static', path='assets/files/Dima_Boika_Python_Dev_CV.pdf', as_attachment=True)


@app.route('/authentication')
def authentication():
    return render_template("authentication.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=form.email.data, name=form.name.data, password=hash_and_salted_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
