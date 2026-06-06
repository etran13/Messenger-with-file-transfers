import sys
import socket
from threading import Thread
import os
from queue import Queue
import struct

# =============================================================================
# Thread classes
# =============================================================================
class MessageSender(Thread):
    """
    Worker thread with access to the message queue and message socket. When
    a new message is added to the queue, it will be sent.
    """
    def __init__(self, sock, queue):
        #print("Sender init")
        Thread.__init__(self)
        self.sock = sock
        self.queue = queue

    def run(self):
        #print("Send started")
        while True:
            message = self.queue.get() 
            self.sock.sendall(message.encode())
            #print("Message sent")

class MessageReciever(Thread):
    """
    Worker thread that is responsible for recieving messages and printing
    them to the screen.
    """
    def __init__(self, sock):
        #print("Recver init")
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        #print("Recv started", flush=True)
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.sock.close()
                os._exit(0)
            print(f"Recieved: {data.decode()}")

class FileSender(Thread):
    """
    Worker thread with access to the file queue and file socket. When
    a filename is added to the queue, the thread will locate the file
    and send it.
    """
    def __init__(self, sock, queue):
        #print("Sender init")
        Thread.__init__(self)
        self.sock = sock
        self.queue = queue

    def run(self):
        #print("Send started")
        while True:
            filename = self.queue.get()
            self.sock.sendall(filename.encode())
            self.send_file(filename)

    def send_file(self, filename):
        """
        Given a filename, check if the file exists and send it over
        the socket if it does. If the file does not exist, fail silently.
        """
        try:
            file_stat= os.stat(filename)
            if file_stat.st_size:
                file = open(self.file_name, 'rb')
                while True:
                    print("Sending file...")
                    file_bytes= file.read( 1024 )
                    if file_bytes:
                        self.sock.send(file_bytes)
                    else:
                        print("Done sending")
                        self.sock.send("".encode())
                        break
                file.close()
        except:
            print("File sending encountered an error")
            return

class FileReceiver(Thread):
    """
    Worker thread responsible for recieving file bytes and writing
    them into a file.
    """
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            filename = self.sock.recv
            file = open(filename, 'wb')
            while True:
                print("Recieving file...")
                file_bytes= self.sock.recv(1024)
                if file_bytes:
                    file.write(file_bytes)
                else:
                    print("Done recieving")
                    break
            file.close()


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
        m_conn.close()
        f_conn.close()
        os._exit(0)

print(arg_dict)