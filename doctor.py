import tool
from commons import *
import sqlite3 as sql

signedInData = None

con = sql.connect("admin.db")
cur = con.cursor()
cur.execute("select * from slots")
slots = cur.fetchall()

forumQues = []

def display(data=None):
    global signedInData
    if data != None: 
        signedInData = data
    tool.menu("\n\nWelcome to the Doctor Portal for {}!".format(signedInData[3]), [
        ("Appointments", appointments),
        ("Close appointment", closeslot),
        ("Patient Search", patientSearch),
        ("Forum", forum),
        ("Logout", tool.logout)
    ])

def appointments():
    global slots
    cur.execute("select * from slots where docid = " + str(signedInData[0]))
    res = cur.fetchall()
    pt = PrettyTable()
    pt.field_names = (["Slot ID", "Date", "Start", "End", "Patient ID"])
    for i in res:
        pt.add_row([i[0], i[4], i[5], i[6], i[3]])
    print(pt, "\n")
    display()

def forum():    
    global forumQues
    res = tool.getQuery('admin', 'forum', 'id, question, patientid', 'WHERE docid IS NULL')
    forumQues = res
    for r in res:
        tool.printItem('Unanswered Question [ID: ' + str(r[0]) + ']', {
            (r[1]): ('Posted by Patient ' + str(r[2]))
        })
    tool.menu('', [
        ("Answer a question", forumAns),
        ("Return", display)
    ])

def forumAns():
    id, = tool.form([("Question ID", '\d*')])
    if int(id) not in [d[0] for d in forumQues]:
        print("Incorrect ID. Please try again.")
        forumAns()
    else:
        answer, = tool.form([
            ('Your response', ''), 
        ])
        tool.updateQuery("admin", "forum", {'docid': signedInData[0], 'answer': answer}, 'id = "{}"'.format(id))
        print("Response saved successfully.")

        forum()

def closeslot():
    global slots
    id = input("Slot ID: ")
    if int(id) not in [S[0] for S in slots]:
        print("Incorrect ID. Please try again.")
        closeslot()
    else:    
        name = input("Enter prescription name: ")
        tool.updateQuery("admin", "slots", {"presfilename":name}, 'id = "{}"'.format(id))
        c = input("How do you want to upload the prescription?\n1. Text\n2. File\n")
        if c == "1":
            pres = input("Enter closing prescription: ")
            tool.updateQuery("admin", "slots", {"prestext":pres}, 'id = "{}"'.format(id)) 
        elif c == "2":
            pres = input("Enter file path: ")
            tool.insertblob(id, pres)
