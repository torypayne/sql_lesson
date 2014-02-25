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
    print row
    print row['last_name']
    grades = hackbright_app.get_all_grades(row['last_name'])
    print "This is grades"
    print grades
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

if __name__ == "__main__":
    app.run(debug=True)