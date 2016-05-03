import socket
import sys
import ssl

"""
function to compute the inputs received from the server.
can compute addition(+), subtraction(-), multiplication(*) and division(/)
and will throw an error if some other fuction is called
"""
def compute(values):
    if(values[3] is '+'):
	message = int(values[2])+int(values[4])        
    elif(values[3] is '-'):
	message = int(values[2])-int(values[4])
    elif(values[3] is '*'):
	message = int(values[2])*int(values[4])
    elif(values[3] is '/'):
	message = int(values[2])/int(values[4])
    else:
        assert 'error'
    return message


def main(args):
#initializing valiable
    port =27993		 #default port number
    hostname='cs5700sp16.ccs.neu.edu'
    nuid='001667566'
#assigning variables the values from the input function
    hostname = args[-2]
    nuid= args[-1]
#initializing sockets
    tempsoc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc =tempsoc
#wrapping the socket with an ssl if '-s' parameter is passed
    if '-s' in args:
        port=27994	#defualt port number for ssl
        soc=ssl.wrap_socket(tempsoc,cert_reqs=ssl.CERT_NONE,ca_certs=None)
#assigning the port number value if '-p' parameter is passed
    if '-p' in args:
        port= int(args[args.index('-p')+1])

    soc.connect((hostname,port))
    message ="cs5700spring2016 HELLO "+nuid+"\n"
    soc.send(message)
    reply = soc.recv(256)
    values = reply.split()
    #print reply
    #print values[1]
# checking the status and replying the computed values   
    while(len(values)>0):
        if(values[1] == 'STATUS' ):
	    message ="cs5700spring2016 "+str(compute(values))+" \n"
            #print message
	    soc.send(message)
	    reply = soc.recv(1024)
            #print reply
            values = reply.split()
# if the status from the server is 'BYE' closing the connection
	elif(values[2] == 'BYE'):
            print values[1]
            soc.close()
            break
# cosing the connection in case of any error
	else:
            soc.close()
            #	    print reply
            raise "Error received"
    
#python initializer
if __name__ == "__main__":
    main(sys.argv)
