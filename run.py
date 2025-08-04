from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash

app = create_app()

# ✅ Run this block ONCE to create default admin
with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(email='admin@example.com').first():
        admin = Admin(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")

if __name__ == '__main__':
    app.run(debug=True)

