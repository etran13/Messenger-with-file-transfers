import sys
import socket
import threading
import os

#Access command line arguments
arguments = sys.argv[1:]
arg_dict = {}
for i in range(0, len(arguments), 2):
    arg_dict[arguments[i]] = arguments[i + 1]

if len(arg_dict) == 1:
    #Do server setup
    port_number = arg_dict["-l"]
else:
    #Do client setup
    pass

print(arg_dict)