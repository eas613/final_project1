import sys 
import os
from customer1 import Customer
from datetime import datetime
from BST_debt import Customer_BST
from BST_id import Customer_BST_id
import socket
from threading import Thread , Lock

def handle_connection(client_socket,client_address,mutex):
    while True:
        query = client_socket.recv(1024).decode().strip().lower()
        if not query:
            data =  "Nothing entered." , False
        elif query.startswith("select"):
            data = query.strip().lower().split()
            response = select(data)
            if type(response[0]) == list:
                s = ""
                for c in response[0]:
                    s+=str(c)+"\n"
                client_socket.sendall(s.encode())
            else:
                client_socket.sendall(str(response[0]).encode())
        elif query.startswith("set"):
            query = query.strip().split(",")
            response = update(query)
            if response[1]:
                with mutex:
                    with open('db.csv', 'a') as file:
                        response[1][4]=str(response[1][4])
                        response[1][5]=str(response[1][5])
                        file.write(",".join(response[1]))
            if type(response[0]) == list:
                s = ""
                for c in response[0]:
                    s+=str(c)+"\n"
                client_socket.sendall(s.encode())
            else:
                client_socket.sendall(str(response[0]).encode())
        elif query == "print":
            list_of_customers =  bst.get_all_customers()
            if not list_of_customers:
                data = "No customers found."
                client_socket.sendall(data.encode())
            else:
                s = ""
                for customer in list_of_customers:
                    s += str(customer)+"\n"
                client_socket.sendall(s.encode())
        elif query == "quit":
            print (f"client {client_address} quit")
            data = f"client {client_address} quit"
            client_socket.sendall(data.encode())
            break
        else:
            data =f"({query}) is invalid!"
            client_socket.sendall(data.encode())
            
        
        
            
    
    
    

def invalid_line(fields)->tuple:
    if len(fields) != 6 :
        response = "length is other than 6."
        return response , True      # line fields length incorrect
    if not all(field.isalpha() for field in fields[0:2]):
        presponse = "Error, Name invalid"
        return response,True       # name should only include alphabet characters
    if not all(field.isdigit() for field in fields[2:4]):
        presponse = "id or phone is not numeric."
        return response,True       # id and phone should only include digits
    if  len(fields[2]) != 9 or len(fields[3]) != 10:
        response = "Invalid length of id or phone ."
        return response,True       # id should be exactly 9 digits and phone exactly 10
    if not fields[3][0] == "0":
        response = "phone must began with 0."
        return response,True      #phone_num should start with 0
    try:
        fields[4] = float(fields[4])
    except ValueError:
        response = "Error , invalid debt input."
        return response,True 
    try:
        fields[5] = datetime.strptime(fields[5].strip(), "%d/%m/%Y").date()
    except ValueError:
        response = "Invalid input of date format."
        return response , True
    return False , False

def add_customer(csv_line)->tuple:
    id = csv_line[2]
    invalid = invalid_line(csv_line)
    if invalid[1]:
        print(invalid[0])
        return invalid[0] ,False
    customer_to_update = bst_id.find_customer_by_id(id)
    if not customer_to_update[1]:
        customer = Customer(*csv_line)
        bst.add_customer(customer)
        bst_id.add_customer(customer)
        print('customer added.')
        return "customer added .", csv_line
    else:
        response = id_name_match(customer_to_update[0],csv_line[0],csv_line[1])
        if not response[1]:
            return  response
        response = customer_to_update[0].check_and_update_date(csv_line[5])
        if not response[1]:
            return response
        debt = csv_line[4]
        customer_to_update[0].update_phone(csv_line[3])
        bst.remove_customer(customer_to_update[0])
        customer_to_update[0].add_debt(debt)
        bst.add_customer(customer_to_update[0])
        return response[0] ,csv_line
    
def select_name(query):
    if len(query) > 3 :
        response ="invalid input , too many parameters, tip:name=..."
        return  response ,False
    name_index = 5 if not query[2][4] == "!" else 6
    if len(query[2]) < name_index+1:
        response ="No name Entered."
        return response , False  
    if not query[2][name_index:].isalpha():
        response = "invalid type , (not alphabetic)"
        return response , False
    response = bst.find_by_name(query[1],query[2][4],query[2][name_index:])
    if not response[1]:
        response = f"{query[1]} name {query[2][name_index:]} not found"
        return response,False
    return response
    

def select_id(query):
    if len(query) > 2 :
        response= "invalid input , too many parameters, tip:id=... "
        return response, False
    id_index = 3 if not query[1][2] == "!" else 4
    if len(query[1]) != (id_index + 9 )or not query[1][id_index:].isdigit():
        response = "id must be 9 digits."
        return response , False
    if query[1][2] == "=":
        response = bst_id.find_customer_by_id(query[1][id_index:]) 
        return response 
    response = bst.find_by_id(query[1][2],query[1][id_index:])
    if not response[1]:
        return "customer not found." ,False
    return response

def select_phone(query):
    if len(query) > 2 :
        response ="invalid input , too many parameters, tip:phone=... "
        return response ,False
    phone_index = 6 if not query[1][5] == "!" else 7
    if len(query[1]) != (10 + phone_index) or not query[1][phone_index:].isdigit():
        response ="Phone must be 10 digits."
        return response ,False
    response = bst.find_by_phone(query[1][5],query[1][phone_index:])
    if not response[1]:
        response =f"{query[1][phone_index:]} phone number not found"
        return response ,False
    return response

def select_debt(query):
    if query[1][4] == "!":
        try:
            amount = float(query[1][6:])
            return bst.find_by_debt("!=",amount)
        except ValueError:
            response ="invalid input , enter debt amount. "
            return response ,False
    else:
        try:
            amount = float(query[1][5:])
            return bst.find_by_debt(query[1][4],amount)
        except ValueError:
            response ="invalid input , enter debt amount. "
            return response, False

def select_date(query):
    if query[1][4] == "!":
        try:
            date = datetime.strptime(query[1][6:].strip(), "%d/%m/%Y").date()
            return bst.find_by_date(query[1][4:6],date)
        except ValueError:
            response ="Invalid input of date format."
            return  response ,True
    else:
        try:
            date = datetime.strptime(query[1][5:].strip(), "%d/%m/%Y").date()
            return bst.find_by_date(query[1][4],date)
        except ValueError:
            response ="invalid input of date format. "
            return response ,True
    

def select(query):
    operators = ["=","<",">"]
    if len(query) < 2 :
        response ="No parameters given ."
        return response , False
    elif query[1] == "first" or query[1] == "last":
        if len(query) < 3:
            response="nothing entered after 'first'/'last', tip:name=..."
            return response , False
        if not query[2].startswith("name"):
            response = f"{query[2]} is unsupported. "
            return response,False
        if len(query[2]) < 5 or ((not query[2][4] in operators) and (len(query[2]) < 6 or not query[2][4:6] == "!=" )) :
            response ="Enter a valid operator."
            return response , False
        return select_name(query) 
        
    elif query[1].startswith("id"):
        if (len(query[1]) < 3 or ((not query[1][2] in operators)) and (len(query[1]) < 4 or not query[1][2:4] == "!=" )) :
            response= "Enter a valid operator."
            return response , False
        return select_id(query) 
    elif query[1].startswith("phone"):
        return select_phone(query) 
    elif query[1].startswith("debt"):
        if len(query[1]) < 6 or not(query[1][4] in operators or query[1][4:6] == "!=" ) :
            response = "invalid operator."
            return response ,False
        response = select_debt(query)
        if not response[1]:
            return "customer not found",False
        return response
    elif query[1].startswith("date"):
        if len(query[1]) < 6 or not(query[1][4] in operators or query[1][4:6] == "!=" ) :
            response = "invalid operator." 
            return response ,False
        response = select_date(query)
        if not response[1]:
            return "not found!" , False
        return response
    else:
        response =f"{query[1]} is not recognized"
        return response ,False

def keys_valid(line):
    valid_keys =[['set', 'first', 'name='], ['last', 'name='], ['id='], ['phone='], ['debt='], ['date=']]
    if len(valid_keys) > len(line):
        response ="missing fields. "
        return response, False
    if len(valid_keys) < len(line):
        response ="Too many fields. "
        return response , False
    csv_line = []
    for i in range(len(valid_keys)):
        line[i] = line[i].strip().split()
        attr = line[i][-1].split("=")[-1]
        if not attr:
           response =f"{line[i][-1]}missing info. "
           return response,False
        csv_line.append(attr) 
    for i in range(len(line)):
        line[i][-1]=line[i][-1][:(line[i][-1].find(csv_line[i]))]
    if not line == valid_keys:
        response = "invalid line."
        return response,False
    return csv_line ,True

def update(line):
    csv_line = keys_valid(line)
    if not csv_line[1]:
        return csv_line 
    if csv_line:
        response = add_customer(csv_line[0])
        return response
    

def id_name_match(customer:Customer,first,last):
    if customer.first != first or customer.last != last:
        response = f"{customer}  Name doesn't match {first} {last}"
        return response ,False
    return True,True

if len(sys.argv) < 2 :
    print ("Error: missing csv file name.")
    quit()
host = '127.0.0.1'
port = 12345
mutex = Lock()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(20)

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

    client_socket, client_address = server_socket.accept()
    t = Thread(target=handle_connection, args=(client_socket, client_address,mutex))
    t.start()    
    


