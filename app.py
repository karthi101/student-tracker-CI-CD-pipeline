from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    marks = db.Column(db.Integer)
    grade = db.Column(db.String(5))

# Function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

# Home page — show students
@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

# Add student
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        marks = int(request.form["marks"])

        grade = calculate_grade(marks)

        new_student = Student(name=name, marks=marks, grade=grade)
        db.session.add(new_student)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")

# Delete student
@app.route("/delete/<int:id>")
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

# Create database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
