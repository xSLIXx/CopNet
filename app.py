from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Für Sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///copnet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# ---------- MODELS ----------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dienstnummer = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, chief, officer
    server = db.Column(db.String(10), nullable=False)  # z.B. S1

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- ROUTES ----------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dienstnummer = request.form['dienstnummer']
        password = request.form['password']

        user = User.query.filter_by(dienstnummer=dienstnummer).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Falsche Dienstnummer oder Passwort.')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Keine Berechtigung.')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)

# ---------- INIT ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Admin anlegen, falls nicht vorhanden
        admin = User.query.filter_by(dienstnummer='S0-ADM01').first()
        if not admin:
            new_admin = User(
                dienstnummer='S0-ADM01',
                password='1a2b3d4C.00',
                role='admin',
                server='S0'
            )
            db.session.add(new_admin)
            db.session.commit()
    app.run(debug=True)
