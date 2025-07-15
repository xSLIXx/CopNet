from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dein_geheimes_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------------------------
# Datenbank-Model
# ------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dienstnummer = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    server = db.Column(db.String(50), nullable=True)

# ------------------------
# Routen
# ------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dienstnummer = request.form['dienstnummer']
        password = request.form['password']

        user = User.query.filter_by(dienstnummer=dienstnummer).first()
        if user and check_password_hash(user.password, password):
            session['dienstnummer'] = user.dienstnummer
            session['role'] = user.role
            return f"Willkommen {user.dienstnummer} (Role: {user.role})"
        else:
            return "Login fehlgeschlagen!"

    return '''
        <form method="post">
            Dienstnummer: <input type="text" name="dienstnummer"><br>
            Passwort: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------------
# Main
# ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Erstellt DB & Tabellen falls nicht vorhanden
    app.run(debug=True)
