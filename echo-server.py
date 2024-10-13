#!/usr/bin/env python3

import socket
import arguments
import argparse

def operation_request(request):
    try:
        request = request.decode('utf-8')
        arr = request.split()
        if len(arr) != 3:
            return "ERROR Input".encode('utf-8')
        operation = arr[0]
        num1 = int(arr[1])
        num2 = int(arr[2])

        if operation == "add":
            return str(num1 + num2).encode('utf-8') 
        elif operation == "subtract":
            return str(num1 - num2).encode('utf-8')
        elif operation == "multiply":
            return str(num1 * num2).encode('utf-8')
        elif operation == "divide":
            return str(num1 // num2).encode('utf-8')
        else:
            return f"ERROR Operation".encode('utf-8')    
    except Exception as e:
        return f"ERROR: {e}".encode('utf-8')
    
# Run 'python3 echo-server.py --help' to see what these lines do
parser = argparse.ArgumentParser('Starts a server that returns the data sent to it unmodified')
parser.add_argument('--server_IP', help='IP address at which to host the server', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which to host the server', **arguments.server_port_arg)
args = parser.parse_args()

SERVER_IP = args.server_IP  # Address to listen on
SERVER_PORT = args.server_port  # Port to listen on (non-privileged ports are > 1023)

print("server starting - listening for connections at IP", SERVER_IP, "and port", SERVER_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received client message: '{data!r}' [{len(data)} bytes]")
            data = operation_request(data)
            print(f"echoing '{data!r}' back to client")
            conn.sendall(data)

print("server is done!")
