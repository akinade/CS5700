Project1 



Files:

	1) client	-	ssh script to run the client.py

	2) client.py	-	python v 2.6 file

	3) README.txt


---------------------------------------------------------------

client

------

script file calling client.py using python compiler.
passes the commandlines arguments to the client.py file

---------------------------------------------------------------

client.py

---------


High-level approach:

Our goal was to use Python to code the client to solve mathematical problems that the server sends to it. We also modified the client to support SSL by including an SSL port in the program when the secure connection is implemented (default) unless specified otherwise.

The code uses socket, ssl and sys libraries. It 

contains two fuctions:
	1) compute:
 takes in the values array consisting of input values received from the server
computes to output based on the input

	2) main(args):
 takes the input arguments passed by the initializer and connectes to the server.
server name and the nuid are required on the command line

if port parameter is not chosen, port number '27993' is chosen by default

if -s parameter is passed, the ssh option is chosen the socket is wrapped in the ssh and 
port number '27994' is chosen

if -p parameter is passed, port is set to the port number given on the command line



A HELLO message is then sent to the server, and each time the server replies back the 
message is parsed and checked for a 'STATUS' or a 'BYE' value. 

If 'STATUS' is found the compute() function is called and the solution is computed
and replied back to the server after concatenation

If 'BYE' is found flag is printed and the connection is closed
 




Challenges faced:

Creating a script called client that accepts these parameters and then executes the actual program. The challenge was to call the program without specifying the path of the code. 

Testing:

1.Checked the Socket connection by testing the reception of a STATUS message when the client sends a HELLO message.
2.Tested the function “compute” which solves the mathematical equations given by the server.
3.Checked the termination of the socket connection after BYE and/or ERROR message is received by the client.
4.Checking if SSL works by comparing the flags received on both the ports (i.e SSL and without SSL)
