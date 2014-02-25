import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    print "%r" % github
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return {'first_name': row[0], 'last_name': row[1], 'github': row[2] }

def add_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project %s: %s with max grade %s" % (title, description, max_grade)

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s with github t%s" % (first_name, last_name, github)

def give_student_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Gave %s grade %s on %s project." % (student_github, grade, project_title)

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project Title: %s
Project Decription: %s
Maximum Grade: %d"""%(row[0], row[1], row[2])

def all_project_grades(title):
    query = """SELECT first_name,last_name, grade FROM reportcardview WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchall()
    grades = {}
    for i in range(len(row)):
        name = row[i][0]+" "+row[i][1]
        grades[name] = row[i][2]
    print grades
    return grades

def get_grade_by_student_project(last_name,title):
    query = """SELECT first_name, last_name, grade, title FROM reportcardview WHERE last_name = ? AND title = ?"""
    DB.execute(query, (last_name,title))
    row = DB.fetchone()
    print row
    print """%s %s got a grade of %s on the %s project"""%(row[0], row[1], row[2], row[3])

def get_all_grades(last_name):
    query = """SELECT first_name, last_name, grade, title FROM reportcardview WHERE last_name = ?"""
    DB.execute(query, (last_name,))
    row = DB.fetchall()
    grades = {}
    for i in range(len(row)):
        # print """%s %s got a grade of %s on the %s project"""%(row[i][0], row[i][1], row[i][2], row[i][3])
        grades[row[i][3]] = row[i][2]
        # print grades
    return grades

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        print "Type your command||arguments split||by double pipes"
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split("||")
        print tokens
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args)
        elif command == "project":
            get_project_by_title(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "new_project":
            add_project(*args)
        elif command == "student_grade":
            get_grade_by_student_project(*args)
        elif command == "assign_grade":
            give_student_grade(*args)
        elif command == "all_grades":
            get_all_grades(*args)
        elif command == "project_grades":
            all_project_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
