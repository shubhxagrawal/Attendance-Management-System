from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(10), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    if 'professor_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        professor = Professor.query.filter_by(username=username, password=password).first()
        if professor:
            session['professor_id'] = professor.id  # Store professor ID in session
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'professor_id' not in session:
        return redirect(url_for('login'))
    session.pop('professor_id', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'professor_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))
    divisions = ['A', 'B']
    return render_template('dashboard.html', divisions=divisions)

@app.route('/remove_student/<int:student_id>', methods=['POST'])
def remove_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash(f"Student {student.name} removed successfully!", "success")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for('view_students'))


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'professor_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        division = request.form['division']

        # Ensure the data is valid
        if not name or not division:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('add_student'))

        # Add the student to the database
        new_student = Student(name=name, division=division)
        db.session.add(new_student)
        db.session.commit()

        flash("Student added successfully!", "success")
        return redirect(url_for('view_students'))

    return render_template('add_student.html')


@app.route('/students')
def view_students():
    if 'professor_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/mark_attendance/<division>', methods=['GET', 'POST'])
def mark_attendance(division):
    if 'professor_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    current_date = datetime.now().date()

    if request.method == 'POST':
        selected_date = request.form['date']
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

        if selected_date > current_date:
            flash("You cannot mark attendance for a future date.", "danger")
            return redirect(url_for('mark_attendance', division=division))

        existing_attendance = Attendance.query.filter_by(date=selected_date).all()
        if existing_attendance:
            flash("Attendance has already been marked for this date.", "warning")
            return redirect(url_for('mark_attendance', division=division))

        students = Student.query.filter_by(division=division).all()
        for student in students:
            status = request.form.get(str(student.id))
            if status:
                attendance = Attendance(student_id=student.id, date=selected_date, status=status)
                db.session.add(attendance)
        db.session.commit()
        flash("Attendance marked successfully!", "success")
        return redirect(url_for('dashboard'))

    # Fetch students and print them for debugging
    students = Student.query.filter_by(division=division).all()
    print(students)  # Add this to check the data being fetched
    return render_template('attendance.html', division=division, current_date=current_date, students=students)

@app.route('/attendance_report')
def attendance_report():
    if 'professor_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    students = Student.query.all()
    reports = []

    for student in students:
        attendance_records = Attendance.query.filter_by(student_id=student.id).all()
        monthly_report = {}

        for record in attendance_records:
            month_year = record.date.strftime('%Y-%m')  # Format as Year-Month
            if month_year not in monthly_report:
                monthly_report[month_year] = {'present': 0, 'absent': 0}
            if record.status == 'Present':
                monthly_report[month_year]['present'] += 1
            else:
                monthly_report[month_year]['absent'] += 1

        reports.append({'name': student.name, 'division': student.division, 'monthly_report': monthly_report})

    return render_template('report.html', reports=reports)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
        if Professor.query.count() == 0:
            professor = Professor(username="root", password="root")
            db.session.add(professor)
            db.session.commit()
            print("Default professor added!")
    app.run(debug=True)
