from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Employee, Admin

main = Blueprint('main', __name__)

# -------------------------
# Dashboard
# -------------------------
@main.route('/')
@main.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('main.login'))

    employees = Employee.query.all()
    return render_template('dashboard.html', employees=employees)

# -------------------------
# Add Employee
# -------------------------
@main.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        new_employee = Employee(name=name, email=email)
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_employee.html')

# -------------------------
# Edit Employee
# -------------------------
@main.route('/edit_employee/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    if 'user' not in session:
        return redirect(url_for('main.login'))

    employee = Employee.query.get_or_404(emp_id)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        db.session.commit()

        flash('Employee updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_employee.html', employee=employee)

# -------------------------
# Delete Employee
# -------------------------
@main.route('/delete_employee/<int:emp_id>')
def delete_employee(emp_id):
    if 'user' not in session:
        return redirect(url_for('main.login'))

    employee = Employee.query.get_or_404(emp_id)
    db.session.delete(employee)
    db.session.commit()

    flash('Employee deleted successfully!', 'danger')
    return redirect(url_for('main.dashboard'))

# -------------------------
# Login
# -------------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.password == password:  # Simple check (hash in production)
            session['user'] = admin.email
            flash("Login successful!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')

# -------------------------
# Register
# -------------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_admin = Admin(username=username, email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')

# -------------------------
# Logout
# -------------------------
@main.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))
