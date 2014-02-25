import hackbright_app

from flask import Flask, render_template, request

app = Flask(__name__)

# Code goes here
@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.get_all_grades(row['last_name'])
    html = render_template("student_info.html", first_name=row['first_name'], 
                            last_name=row['last_name'], 
                            github=row['github'], 
                            grades=grades)
    return html

@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    project_grades = hackbright_app.all_project_grades(project_title)
    html = render_template("project_grades.html",project=project_title,
                                                grades=project_grades)
    return html

@app.route("/add_student")
def add_student():
    hackbright_app.connect_to_db()
    html = render_template("new_student.html")    
    return html

@app.route("/student_added")
def student_added():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name =  request.args.get("last_name") 
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("student_added.html", first_name=first_name, last_name=last_name,
                                                    github=github)
    return html

@app.route("/add_project")
def add_project():
    hackbright_app.connect_to_db()
    html = render_template("add_project.html")    
    return html

@app.route("/project_added")
def project_added():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description =  request.args.get("description") 
    max_grade = request.args.get("max_grade")
    hackbright_app.add_project(title, description, max_grade)
    html = render_template("project_added.html", title=title, description=description, 
                                                max_grade=max_grade)
    return html

@app.route("/add_grade")
def add_grade():
    hackbright_app.connect_to_db()
    html = render_template("new_grade.html")    
    return html

@app.route("/grade_added")
def grade_added():
    hackbright_app.connect_to_db()
    github = request.args.get("github")
    title =  request.args.get("title") 
    grade = request.args.get("grade")
    hackbright_app.give_student_grade(github, title, grade)
    html = render_template("grade_added.html", github=github, title=title, 
                                                grade=grade)
    return html

if __name__ == "__main__":
    app.run(debug=True)