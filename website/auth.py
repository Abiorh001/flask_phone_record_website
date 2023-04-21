from flask import Flask,Blueprint, url_for, render_template,flash, request, redirect
from wtforms import Form, StringField, PasswordField, validators, SubmitField, TextAreaField
from .models import db, User, UserMixin, Contact
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from . import mail




auth = Blueprint("auth", __name__, url_prefix="/auth")





class SignupForm(FlaskForm):
    full_name = StringField('Full Name',[validators.DataRequired(message="Full name is required"),validators.Length(min=4, max=100)])
    username = StringField('Username',[validators.DataRequired(message="Username is required"),validators.Length(min=4, max=25)])
    email = StringField('Email Address',[validators.DataRequired(message="Email is required"),validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.DataRequired(message="Password is required"),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')



@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
         full_name = form.full_name.data
         username = form.username.data
         email = form.email.data
         password = form.password.data

         user = User.query.filter_by(email=email).first()
         if user is not None:
             flash("Email already exist, please login!", category="error")
         
         else:
             user_name = User.query.filter_by(username=username).first()
             if user_name is not None:
                flash(f"{username} not available. use another username", category="error")
             else:
                new_user = User(full_name=full_name, username=username, email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()


                flash(f"Thanks for signing up! {username}", category="success")
                login_user(new_user, remember=True)
                
    

                #msg=Message("Thank You for your registration", sender="", recipients=[email])
                #link = url_for("views.home", _external=True)
                #msg.body = f"You can click here to login immediately {link}"
                #mail.send(msg)
                #flash("Confirmation email sent succesfully", category="success")
                return redirect(url_for('views.home'))

    return render_template("signup.html", form=form, user=current_user)









class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(message="Username is required")])
    password = PasswordField('Enter Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')





@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Username is not correct', category='error')
        elif user:
            if check_password_hash(user.password, password):
                flash("Login Successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect password try again!', category='error')
    return render_template("login.html", form=form, user=current_user)



class ForgetPassword(FlaskForm):
    email = StringField('Email Address',[validators.DataRequired(message="Email is required"),validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.DataRequired(message="Password is required"),validators.Length(min=6, max=50),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    submit = SubmitField('Change Password')

@auth.route("/forget_password", methods=["GET","POST"])
def forget_password():
    form = ForgetPassword()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            password = form.password.data
            user.password = generate_password_hash(password,method="sha256")
            db.session.commit()
            flash("password changed successfully!", category="sucess")
            return redirect(url_for("auth.login"))
        else:
            flash("No email address associated with this account", category="error")
            return redirect(url_for("auth.signup"))
    return render_template("forget_password.html", form=form)



class EditProfileForm(FlaskForm):
    full_name = StringField('Full Name', [validators.Length(0, 64)])
    location = StringField('Location', [validators.Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')



@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
     form = EditProfileForm()
     if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', category='sucess')
        return redirect(url_for('views.user'))

     elif request.method == "GET":
        form.full_name.data = current_user.full_name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
    
     return render_template('edit_profile.html', form=form)




@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.landing_page"))
