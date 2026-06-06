import sys
import socket
from threading import Thread
import os
from queue import Queue

# =============================================================================
# Thread classes
# =============================================================================
class MessageSender(Thread):
    """
    Worker thread with access to the message queue and message socket. When
    a new message is added to the queue, it will be sent.
    """
    def __init__(self, sock, queue):
        print("Sender init")
        Thread.__init__(self)
        self.sock = sock
        self.queue = queue

    def run(self):
        print("Send started")
        while True:
            message = self.queue.get() 
            socket.sendall(message.encode())
            print("Message sent")

class MessageReciever(Thread):
    """
    Worker thread that is responsible for recieving messages and printing
    them to the screen.
    """
    def __init__(self, sock):
        print("Recver init")
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        print("Recv started", flush=True)
        while True:
            print("Recv looping")
            data = socket.recv(1024)
            print(f"Recieved: {data.decode()}")

class FileSender(Thread):
    pass

class FileReceiver(Thread):
    pass


# =============================================================================
# Helper functions
# =============================================================================

def accept_connection(portNum):
    """For server setup: Accepts and returns two connection objects:
    one for messages and one for files"""
    print("accept_connection")
    port_int = int(portNum)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initialServer:
        initialServer.bind(("10.56.2.249", port_int))
        initialServer.listen()
        message_conn, addr = initialServer.accept() 
        file_conn, addr = initialServer.accept() 
        return (message_conn, file_conn)

def make_connection(portNum):
    "For client setup: Returns a connection object given a port number"
    print("make_connection")
    port_int = int(portNum)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("10.56.2.249", port_int)) 
    return conn

def printInterface():
    "Prints the dialog for the user"
    print("Enter an option ('m', 'f', 'x'):")
    print("  (M)essage (send)")
    print("  (F)ile (request)")
    print(" e(X)it")

# =============================================================================
# Main program
# =============================================================================

#Access command line arguments
arguments = sys.argv[1:]
arg_dict = {}
for i in range(0, len(arguments), 2):
    arg_dict[arguments[i]] = arguments[i + 1]

if len(arg_dict) == 1:
    #Do server setup
    port_number = arg_dict["-l"]
    m_conn, f_conn = accept_connection(arg_dict["-l"])
    print("Server: made")
else:
    #Do client setup
    m_conn = make_connection(arg_dict["-l"])
    f_conn = make_connection(arg_dict["-l"])
    print("Client: made")

#Instantiate queues for messages and files
m_queue = Queue()
f_queue = Queue()

#Create and start sending and recieving threads
m_recv = MessageReciever(m_conn)
m_recv.start()

f_recv = None

m_send = MessageSender(m_conn, m_queue)
m_send.start()

f_send = None

#Start main dialog loop
while True:
    #Get input
    printInterface()
    choice = input("")

    #Handle subsequent input
    if choice == "m":
        message = input("Enter your message: ")
        m_queue.put(message)
    elif choice == "f":
        filename = input("Which file do you want? ")
        f_queue.put(filename)
    elif choice == "x":
        os._exit(0)

print(arg_dict)