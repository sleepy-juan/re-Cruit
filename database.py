import Credentials as C
import pymysql

#from Credentials import host, port, user, passwd, db, charset;

def connect():
    return pymysql.connect(host=C.host, port=C.port, user=C.user, passwd=C.passwd, db=C.db, charset=C.charset)

def getAll(table):
    db = connect()
    result = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM %s;" % table
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        db.close()
    
    return result

def login_accept(id, password, type):
    account_list = getAll(type)
    if (type == "student"):
        for i in account_list:
            if ((i[0] == id) and (i[6] == password)):
                return True
        return False
    elif (type == "company"):

        for i in account_list:
            if ((i[0] == id) and(i[4] == password)):
                return True
        return False
    else:
        return False

def add_student(SID, fname, lname, phone, email, school, major, password):
    db = connect()
    
    try:
        with db.cursor() as cursor:
            sql = '''insert into student values(%d, "%s", "%s", "%s", "%s", "%s", "%s");''' % (SID, school, email, phone, fname, lname, password)
            cursor.execute(sql)
            sql = '''insert into major values(%d, "%s");''' % (SID, major)
            cursor.execute(sql)
        db.commit()
    finally:
        db.close()
    return True
def add_company(CID, email, address, name, password):
    db = connect()
    
    try:
        with db.cursor() as cursor:
            sql = '''insert into student values(%d, "%s", "%s", "%s", "%s");''' % (CID, email, address, name, password)
            cursor.execute(sql)
        db.commit()
    finally:
        db.close()
    return True

def add_course_student(SID, code, name, credit, syllabus, professor, grade, year, semester, retake):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = '''insert into course values(%d, "%s", "%s", "%s");''' % (code, name, credit, professor)
            cursor.execute(sql)
            sql = '''insert into takes values(%d, "%s", "%s", "%s", "%s", %d);''' % (SID, code, grade, year, semester, retake)
            cursor.execute(sql)
        db.commit()
    finally:
        db.close()
    return True

def add_work_student(SID, name, description, category):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = '''insert into didworks values(%d, "%s", "%s", "%s");''' % (SID, name, description, category)
            cursor.execute(sql)
        db.commit()
    finally:
        db.close()
    return True

def view_message_student(SID):
    db = connect()
    result = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM MESSAGE;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        db.close()
    result_filter = []
    for i in result:
        if (i[1] == SID):
            result_filter.append(i)
    return result_filter
def view_message_company(CID):
    db = connect()
    result = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM MESSAGE;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        db.close()
    result_filter = []
    for i in result:
        if (i[2] == CID):
            result_filter.append(i)
    return result_filter

def add_position(CID, Cname, Pname, PID, description, required_GPA, required_Code):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = '''insert into position values("%s", %d, "%s", "%s");''' % (pname, PID, description, required_GPA)
            cursor.execute(sql)
            sql = '''insert into holds values(%d, %d);''' % (CID, PID)
            cursor.execute(sql)
            for code in required_Code:
                sql = '''insert into requires values(%d, %d);''' % (code, PID)
                cursor.execute(sql)
        db.commit()
    except:
        return False
    finally:
        db.close()
    return True