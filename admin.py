from datetime import datetime
import tool
from commons import *

signedInData = None
docs = None
slots = None
queries = []

def display(data=None):
    global signedInData
    if data != None: 
        signedInData = data
    tool.menu("\n\nWelcome to the Administrator Portal for {}!".format(signedInData[2]), [
        ("Manage Doctors", doclist),
        ("Patient Search", patientSearch),
        ("Messages", messages),
        ("Logout", tool.logout)
    ]) 

def doclist():
    global docs
    docs = tool.getQuery('admin', 'doctors', '*', 'WHERE hospitalid = "{}"'.format(signedInData[0]))
    tool.printTable(docs, {0: "Doctor ID", 3: "Name", 4: "Speciality", 1: "Password"})
    tool.menu('', [
        ("Add Doctor", addDoc),
        ("Edit Doctor Details", editDoc),
        ("Delete Doctor", delDoc),
        ("Manage Slots", slotlist),
        ("Return", display)
    ])

def messages():    
    global queries
    res = tool.getQuery('admin', 'queries', 'id, patientid, slotid, question', 'WHERE answer IS NULL AND hospitalid = {}'.format(str(signedInData[0])))
    queries = res
    for r in res:
        tool.printItem('Unanswered Query [ID: ' + str(r[0]) + ']', {
            (r[3]): ('Posted by Patient ' + str(r[1]) + ' for slot ' + str(r[2]))
        })
    tool.menu('', [
        ("Answer a question", queryAns),
        ("Return", display)
    ])

def queryAns():
    id, = tool.form([("Query ID", '\d*')])
    if int(id) not in [d[0] for d in queries]:
        print("Incorrect ID. Please try again.")
        queryAns()
    else:
        answer, = tool.form([
            ('Your response', ''), 
        ])
        tool.updateQuery("admin", "queries", {'answer': answer}, 'id = "{}"'.format(id))
        print("Response saved successfully.")

        messages()

def addDoc():
    name, branch = tool.form([
        ('Name of Doctor', ''), 
        ('Speciality', '')
    ])
    passw = tool.randstr(6)
    id = tool.writeQuery("admin", "doctors", "name, branch, hospitalid, password", "'" + "', '".join([name, branch, str(signedInData[0]), passw]) + "'")
    print("Doctor added.\n")
    print("Doctor ID: ", id)
    print("Password is: ", passw)

    doclist()

def editDoc():
    id, = tool.form([("Doctor ID", '\d*')])
    if int(id) not in [d[0] for d in docs]:
        print("Incorrect ID. Please try again.")
        editDoc()
    else:
        name, branch, passw = tool.form([
            ('New Name', ''), 
            ('New Speciality', ''),
            ('New Password (at least 6 characters)', '.......*')
        ])
        tool.updateQuery("admin", "doctors", {'name': name, 'branch': branch, 'password': passw}, 'id = "{}"'.format(id))
        print("Details updated successfully.")

        doclist()

def delDoc():
    id, = tool.form([("Doctor ID", '\d*')])
    if int(id) not in [d[0] for d in docs]:
        print("Incorrect ID. Please try again.")
        delDoc()
    else:
        tool.deleteQuery("admin", "doctors", 'id = "{}"'.format(id))
        print("Doctor deleted successfully.")

        doclist()

def slotlist():    
    global slots
    slots = tool.getQuery('admin', 'slots CROSS JOIN doctors', '*', 'WHERE slots.docid = doctors.id AND slots.hospitalid = "{}"'.format(signedInData[0]))
    temp = []
    for S in slots:
        status = ""
        slotTime = datetime.strptime(S[4] + " " + S[5], "%d-%m-%Y %H:%M").timestamp()
        currentTime = datetime.now().timestamp()
        if slotTime < currentTime or S[7] != None: 
            status = "Closed"
        else: 
            if S[3] == None:
                status = "Open"
            else:
                status = "Booked"
        temp.append(S + (status,))
    slots = temp
    tool.printTable(slots, {0: "Slot ID", 4: "Date", 5: "Start Time", 6: "End Time", 13: "Doctor", 14: "Department", 3: "Patient ID", 15: "Status"})
    tool.menu('', [
        ("Add Slot", addSlot),
        ("Delete Slot", delSlot),
        ("Return", doclist)
    ]) 

def addSlot():    
    date, strTime, endTime, docid = tool.form([
        ('Date (dd-mm-yyyy)', '\d\d-\d\d-\d\d\d\d'), 
        ('Start Time (hh:mm)', '\d\d:\d\d'),
        ('End Time (hh:mm)', '\d\d:\d\d'),
        ("Doctor ID", "\d*")
    ])
    id = tool.writeQuery("admin", "slots", "docid, hospitalid, date, starttime, endtime", "'" + "', '".join([docid, str(signedInData[0]), date, strTime, endTime]) + "'")
    print("Slot created successfully with ID " + str(id) + ".\n")
    
    slotlist()
                
def delSlot():
    id, = tool.form("Slot ID", '\d*')
    if int(id) not in [S[0] for S in slots]:
        print("Incorrect ID. Please try again.")
        delSlot()
    else:
        if slots[[S[0] for S in slots].index(int(id))][15] == "Closed": 
            print("Closed slots cannot be deleted.")
        else:    
            tool.deleteQuery("admin", "slots", 'id = "{}"'.format(id))
            print("Slot deleted successfully.")
        slotlist()