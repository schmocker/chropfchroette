from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from sqlalchemy.exc import IntegrityError
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)

# Flask-WTF requires this line
csrf = CSRFProtect(app)

# Configure PostgreSQL connection
app.config[
    'SQLALCHEMY_DATABASE_URI'] = ('postgresql://chropfchroette:password@db:5432'
                                  '/chropfchroette')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)


with app.app_context():
    db.create_all()


class SubscribeForm(FlaskForm):
    email = EmailField('E-Mail', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Für Newsletter anmelden')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        new_subscriber = Subscriber(email=email)
        try:
            db.session.add(new_subscriber)
            db.session.commit()
            flash('Du hast dich erfolgreich angemeldet!', 'success')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('Diese E-Mail-Adresse ist bereits registriert.', 'info')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('Ein Fehler ist aufgetreten. Bitte versuche es erneut.', 'danger')
    return render_template('index.html', form=form)
