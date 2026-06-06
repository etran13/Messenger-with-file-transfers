import sys
import socket
import threading
import os

def accept_connection(portNum):
    "For server setup: Accepts and returns a connection object"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initialServer:
        initialServer.bind(("10.56.2.249", portNum))
        initialServer.listen()
        conn, addr = initialServer.accept() 
        return conn

def make_connection(portNum):
    "For client setup: Returns a connection object given a port number"
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("10.56.2.249", portNum)) 
    return conn

#Access command line arguments
arguments = sys.argv[1:]
arg_dict = {}
for i in range(0, len(arguments), 2):
    arg_dict[arguments[i]] = arguments[i + 1]

if len(arg_dict) == 1:
    #Do server setup
    port_number = arg_dict["-l"]

    #Make and accept connection for messages m and files f
    m_conn = accept_connection(arg_dict["-l"])
    f_conn = accept_connection(arg_dict["-l"])
    print("Server: made")
else:
    m_conn = make_connection(arg_dict["-l"])
    f_conn = make_connection(arg_dict["-l"])
    print("Client: made")

print(arg_dict)