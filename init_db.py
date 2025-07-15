from app import db, User, app
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # Beispiel-Admin-User
    admin = User(
        dienstnummer='S0-ADM01',
        password=generate_password_hash('DeinAdminPasswort'),
        role='admin',
        server='DeinServerName'
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin-User erstellt!")
