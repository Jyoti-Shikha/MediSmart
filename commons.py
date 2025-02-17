import sqlite3 as sql
from prettytable import PrettyTable

from patient import display

def patientSearch():
    con = sql.connect("patient.db")
    cur = con.cursor()
    cur.execute("select * from patients")
    s = cur.fetchall()
    print("Please provide the following details:\n")
    pid = input("Patient ID: ")
    if len(pid) == 0:
        print("Incorrect ID. Please try again.")
        patientSearch()
    if int(pid) not in [i[0] for i in s]:
        print("Patient does not exist. Try again")
        patientSearch()
    else:
        cur.execute("select * from patients where id = " + str(pid))
        res = cur.fetchone()
        print("\nHere are the search results:\n")
        pt = PrettyTable()
        pt.field_names = (["Patient ID", "Name", "Contact"])
        pt.add_row([res[0], res[2], res[3]])
        print(pt, "\n")
    

