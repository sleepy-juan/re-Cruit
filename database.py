import Credentials as C
import pymysql

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
        sql = '''INSERT INTO student VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s");''' % (obj['sid'], obj['school'], obj['email'], obj['phone'], obj['fname'], obj['lname'], obj['password'])
        query(sql)

        sql = '''INSERT INTO student VALUES("%s", "%s")''' % (obj['sid'], obj['major'])
        query(sql)
    elif type == "company":
        sql = '''INSERT INTO company VALUES(%d, "%s", "%s", "%s", "%s");''' % (obj['cid'], obj['email'], obj['address'], obj['name'], obj['password'])
        query(sql)
    elif type == "work":
        sql = '''INSERT INTO didworks VALUES(%d, "%s", "%s", "%s");''' % (obj["sid"], obj["name"], obj["description"], obj["category"])
        query(sql)
    elif type == "course":
        sql = '''INSERT INTO course VALUES(%d, "%s", "%s", "%s");''' % (obj['code'], obj['name'], obj['credit'], obj['professor'])
        query(sql)

        sql = '''INSERT INTO takes VALUES(%d, "%s", "%s", "%s", "%s", %d)''' % (obj['sid'], obj['code'], obj['grade'], obj['year'], obj['semester'], obj['retake'])
        query(sql)
    elif type == "position":
        sql = '''INSERT INTO position VALUES("%s", %d, "%s", "%s");''' % (obj['pname'], obj['pid'], obj['description'], obj['required_GPA'])
        query(sql)

        sql = '''INSERT INTO holds VALUES(%d, %d);''' % (obj['cid'], obj['pid'])
        query(sql)
