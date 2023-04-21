from flask import Flask, Blueprint, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail, Message
import os


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()


def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = "12J3RHRR744"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Lucifer_001@localhost:3306/phonecontactdb"
    app.config['WTF_CSRF_ENABLED'] = True
    
    # for email config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = ""
    app.config['MAIL_PASSWORD'] = ""

    from .views import views
    app.register_blueprint(views)

    from .auth import auth
    app.register_blueprint(auth)


    from .models import User,Contact
    db.init_app(app)
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)
        mail.init_app(app)

    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('views.landing_page'))



    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


     # error hadnling views
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404




    return app



 




