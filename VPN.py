#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)

def parse_message(message):
    try:
        header, actual_message = message.split(' ', 1)
        VPN_IP, VPN_PORT = header.split(':')
        VPN_PORT = int(VPN_PORT)
        return VPN_IP, VPN_PORT, actual_message
    except Exception as e:
        print("Error Input")
        return None, None, None
    
print("VPN starting - listening for connections at IP", VPN_IP, "and port", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((VPN_IP, VPN_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            message = conn.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Connection established with {addr}")
            print(f"Received client message: '{message}'")
            SERVER_IP, SERVER_PORT, MESSAGE = parse_message(message)
            if SERVER_IP is None:
                error_msg = "Error Message"
                print(error_msg)
                conn.sendall(error_msg.encode('utf-8'))
            else:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vpn:
                        vpn.connect((SERVER_IP, SERVER_PORT))
                        print(f"Forwarding {MESSAGE} to server at {SERVER_IP}:{SERVER_PORT}")
                        vpn.sendall(MESSAGE.encode('utf-8'))
                        server_response = vpn.recv(1024).decode("utf-8")
                        print(f"Received response from server: '{server_response}'")
                        conn.sendall(server_response.encode('utf-8'))
                except Exception as e:
                    conn.sendall("Error Connection")
print("VPN is done!")




### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.