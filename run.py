from flask import Flask, render_template, redirect, url_for, request
import database as db

app = Flask(__name__)

#--------------------------------------------------------------------------------
# Sign In
#

# Page - Sign In
@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")

# Process - Called when SignIn & SignUp
@app.route("/_signin", methods = ["POST"])
def _signin():
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
            return redirect(url_for('studentmypage', sid=result[0], Fname=result[4]))
        else:                   # as company
            return redirect(url_for('companymypage', name=result[3]))

#--------------------------------------------------------------------------------
# Sign In

# Page - Search with query
@app.route("/searchquery/<query>")
def searchquery(query):
    student, company, position, course = db.search(query)
    return render_template("search.html", students = student, companies = company, positions = position, courses = course)

@app.route("/search")
def search():
    return render_template("search.html")

# Process - Search
@app.route("/_search", methods=["POST"])
def _search():
    if request.method == "POST":
        query = request.form['query']
        return redirect(url_for('searchquery', query = query))

#--------------------------------------------------------------------------------
# Student
#

# Page - Student Enroll
@app.route("/student")
def student():
    return render_template("student.html")

# Process - Student Enroll
@app.route("/_studentenroll", methods=["POST"])
def _studentenroll():
    if request.method == "POST":
        db.add(request.form, "student")

        return redirect(url_for('studentmypage', sid = request.form["sid"], Fname = request.form["fname"]))
    
# Page - Student MyPage
@app.route("/studentmypage/<sid>/<Fname>/")
def studentmypage(sid, Fname):
    course = db.get("course", sid)
    work = db.get("work", sid)
    position = db.calculate("position", sid)
    message = db.receive(sid, "student")
    return render_template("studentmypage.html", sid = sid, Fname = Fname, courses = course, works = work, positions = position, messages = message)

# Page - Add Course
@app.route("/studentmypage/<sid>/<Fname>/addcourse")
def addcourse(sid, Fname):
    return render_template("addcourse.html")

# Process - Add Course
@app.route("/studentmypage/<sid>/<Fname>/_addcourse", methods = ["POST"])
def _addcourse(sid, Fname):
    if request.method == "POST":
        obj = {"sid": sid}
        for field in ["code", "name", "credit", "professor", "grade", "year", "semester"]:
            obj[field] = request.form[field]
        db.add(obj, "course")

        return redirect(url_for('studentmypage', sid = sid, Fname = Fname))

# Page - Add Work
@app.route("/studentmypage/<sid>/<Fname>/addwork")
def addwork(sid, Fname):
    return render_template("addwork.html")

# Process - Add Work
@app.route("/studentmypage/<sid>/<Fname>/_addwork", methods = ["POST"])
def _addwork(sid, Fname):
    if request.method == "POST":
        obj = {"sid": sid}
        for field in ["name", "description", "category"]:
            obj[field] = request.form[field]
        db.add(obj, "work")

        return redirect(url_for('studentmypage', sid = sid, Fname = Fname))

# Process - Send Message to Company
@app.route("/studentmypage/<sid>/<Fname>/_sendtocompany", methods = ["POST"])
def _sendtocompany(sid, Fname):
    if request.method == "POST":
        message = request.form['message']
        name = request.form['name']
        db.send(message, sid, name, "student")

        return redirect(url_for("studentmypage", sid = sid, Fname = Fname))

# Process - Send Message to Company
@app.route("/studentmypage/<sid>/<Fname>/_sendtocompany/<name>", methods = ["POST"])
def _sendtothecompany(sid, Fname, name):
    if request.method == "POST":
        message = request.form['message']
        db.send(message, sid, name, "student")

        return redirect(url_for("studentmypage", sid = sid, Fname = Fname))

#--------------------------------------------------------------------------------
# Company
#

# Page - Company Enroll
@app.route("/company")
def company():
    return render_template("company.html")

# Process - Company Enroll
@app.route("/_companyenroll", methods=["POST"])
def _companyenroll():
    if request.method == "POST":
        db.add(request.form, "company")

        return redirect(url_for('companymypage', name = request.form["name"]))

# Page - Company MyPage
@app.route("/companymypage/<name>/")
def companymypage(name):
    position = db.get("position", name)
    message = db.receive(name, "company")
    return render_template("companymypage.html", name = name, positions = position, messages = message)

# Page - Add Position
@app.route("/companymypage/<name>/addposition")
def addposition(name):
    return render_template("addposition.html")

# Process - Add Position
@app.route("/companymypage/<name>/_addposition", methods = ["POST"])
def _addposition(name):
    if request.method == "POST":
        db.add(request.form, "position")

        return redirect(url_for('companymypage', name = name))

# Process - Send Message to Student
@app.route("/companymypage/<name>/_sendtostudent", methods = ["POST"])
def _sendtostudent(name):
    if request.method == "POST":
        message = request.form['message']
        sid = request.form['sid']
        db.send(message, name, sid, "company")

        return redirect(url_for('companymypage', name = name))

# Process - Send Message to Student
@app.route("/companymypage/<name>/_sendtostudent/<sid>", methods = ["POST"])
def _sendtothestudent(name, sid):
    if request.method == "POST":
        message = request.form['message']
        db.send(message, name, sid, "company")

        return redirect(url_for('companymypage', name = name))

#--------------------------------------------------------------------------------
# run
#
if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=False)