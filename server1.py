import sys 
import os
from customer1 import Customer
from datetime import datetime
from BST_debt import Customer_BST
from BST_id import Customer_BST_id

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

def add_customer(csv_line):
    id = csv_line[2]
    if invalid_line(csv_line):
        print("Error, invalid csv_line.\n")
        return
    customer_to_update = bst_id.find_customer_by_id(id)
    if not customer_to_update:
        customer = Customer(*csv_line)
        bst.add_customer(customer)
        bst_id.add_customer(customer)
    else:
        if not id_name_match(customer_to_update,csv_line[0],csv_line[1]):
            return
        if not customer_to_update.check_and_update_date(csv_line[5]):
            return
        debt = csv_line[4]
        bst.remove_customer(customer_to_update)
        customer_to_update.add_debt(debt)
        bst.add_customer(customer_to_update)
    
def select_name(query):
    if len(query) > 3 :
        print ("invalid input , too many parameters, tip:name=...")
        return
    name_index = 5 if not query[2][4] == "!" else 6
    if len(query[2]) < name_index+1:
        print ("No name Entered.")
        return
    if not query[2][name_index:].isalpha():
        print("invalid type , (not alphabetic)")
        return
    if not bst.find_by_name(query[1],query[2][4],query[2][name_index:]):
        print (f"{query[1]} name {query[2][name_index:]} not found")
        return
    

def select_id(query):
    if len(query) > 2 :
        print ("invalid input , too many parameters, tip:id=... ")
        return
    id_index = 3 if not query[1][2] == "!" else 4
    if len(query[1]) != (id_index + 9 )or not query[1][id_index:].isdigit():
        print ("id must be 9 digits.")
        return
    if query[1][2] == "=":
        customer = bst_id.find_customer_by_id(query[1][id_index:]) 
        if customer :
            print (customer)
        else:
            print (f"id {query[1][id_index:]} not found")
        return
    elif bst.find_by_id(query[1][2],query[1][id_index:]):
        return
    else:
        print (f"id {query[1][id_index:]} not found")
        return

def select_phone(query):
    if len(query) > 2 :
        print ("invalid input , too many parameters, tip:phone=... ")
        return
    phone_index = 6 if not query[1][5] == "!" else 7
    if len(query[1]) != (10 + phone_index) or not query[1][phone_index:].isdigit():
        print ("Phone must be 10 digits.")
        return
    if not bst.find_by_phone(query[1][5],query[1][phone_index:]):
        print (f"{query[1][phone_index:]} phone number not found") 
        return

def select_debt(query):
    if query[1][4] == "!":
        try:
            amount = float(query[1][6:])
            return bst.find_by_debt("!=",amount)
        except ValueError:
            print("invalid input , enter debt amount. ")
            return
    else:
        try:
            amount = float(query[1][5:])
            return bst.find_by_debt(query[1][4],amount)
        except ValueError:
            print("invalid input , enter debt amount. ")
            return

def select_date(query):
    if query[1][4] == "!":
        try:
            date = datetime.strptime(query[1][6:].strip(), "%d/%m/%Y").date()
            return bst.find_by_date(query[1][4:6],date)
        except ValueError:
            print("Invalid input of date format.")
            return 
    else:
        try:
            date = datetime.strptime(query[1][5:].strip(), "%d/%m/%Y").date()
            return bst.find_by_date(query[1][4],date)
        except ValueError:
            print("invalid input of date format. ")
            return
    

def select(query):
    operators = ["=","<",">"]
    if len(query) < 2 :
        print("No parameters given .")
        return 
    elif query[1] == "first" or query[1] == "last":
        if len(query) < 3:
            print("nothing entered after 'first'/'last', tip:name=...")
            return
        if not query[2].startswith("name"):
            print (f"{query[2]} is unsupported. ")
            return
        if len(query[2]) < 5 or ((not query[2][4] in operators) and (len(query[2]) < 6 or not query[2][4:6] == "!=" )) :
            print("Enter a valid operator.")
            return
        select_name(query)
        return
    elif query[1].startswith("id"):
        if (len(query[1]) < 3 or ((not query[1][2] in operators)) and (len(query[1]) < 4 or not query[1][2:4] == "!=" )) :
            print("Enter a valid operator.")
            return
        select_id(query)
        return
    elif query[1].startswith("phone"):
        select_phone(query)
        return
    elif query[1].startswith("debt"):
        if len(query[1]) < 6 or not(query[1][4] in operators or query[1][4:6] == "!=" ) :
            print("invalid operator.")
            return
        if not select_debt(query):
            print("not found!")
        return
    elif query[1].startswith("date"):
        if len(query[1]) < 6 or not(query[1][4] in operators or query[1][4:6] == "!=" ) :
            print("invalid operator.")
            return
        if not select_date(query):
            print("not found!")
        return
    else:
        print(f"{query[1]} is not recognized")
        return 

def keys_valid(line):
    valid_keys =[['set', 'first', 'name='], ['last', 'name='], ['id='], ['phone='], ['dept='], ['date=']]
    if len(valid_keys) > len(line):
        print("missing fields. ")
        return False
    if len(valid_keys) < len(line):
        print("Too many fields. ")
        return False
    csv_line = []
    for i in range(len(valid_keys)):
        line[i] = line[i].strip().split()
        attr = line[i][-1].split("=")[-1]
        if not attr:
            print (f"missing info. ")
        csv_line.append(attr) 
    for i in range(len(line)):
        line[i][-1]=line[i][-1][:(line[i][-1].find(csv_line[i]))]
    if not line == valid_keys:
        print ("invalid line.")
        return
    return csv_line

def update(line):
    csv_line=keys_valid(line)
    if csv_line:
        add_customer(csv_line)
    

def id_name_match(customer:Customer,first,last):
    if customer.first != first or customer.last != last:
        print (f"{customer}  Name doesn't match {first} {last}")
        return False
    return True
if __name__ == "main":
    if len(sys.argv) < 2 :
        print ("Error: missing csv file name.")
        quit()

    bst = Customer_BST()
    bst_id = Customer_BST_id()

    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        with open(csv_file, "w"):
            pass

    with open(csv_file, "r") as fd:
        for line in fd.readlines():
            csv_line = line.strip().split(",")
            add_customer(csv_line)
            
        bst.print_ordered_by_debt()

    while True:
        query = input("==> ").strip().lower()
        if not query:
            print("Nothing entered.")
        elif query.startswith("select"):
            query =query.strip().lower().split()
            select(query)
        elif query.startswith("set"):
            query = query.strip().split(",")
            update(query)
        elif query == "print":
            bst.print_ordered_by_debt()
        elif query == "quit":
            break


