Project2

TeamName : anikadharani


Members:

	1) Dharanish	Kedarisetti	001667566

	2) Anika	Ramachandran    001630313
Files:

	1) webcrawler-	ssh script to run the topview.py
	2) topview.py-	python v 2.6 file

	3) README - .txt
---
---------------------------------------------------------------

webcrawler
------

script file calling topview.py using python compiler.
passes the commandlines arguments to the topview.py file

---------------------------------------------------------------

topview.py

---------


High-level approach:
Our goal was to use Python to code a web crawler that gathers data from a fake social networking website that has been set up.



The code uses socket, sgml and sys libraries. It 

contains three classes:
	1) crawler: Crawls the webpages avoiding loops to find and print the Secret Flags
	2) MyParser: Parses text files formatted in sgml 
	3) HTTP: Opens the webpage using GET nad POST
	
It 

contains four main functions:
	1)getCookie(reply,cookie): extracts Cookie from the Header
	2)request(address,cookie): hanldes HTTP status Codes
	3)login(args): Logs into the webpage using given credentials 
	4) main(args):
 takes the input arguments passed by the initializer and connectes to the server.
username and password are required on the command line


The program crawls through the pages of Fakebook and prints the secret flags (limited to 5) and the connection is closed
 



Challenges faced:

1.	When returning the list of hyperlinks from the parser the parser was repeating the links which were added causing the program to take a longer time to execute. This was resolved by clearing the cache.
2.	Initially it was assumed that the checking condition for the links to be, weather the link parsed on the current page were already visited but no checking was done to confirm if they have already been added in the unvisited list which was added at a later stage.
3.	To figure out the validation for incorrect user credentials while logging in.

Testing:

1.	Checked the Socket connection.
2.	Checked the reception of Webpage.
3.	Tested Login using Session ID and CSRFtoken with username and password.
4.	Tested the conditions for all probable Status Messages.
5.	Tested the code to avoid infinite loops by adding a visited and unvisited log.
6.	Provided a condition limiting the secret flags to 5 for program execution. 
7.      Error checking for incorrect credentials.
8.	Error checking for incorrect number of arguments on command line.
