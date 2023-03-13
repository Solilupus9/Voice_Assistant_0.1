def changingname():
    email=input("Enter email address:")
    code16=input("Enter your 16 digit security code:").replace(' ','')
    f = open("datalog.txt", "w")
    f.writelines(email)
    f.write("\n")
    f.writelines(code16)
    f.close()
    print("Entered data:")

def dataread():
    file=open('datalog.txt')
    content= file.readlines()
    print(content[0]+content[1])

changingname()
dataread()
