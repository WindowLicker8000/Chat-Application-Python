import socket, time, threading
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = input("What IP do you want to connnect to? ")
host_port = 9999

print("Initiating connection")

def connect_to_host():
    connection_attempt_count = 1
    while True:

        try:
            sock.connect((host_ip, host_port))
            print("Connection Successful")
            break
        except:
            connection_attempt_count += 1
            print("Previous attempt unsuccessful. Initiating attempt number " + str(connection_attempt_count) + ".")
connect_to_host()

def send_input ():
    while True:
        try:
            message = input("")
            b = message.encode('utf-8')
            sock.sendall(b)
        except:
            print("Disconnected from server - Check your connection. The problem may also be on our end.")
            break
send1 = Thread(target=send_input, args=())
send1.daemon = True

def receive_input ():
    while True:
    
        try:
            data = sock.recv(1024)
            if data:
                decoded_data = data.decode('utf-8')
                print(decoded_data)
        except:
            print("Disconnected from server - Check your connection. The problem may also be on our end.")
            break 
receive1 = threading.Thread(target=receive_input, args=())
receive1.daemon = True

receive1.start() 
send1.start()
while True:
    time.sleep(1)