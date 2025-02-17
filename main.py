import tool
import patient
import admin
import doctor

signedInData = None

def patientMenu():
    tool.menu('', [('Sign Up', patientSignUp), ('Sign In', patientSignIn), ('Return', main)])

def adminMenu():
    tool.menu('', [('Sign Up', adminSignUp), ('Sign In', adminSignIn), ('Return', main)])

def doctorMenu():
    tool.menu('', [('Sign In', doctorSignIn), ('Return', main)])

def exit():
    print("Thank you for using MediSmart!")
    quit()

def patientSignUp():
    global signedInData
    name, phone, passw = tool.form([
        ('Name', ''), 
        ('Phone Number', '\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*'), 
        ('Password (at least 6 characters)', '.......*')
    ])
    id = tool.writeQuery("patient", "patients", "name, phone, password", "'" + "', '".join([name, phone, passw]) + "'")
    signedInData = (id, passw, name, phone)
    print("You were successfully registered. Here are your account details: \n")
    print("Patient ID: ", signedInData[0])
    print("Your password is: ", signedInData[1])

    patient.display(signedInData)    

def patientSignIn():
    global signedInData
    id, passw = tool.form([
        ('Patient ID', ''), 
        ('Password', '')
    ])
    data = tool.getQuery("patient", "patients", "*", "WHERE id='{}'".format(id))
    if len(data) == 0:
        print("\nIncorrect Patient ID. Please try again.")
        patientSignIn()
    else:
        if passw != data[0][1]:
            print("\nIncorrect Password. Please try again.")
            patientSignIn()
        else:
            print("\nLogged in successfully.")
            signedInData = data[0]
            patient.display(signedInData)     

def adminSignUp():
    global signedInData
    name, address, pincode, phone, description, passw = tool.form([
        ('Hospital Name', ''), 
        ('Address', ''), 
        ('Pincode (6-digit)', '\d{6}'),
        ('Phone Number', '\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*'), 
        ('Description', ''), 
        ('Password (at least 6 characters)', '.......*')
    ])
    id = tool.writeQuery("admin", "hospitals", "name, address, pincode, phone, description, password", "'" + "', '".join([name, address, pincode, phone, description, passw]) + "'")
    signedInData = (id, passw, name, address, pincode, phone, description)
    print("You were successfully registered. Here are your account details: \n")
    print("Hospital ID: ", signedInData[0])
    print("Your password is: ", signedInData[1])
    
    admin.display(signedInData)

def adminSignIn():
    global signedInData
    id, passw = tool.form([
        ('Hospital ID', ''), 
        ('Password', '')
    ])
    data = tool.getQuery("admin", "hospitals", "*", "WHERE id='{}'".format(id))
    if len(data) == 0:
        print("\nIncorrect Hospital ID. Please try again.")
        adminSignIn()
    else:
        if passw != data[0][1]:
            print("\nIncorrect Password. Please try again.")
            adminSignIn()
        else:
            print("\nLogged in successfully.")
            signedInData = data[0]
            admin.display(signedInData)

def doctorSignIn():
    global signedInData
    id, passw = tool.form([
        ('Doctor ID', ''), 
        ('Password', '')
    ])
    data = tool.getQuery("admin", "doctors", "*", "WHERE id='{}'".format(id))
    if len(data) == 0:
        print("\nIncorrect Doctor ID. Please try again.")
        doctorSignIn()
    else:
        if passw != data[0][1]:
            print("\nIncorrect Password. Please try again.")
            doctorSignIn()
        else:
            print("\nLogged in successfully.")
            signedInData = data[0]
            doctor.display(signedInData)

def main():
    tool.menu('Welcome to MediSmart!', [('Continue as Patient', patientMenu), ('Continue as Administrator', adminMenu), ('Continue as Doctor', doctorMenu), ('Exit', exit)])
    main()

tool.init()
main()