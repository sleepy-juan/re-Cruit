from flask import Flask, render_template, redirect, url_for, request
import database as db

app = Flask(__name__)

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/signin", methods = ["POST"])
def signin():
    if request.method == 'POST':
        uid = request.form["userid"]
        upw = request.form["userpw"]
        stu = request.form["role"]
        result = db.signIn(uid, upw, stu)

        if not result:
            if stu == "student":
                return redirect(url_for('student'))
            else:
                return redirect(url_for('company'))

        if stu == "student":    # as student
            return redirect(url_for('studentmypage', Fname=result[4]))
        else:                   # as company
            return redirect(url_for('companymypage', name=result[3]))

@app.route("/studentmypage/<Fname>/")
def studentmypage(Fname):
    return render_template("studentmypage.html", Fname = Fname)

@app.route("/companymypage/<name>/")
def companymypage(name):
    return render_template("companymypage.html", name = name)

@app.route("/student")
def student():
    return render_template("student.html")

@app.route("/company")
def company():
    return render_template("company.html")

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)


'''
@app.route("/")
def index():
    return render_template('index.html')

# url for select
@app.route("/select")
def select():
    # Connect to database
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='1111',
                         db='cs360',
                         charset='utf8')
    try:
        # Set cursor to the database
        with db.cursor() as cursor:
            # Write SQL query
            sql = "SELECT * FROM EMPLOYEE;"
            # Execute SQL
            cursor.execute(sql)

            # Fetch the result
            # result is dictionary type
            result = cursor.fetchall()
            # Print tuples

            output = ""
            for row in result:
                output += "{0} {1}\n".format(row[0], row[2])
    finally:
        db.close()

    return render_template('select.html', result=output)

@app.route("/redirect_insert")
def redirect_insert():
    return render_template('insert.html')

@app.route("/insert", methods = ['POST'])
def insert():
    if request.method == 'POST':
        fname = request.form['FirstName']
        lname = request.form['LastName']
        ssn = request.form['Ssn']
        return redirect(url_for('insert_sent', Fname = fname, Lname = lname, Ssn = ssn))

@app.route("/insert_sent/<Fname>/<Lname>/<Ssn>")
def insert_sent(Fname, Lname, Ssn):
    # Connect to database
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='1111',
                         db='cs360',
                         charset='utf8')
    try:
        # Set cursor to the database
        with db.cursor() as cursor:
            # Write SQL query
            sql = """INSERT INTO EMPLOYEE
                     VALUES('""" + Fname + """',
                            'E','"""\
                            + Lname + "','"\
                            + Ssn + """',
                            '1937-11-10',
                            '450 Stone, Houston, TX',
                            'M',
                            55000,
                            NULL,
                            1);"""
            # Execute SQL
            cursor.execute(sql)
        # You must manually commit after every DML methods.
        db.commit()
    finally:
        db.close()

    return redirect("/")

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
'''