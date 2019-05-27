import Credentials as C
import pymysql
import random

#from Credentials import host, port, user, passwd, db, charset;

def connect():
    return pymysql.connect(host=C.host, port=C.port, user=C.user, passwd=C.passwd, db=C.db, charset=C.charset)

def query(sql):
    db = connect()
    result = []
    try:
        with db.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
    
    return result

def signIn(id, pw, type):
    if type == "student":
        sql = '''SELECT * FROM student WHERE sid = "%s" and password="%s"''' % (id, pw)
    else:
        sql = '''SELECT * FROM company WHERE cid = "%s" and password="%s"''' % (id, pw)
    
    res = query(sql)
    if len(res) == 0:
        return False
    return res[0]

def add(obj, type):
    if type == "student":
        sid = int(obj['sid'])
        sql = '''INSERT INTO student VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s");''' % (sid, obj['school'], obj['email'], obj['phone'], obj['fname'], obj['lname'], obj['password'])
        query(sql)

        sql = '''INSERT INTO major VALUES(%d, "%s")''' % (sid, obj['major'])
        query(sql)
    elif type == "company":
        cid = int(obj['cid'])
        sql = '''INSERT INTO company VALUES(%d, "%s", "%s", "%s", "%s");''' % (cid, obj['email'], obj['address'], obj['name'], obj['password'])
        query(sql)
    elif type == "work":
        sid = int(obj['sid'])
        sql = '''INSERT INTO didworks VALUES(%d, "%s", "%s", "%s");''' % (sid, obj["name"], obj["description"], obj["category"])
        query(sql)
    elif type == "course":
        sql = '''SELECT * FROM course WHERE code="%s"''' % obj['code']
        result = query(sql)
        if len(result) == 0:
            sql = '''INSERT INTO course VALUES("%s", "%s", "%s", "%s");''' % (obj['code'], obj['name'], obj['credit'], obj['professor'])
            query(sql)

        sid = int(obj['sid'])
        sql = '''INSERT INTO takes VALUES(%d, "%s", "%s", "%s", "%s")''' % (sid, obj['code'], obj['grade'], obj['year'], obj['semester'])
        query(sql)
    elif type == "position":
        pid = int(obj['pid'])
        required_gpa = float(obj['required_gpa'])
        sql = '''INSERT INTO position VALUES("%s", %d, "%s", %f);''' % (obj['name'], pid, obj['description'], required_gpa)
        query(sql)

        cid = int(obj['cid'])
        sql = '''INSERT INTO holds VALUES(%d, %d);''' % (cid, pid)
        query(sql)

        sql = '''INSERT INTO requires VALUES("%s", %d);''' % (obj['code'], pid)
        query(sql)

def get(what, uid):
    uid = int(uid)
    if what == "position":
        sql = '''SELECT position.pid, position.name, position.description, position.required_gpa 
        FROM position, company, holds 
        WHERE position.pid = holds.pid and holds.cid = company.cid and company.cid = %d;''' % uid
        result = query(sql)
        return result
    elif what == "course":
        sql = '''SELECT course.code, course.name, course.credit, takes.grade, course.professor, takes.year, takes.semester
        FROM course, takes, student
        WHERE course.code = takes.code and takes.sid = student.sid and student.sid = %d;''' % uid
        result = query(sql)
        return result
    elif what == "work":
        sql = '''SELECT didworks.name, didworks.description, didworks.category
        FROM didworks, student
        WHERE didworks.sid = student.sid and student.sid = %d;''' % uid
        result = query(sql)
        return result

def calculate(what, uid):
    uid = int(uid)
    if what == "position":
        courses = get("course", uid)
        gpa = list(map(lambda course: float(course[2]), courses))
        gpa = sum(gpa) / len(gpa)

        sql = '''SELECT company.name, position.name, position.description 
        FROM company, position, holds
        WHERE position.pid = holds.pid and holds.cid = company.cid and position.required_gpa < %f;''' % gpa
        result = query(sql)
        return result

def send(msg, f, t, sender):
    # f - user id, t - user name
    mid = int(random.random() * 10000000)
    if sender == "student":
        f = int(f)
        sql = '''INSERT INTO message VALUES(%d, %d, (SELECT cid FROM company WHERE company.name = "%s"), now(), now(), "%s", "%s");''' % (mid, f, t, msg, sender)
        query(sql)
    else:
        f = int(f)
        t = int(t)
        sql = '''INSERT INTO message VALUES(%d, %d, %d, now(), now(), "%s", "%s");''' % (mid, t, f, msg, sender)
        query(sql)

def receive(uid, receiver):
    uid = int(uid)
    if receiver == "student":
        sql = '''SELECT message.text, company.name
        FROM message, student, company
        WHERE message.sid = student.sid and message.cid = company.cid and message.sender = "company" and student.sid = %d;''' % uid
        result = query(sql)
        return result
    else:
        sql = '''SELECT message.text, student.fname, student.lname, student.sid
        FROM message, student, company
        WHERE message.sid = student.sid and message.cid = company.cid and message.sender = "student" and company.cid = %d;''' % uid
        result = query(sql)
        return result