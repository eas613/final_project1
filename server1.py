import sys 
import os
from customer1 import Customer
from datetime import datetime
from BST_debt import Customer_BST
# from BST_id import Customer_BST_id

def invalid_line(fields):
    if len(fields) != 6 :
        print("length is other than 6.")
        return True      # line fields length incorrect
    if not all(field.isalpha() for field in fields[0:2]):
        print ("Error, Name invalid")
        return True       # name should only include alphabet characters
    if not all(field.isdigit() for field in fields[2:4]):
        print ("id or phone is not numeric.")
        return True       # id and phone should only include digits
    if  len(fields[2]) != 9 or len(fields[3]) != 10:
        print("Invalid length of id or phone .")
        return True       # id should be exactly 9 digits and phone exactly 10
    if not fields[3][0] == "0":
        print("phone must began with 0.")
        return True      #phone_num should start with 0
    try:
        fields[4] = float(fields[4])
    except ValueError:
        print("Error , invalid debt input.")
        return True   
    try:
        fields[5] = datetime.strptime(fields[5].strip(), "%d/%m/%Y").date()
    except ValueError:
        print("Invalid input of date format.")
        return True
    return False

if len(sys.argv) < 2 :
    print ("Error: missing csv file name.")
    quit()

bst = Customer_BST()

csv_file = sys.argv[1]
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass

with open(csv_file, "r") as fd:
    for line in fd.readlines():
        fields = line.strip().split(",")

        if invalid_line(fields):
            print("Error, invalid fields.\n")
            continue