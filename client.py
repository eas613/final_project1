import sys 
import socket

if len(sys.argv) < 3:
    print ("Error: missing host /& port.")
    quit()

host ,port = sys.argv[1],int(sys.argv[2])


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))

# Send data to the server
while True:
    message = input("==> ")
    client_socket.sendall(message.encode('utf-8'))

    # Receive the echoed data from the server
    data = client_socket.recv(1024)
    print(f"Received: {data.decode('utf-8')}")



        
