# CSC 249 – Project 2 – Simple VPN

## Overview of Application
The project implements a VPN server to perform +,-,* and / basic mathematical operations. The VPN act like a intermediary between the client and the server. The client takes user input from command line, sending message to the VPN. In the VPN, it takes the request from the client, parse the input message, forward to the actual server and returns the result. The server processes the operation with sent data and send the result back. The communications are performed over TCP.

## Client->VPN Server Message Format
The client sends a message to the VPN containing both the server address and the operation request. The supported operations are: add, subtract, multiply, and divide. All of the mathematical operations are self-explanatory. The client message will be encoded as a UTF-8 string and sent over to the VPN as bytes. When the input is not supported, error message will be returned.

Message is sent in the form of:

<server_IP>:<server_port> <operation> <operand1> <operand2>

"Error Input" if the VPN is failed to parse the input message from client.

## VPN Server->Client Message Format
The VPN forward the client’s message to the server, and wait for server's response to get back to the client. The server responds to the client with either a result or an error message. If the request is valid and the operation proceeds, the server sends the result as a string. If the request is not supported or the server cannot process it, the server sends back an error message. 

Error messages are performed in the format of:

"ERROR Input" if the request format does not match the operation, num1, num2 structure.

"ERROR Operation" if the client specifies an unsupported operation.

"ERROR: invalid literal for int() with base 10: '{num1}' " if the numbers provided are not integers.

## Example Output 1

client input: 

--message add 1 2

VPN input:

Received client message: '127.0.0.1:65432 add 1 2'

VPN output:

Received response from server: '3'

response output:

Received response: '3' [1 bytes]

### Client Trace

python3 client.py --message add 1 2

client starting - connecting to VPN at IP 127.0.0.1 and port 55554

connection established, sending message '127.0.0.1:65432 add 1 2'

message sent, waiting for reply

Received response: '3' [1 bytes]

client is done!

### VPN Trace

python3 VPN.py

VPN starting - listening for connections at IP 127.0.0.1 and port 55554

Connected established with ('127.0.0.1', 58941)

Connection established with ('127.0.0.1', 58941)

Received client message: '127.0.0.1:65432 add 1 2'

Forwarding add 1 2 to server at 127.0.0.1:65432

Received response from server: '3'

VPN is done!

### Server Trace

echo-server.py

server starting - listening for connections at IP 127.0.0.1 and port 65432

Connected established with ('127.0.0.1', 58942)

Received client message: 'b'add 1 2'' [7 bytes]

echoing 'b'3'' back to client

server is done!

## Example Output 2

client input: 

--message subtract 3 1

VPN input:

Received client message: '127.0.0.1:65432 subtract 3 1'

VPN output:

Received response from server: '2'

response output:

Received response: '2' [1 bytes]

### Client Trace
python3 client.py --message subtract 3 1

client starting - connecting to VPN at IP 127.0.0.1 and port 55554

connection established, sending message '127.0.0.1:65432 subtract 3 1'

message sent, waiting for reply

Received response: '2' [1 bytes]

client is done!

### VPN Trace

python3 VPN.py

VPN starting - listening for connections at IP 127.0.0.1 and port 55554

Connected established with ('127.0.0.1', 60109)

Connection established with ('127.0.0.1', 60109)

Received client message: '127.0.0.1:65432 subtract 3 1'

Forwarding subtract 3 1 to server at 127.0.0.1:65432

Received response from server: '2'

VPN is done!

### Server Trace

echo-server.py

server starting - listening for connections at IP 127.0.0.1 and port 65432

Connected established with ('127.0.0.1', 60110)

Received client message: 'b'subtract 3 1'' [12 bytes]

echoing 'b'2'' back to client

server is done!

## how the network layers are interacting when you run your server, VPN server, and client
When running the server, VPN server, and client:

1. The client establishes a TCP connection to the VPN server at the specified IP and port. 
2. The VPN parses the client's message to extract the server's IP and port. It then establishes a new TCP connection to the server and forwards the operation request.
3. The server receives the operation request, performs the mathematic operation, and sends the result back to the VPN.
4. The VPN receives the result from the server and sends it back to the client over the original connection.
5. The client prints the result received from the VPN.

## Acknowledgments
This client-vpn-server system was built based on CSC249 Project1 provided starter code(https://github.com/abpw/csc-249-p2-simple-VPN-server.git). The Python socket library was used to handle TCP communication between client and server. The Python argparse and arguments libraries are used for parsing command-line arguments and for identifies IP addresses and ports.