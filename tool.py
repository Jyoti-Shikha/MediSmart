import sqlite3 as sql
import regex as re
import random 
import string
from prettytable import PrettyTable
import webbrowser
import base64

def init():
    # Admin Database
    con = sql.connect('admin.db')
    cur = con.cursor()
    
    # Create Queries Table    
    cur.execute('''CREATE TABLE IF NOT EXISTS queries(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        patientid TEXT,
                        hospitalid TEXT,
                        slotid TEXT,
                        question TEXT,
                        answer TEXT 
                    );''')

    # Create Forum Table    
    cur.execute('''CREATE TABLE IF NOT EXISTS forum(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        patientid TEXT,
                        docid TEXT,
                        question TEXT,
                        answer TEXT 
                    );''')

    # Create Doctors table
    cur.execute('''CREATE TABLE IF NOT EXISTS doctors(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        password TEXT,
                        hospitalid INTEGER, 
                        name TEXT, 
                        branch TEXT
                    );''')

    # Create Slots Table
    cur.execute('''CREATE TABLE IF NOT EXISTS slots(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        docid INTEGER,
                        hospitalid INTEGER,
                        patientid INTEGER,
                        date TEXT,
                        starttime TEXT,
                        endtime TEXT,
                        prestext TEXT,
                        presfilename TEXT,
                        presfile BLOB 
                    );''')

    # Create Hospitals Table
    cur.execute('''CREATE TABLE IF NOT EXISTS hospitals(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        password TEXT,
                        name TEXT,
                        address TEXT,
                        pincode INTEGER,
                        phone TEXT,
                        description TEXT 
                    );''')

    con.commit()
    con.close()

    # Patient Database
    con = sql.connect('patient.db')
    cur = con.cursor()
    
    # Create Patients table
    cur.execute('''CREATE TABLE IF NOT EXISTS patients(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        password TEXT,
                        name TEXT,
                        phone TEXT
                    );''')
    con.commit()
    con.close()

def menu(init: str, items: list):
    # init = Menu Introduction Text
    # item = Tuple(prompt, function)
    print(init, '\n')
    for i, M in enumerate(items):
        print(str(i+1) + ".", M[0])
    while True:
        try:
            res = int(input("\n\nSelect one of the options above to continue: "))            
            items[res-1][1]() 
            break
        except Exception as e:
            continue
    return

def form(prompts: list, init: str='\nPlease provide the following details.'): 
    # prompt = Tuple(question, regex)
    print(init, '\n')
    res = []
    for P in prompts: 
        r = ''
        while r == '':
            r = input(P[0] + ": ").strip()
            if P[1] != '': 
                if not re.match(P[1], r):
                    print("Invalid input.")
                    r = ''
        res.append(r)
    return res

def getQuery(db: str, tables: str, cols: str, options: str):
    con = sql.connect(db + '.db')
    cur = con.cursor()
    cur.execute('SELECT ' + cols + ' FROM ' + tables + ' ' + options + ';')
    r = cur.fetchall()
    con.close()
    return r

def writeQuery(db: str, table: str, cols: str, values: str):
    con = sql.connect(db + '.db')
    cur = con.cursor()
    cur.execute('INSERT INTO ' + table + ' (' + cols + ') VALUES (' + values + ');')
    con.commit()
    cur.execute('SELECT last_insert_rowid();')
    r = cur.fetchone()
    con.close()
    return r[0]

def updateQuery(db: str, table: str, fields: dict, cond: str):
    con = sql.connect(db + '.db')
    cur = con.cursor()
    cur.execute('UPDATE ' + table + ' SET ' + ", ".join(["{} = '{}'".format(k, v) for k,v in fields.items()]) + " WHERE " + cond + ";")
    con.commit()
    con.close()
    return

def deleteQuery(db: str, table: str, cond: str):
    con = sql.connect(db + '.db')
    cur = con.cursor()
    cur.execute('DELETE FROM ' + table + " WHERE " + cond + ";")
    con.commit()
    con.close()
    return

def randstr(n: int):
    return ''.join(random.choices(string.digits + string.ascii_letters, k = n))

def printTable(T: list, labels: dict):
    # labels: dict((index: header))
    head = list(labels.values())   
    t = PrettyTable(head)
    for r in T:
        row = []
        for i in labels:
            row.append(r[i])    
        t.add_row(row)
    print(t)

def printItem(title: str, data: dict):
    # data = dict(header: value)
    x = PrettyTable(list(data.keys()))
    x.add_row(list(data.values()))
    print(x.get_string(title=title))

def insertblob(id: int, path: str):
    con = sql.connect("admin.db")
    cur = con.cursor()
    with open(path, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        t = "update slots set presfile = (?) where id = " + str(id)
    cur.execute(t, (base64_message,))
    con.commit()

def getblob(id: int):
    con = sql.connect("admin.db")
    cur = con.cursor()
    cur.execute("select id, presfile from slots where id = (?)", (str(id),))
    bytesdata = cur.fetchone()
    if bytesdata == None:
        print("No prescription to show")
    else:
        string = ""
        for i in bytesdata[1]:
            string = string + i
        sid = bytesdata[0]
        base = string.encode('utf-8')
        rand = random.randint(1, 1000)
        with open("Prescription" + str(sid) + ".pdf", 'wb') as file:
            decodeddata = base64.decodebytes(base)
            file.write(decodeddata)
        webbrowser.open_new("Prescription" + str(sid) + ".pdf")

def logout():
    return