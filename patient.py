from datetime import datetime
import sqlite3 as sql
import tool
from prettytable import PrettyTable

signedInData = None

con = sql.connect("admin.db")
cur = con.cursor()
cur.execute("select * from slots")
slots = cur.fetchall()

def display(data=None):
    global signedInData
    if data != None: 
        signedInData = data
    tool.menu("\n\nWelcome to the Patient Portal for {}!".format(signedInData[2]), [
        ("Search for Doctors", search),
        ("Appointments and Records", records),
        ("Forum", forum),
        ("Inquiries", inquire),
        ("Update account details", updateaccount),
        ("View medical history", gethistory),
        ("Logout", tool.logout)
    ])
    
def search():
    global slots
    pin, branch = tool.form([
        ('Your Pincode', '\d{6}'), 
        ('Medical Department', '')
    ])
    slots = tool.getQuery('admin', '(slots JOIN doctors ON slots.docid = doctors.id) JOIN hospitals on slots.hospitalid = hospitals.id', '*', 'WHERE hospitals.pincode = "{}" AND doctors.branch LIKE "%{}%" AND slots.patientid IS NULL'.format(pin, branch))
    
    k = 0
    print("\nHere are your search results.\n")
    for S in slots:
        slotTime = datetime.strptime(S[4] + " " + S[5], "%d-%m-%Y %H:%M").timestamp()
        currentTime = datetime.now().timestamp()
        if currentTime < slotTime:     
            k += 1
            tool.printItem("[Slot ID: " + str(S[0]) + "] Dr. " + S[13] + ", " + S[17], {
                'Date': S[4],
                'Time': S[5] + " to " + S[6],
                'Hospital Address': S[18],
                'Hospital Phone': S[20],
                'About Hospital': S[21]            
            })
    if k == 0:
        print("No doctors are available at the moment.")
        display()
    tool.menu('', [
        ("Book an appointment", bookSlot),
        ("Send inquiry to a hospital", inquire),
        ("Return", display)
    ])     

def forum():
    res = tool.getQuery('admin', 'forum', 'question, answer, docid', 'WHERE patientid = "{}"'.format(signedInData[0]))
    
    for r in res:
        tool.printItem('Unanswered' if r[2] == None else 'Answered', {
            ('Question: ' + r[0]): ('Answer: ' + str(r[1]))
        })
    tool.menu('', [
        ("Ask a question", forumAsk),
        ("Return", display)
    ])

def forumAsk(): 
    query, = tool.form([("Ask your question", '')])
    tool.writeQuery("admin", "forum", "patientid, question", "'" + "', '".join([str(signedInData[0]), query]) + "'")
    print("Question posted successfully.")
    forum()

def bookSlot():
    id, = tool.form([("Slot ID", '\d*')])
    if int(id) not in [S[0] for S in slots]:
        print("Incorrect ID. Please try again.")
        bookSlot()
    else:
        tool.updateQuery("admin", "slots", {'patientid': signedInData[0]}, "id = '{}'".format(id))
        print("Appointment booked successfully.")
        display()

def inquire():
    id, = tool.form([("Slot ID", '\d*')])
    if int(id) not in [S[0] for S in slots]:
        print("Incorrect ID. Please try again.")
        bookSlot()
    else:
        query, = tool.form([("Your query", '')])
        tool.writeQuery("admin", "queries", "patientid, hospitalid, slotid, question", "'" + "', '".join([str(signedInData[0]), str(slots[[S[0] for S in slots].index(int(id))][15]), id, query]) + "'")
        print("Inquiry sent successfully.")
        display()

def gethistory():
    global slots
    id = input("Slot ID: ")
    if int(id) not in [S[0] for S in slots]:
        print("No medical history to show")
        gethistory()
    else:
        for S in slots:
            if S[0] == int(id):
                print("Date:", S[4])
                print("Start time:", S[5])
                print("End time:", S[6])
                if S[9] == None and S[7] == None:
                    print("No prescription to show. Try again after some time")
                if S[9] != None:
                    print("Prescription name:", S[8])
                    tool.getblob(id)
                elif S[7] != None:
                    print("Prescription name:", S[8])
                    print("Prescription:", S[7])
                print()
    display()

def updateaccount():
    con = sql.connect("patient.db")
    cur = con.cursor()
    print("Please provide the following details:\n")
    pid = int(input("Enter your ID: "))
    passw = input("Enter your password: ")
    cur.execute("select password from patients where id = " + str(pid))
    res = cur.fetchone()
    if len(res) == 0:
        print("Invalid ID. Please try again.")
        updateaccount()
    elif passw != res[0]:
        print("Invalid password. Please try again.")
    else:
        c = input("\nWhat do you want to change?\n1. Password\n2. Name\n3. Contact number\n4. Return\n\nSelect one of the options above to continue: ")
        if c == "1":
            npass = input("Enter new password: ")
            cur.execute("update patients set password = (?) where id = " + str(pid), (npass,))
            con.commit()
        elif c == "2":
            nname = input("Enter new profile name: ")
            cur.execute("update patients set name = (?) where id = " + str(pid), (nname,))
            con.commit()
        elif c == "3":
            nphone = input("Enter new contact: ")
            cur.execute(("update patients set phone = (?) where id = " + str(pid)), (nphone,))
            con.commit()
        elif c == "4":
            display()

def records():
    global slots
    cur.execute("select * from slots where patientid = " + str(signedInData[0]))
    res = cur.fetchall()
    pt = PrettyTable()
    pt.field_names = (["Slot ID", "Date", "Start", "End", "Doctor ID", "Hospital ID"])
    for i in res:
        pt.add_row([i[0], i[4], i[5], i[6], i[1], i[2]])
    print(pt, "\n")
    display()