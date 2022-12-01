from functools import wraps

from flask import render_template, send_from_directory, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from app import app, db
from app.forms import RegisterForm, LoginForm, CreateProjectForm
from app.models import Project, User


# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise, continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', logged_in=current_user.is_authenticated)


@app.route('/about')
def about():
    return render_template('about.html', logged_in=current_user.is_authenticated)


@app.route('/contact')
def contact():
    return render_template('contact.html', logged_in=current_user.is_authenticated)


@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', all_projects=projects, logged_in=current_user.is_authenticated)


@app.route('/portfolio-details/<int:project_id>')
def portfolio_details(project_id):
    requested_project = Project.query.get(project_id)
    return render_template('portfolio-details.html', project=requested_project)


@app.route("/new-project", methods=["GET", "POST"])
@admin_only
def add_new_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        new_post = Project(name=form.name.data, category=form.category.data, used_technology=form.used_technology.data,
                           img_fg_path=form.img_fg_path.data, img_bg_path=form.img_bg_path.data,
                           github_url=form.github_url.data, description=form.description.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("portfolio"))
    return render_template("add-new-project.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/edit-post/<int:project_id>", methods=["GET", "POST"])
@admin_only
def edit_project(project_id):
    project = Project.query.get(project_id)
    edit_form = CreateProjectForm(name=project.name, category=project.category, used_technology=project.used_technology,
                                  img_fg_path=project.img_fg_path.data, img_bg_path=project.img_bg_path.data,
                                  github_url=project.github_url, description=project.description)
    if edit_form.validate_on_submit():
        project.name = edit_form.name.data
        project.category = edit_form.category.data
        project.used_technology = edit_form.used_technology.data
        project.img_fg_path = edit_form.img_fg_path.data
        project.img_bg_path = edit_form.img_bg_path.data
        project.github_url = edit_form.github_url.data
        project.description = edit_form.description.data
        db.session.commit()

        return redirect(url_for("portfolio_details", post_id=project.id))

    return render_template("add-new-project.html", form=edit_form, is_edit=True)


@app.route('/delete/<int:project_id>')
@admin_only
def delete_project(project_id):
    project_to_delete = Project.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('portfolio'))


@app.route('/resume')
def resume():
    return render_template('resume.html', logged_in=current_user.is_authenticated)


@app.route('/download')
def download():
    return send_from_directory(directory='static', path='assets/files/Dima_Boika_Python_Dev_CV.pdf', as_attachment=True)


# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if User.query.filter_by(email=form.email.data).first():
#             print(User.query.filter_by(email=form.email.data).first())
#             # User already exists
#             flash("You've already signed up with that email, log in instead!")
#             return redirect(url_for('login'))
#
#         hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
#         new_user = User(email=form.email.data, name=form.name.data, password=hash_and_salted_password)
#         db.session.add(new_user)
#         db.session.commit()
#         login_user(new_user)
#         return redirect(url_for("home"))
#
#     return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        # Email doesn't exist
        if user is None:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
