import socket
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = 'Your IP Here'
print("IP of host: ", host_ip, ", host name: ", host_name)
port = 9999
sock_address = (host_ip, port)
sock.bind(sock_address)
client_dict = {}
client_list = []

client_sock = ""

def send_input (client = client_sock, client_list = client_list):

    while True:
        message = "Server >  " + input("")
        b = message.encode('utf-8')

        for i in client_list:
            i.sendall(b)


send1 = Thread(target=send_input, args=())
send1.daemon = True

def command(command, client):
    message = ""
    split_command = command.split()
    if command == "/help":
        message = "Command list. Work in progress."
    elif split_command[0] == "/username":
        message = "Name changed."
        client_dict[client] = split_command[1]

    if message:
        client.sendall(message.encode('utf-8'))
    

def receive_input ():
    data = ""
    while True:
        for i in client_list:
            if i:
                try:
                    data = i.recv(1024)
                except:
                    print( str(client_dict[i]) + " left the chat.")
                    client_list.remove(i)
                    del client_dict[i]
            if (data) and (client_dict):
                decoded_data = data.decode('utf-8')
                print(str(client_dict[i]) + " >  " + decoded_data)
                if (decoded_data[0] == "/"):
                    command(decoded_data, i)
                else:
                    
                    data_to_send = str(client_dict[i]) + " >  " + decoded_data
                    data_to_send_encoded = data_to_send.encode('utf-8')
                    for i in client_list:
                        i.sendall(data_to_send_encoded)
receive1 = Thread(target=receive_input, args=())

print('Socket Successfully Bound')

sock.listen(10)

count = 0
while True:

    sock.listen(10)     

    client_sock, address = sock.accept()
    client_dict[client_sock] = address[0]
    client_list.append(client_sock)
    print("Client " + str(address[0]) + " connected.")
    if count == 0:
        receive1.start()
        send1.start()
    count += 1


##Handle server and individual thread termination