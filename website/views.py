from flask import Flask,Blueprint, url_for, flash, redirect, render_template, abort, request
from flask_login import login_required, current_user
from wtforms import Form, StringField, PasswordField, validators, SubmitField, TextAreaField
from .models import db, User, Contact, UserMixin
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from flask_login import login_user, login_required, logout_user, current_user





views = Blueprint("views", __name__)


@views.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user, username = current_user.username)




@views.route('/')
def landing_page():
    return render_template('landing.html')


@views.route("/user")
@login_required
def user():
        return render_template('user.html', user=current_user)





@views.route("/contacts")
@login_required
def contacts():
    contact = current_user.contact.all()
    return render_template("contacts.html", user=current_user, contacts=contact)



class NewContactForm(FlaskForm):
    name = StringField("Full name", [validators.DataRequired(message="name is required"), Length(min=3, max=50)])
    phone_number = StringField("Phone Number", [validators.DataRequired(message="phone number is required"), Length(min=3, max=50)])
    email = StringField("Email Address")
    state = StringField("State")
    city = StringField("City")
    country = StringField("Country")
    submit = SubmitField("Add Contact")




@views.route("/add_contact", methods=["GET", "POST"])
@login_required
def add_contact():
    form = NewContactForm(request.form)
    name = form.name.data
    phone_number = form.phone_number.data
    email = form.email.data
    state = form.state.data
    city = form.city.data
    country = form.country.data
    if request.method == "POST" and form.validate_on_submit():
        contact = Contact.query.filter_by(phone_number=phone_number).first()
        if contact is None:
            new_contact = Contact(name=name, phone_number=phone_number, email=email, state=state, city=city, country=country, user_id = current_user.id)
            db.session.add(new_contact)
            db.session.commit()
            flash("New Contact addedd succesfull", category="success")
            return redirect(url_for("views.contacts"))
        else:
            flash("Phone number already exist", category="error")
            return redirect(url_for("views.contacts"))

    return render_template("add_contact.html", form=form, user=current_user)



class EditContactForm(FlaskForm):
    name = StringField("Full name", [validators.DataRequired(message="name is required"), Length(min=3, max=50)])
    phone_number = StringField("Phone Number", [validators.DataRequired(message="phone number is required"), Length(min=3, max=50)])
    email = StringField("Email Address")
    state = StringField("State")
    city = StringField("City")
    country = StringField("Country")
    submit = SubmitField("Edit Contact")



@views.route("/edit_contact/<int:contact_id>", methods=["GET","POST"])
def edit_contact(contact_id):
    form = EditContactForm(request.form)
   # user = User.query.get(current_user.id)
   # contact = user.contact.filter_by(id = contact.id).first()
    contact = Contact.query.get(contact_id)
    if contact is None:
        flash("the contact doesn't exist", category="error")
        return redirect(url_for("views.contacts"))
    else:

        if request.method == "POST" and  form.validate_on_submit():
            contact.name = form.name.data
            contact.phone_number = form.phone_number.data
            contact.email = form.email.data
            contact.state = form.state.data
            contact.city = form.city.data
            contact.country = form.country.data
            db.session.commit()
            flash("Contact edit succesfully", category="success")
            return redirect(url_for("views.contacts"))
        elif request.method == "GET":
            form.name.data = contact.name
            form.phone_number.data = contact.phone_number
            form.email.data = contact.email
            form.state.data = contact.state
            form.city.data = contact.city
            form.country.data = contact.country
    return render_template("edit_contact.html", form=form, contact=contact)

@views.route("/delete_contact/<int:contact_id>", methods=["GET", "POST"])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for("views.contacts"))
