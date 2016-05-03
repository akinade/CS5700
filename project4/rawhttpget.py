__author__ = 'dhara'
#import socket
import rawsock
import sys



def main(args):
    webaddress = args[0]
    index=False
    if webaddress[-1]=='/':
	index=True
    webaddress=webaddress.split('/')
    hostname=webaddress[2]
    if index:
	webaddress[3:]=''
    address='/'+'/'.join(webaddress[3:])
    soc=rawsock.rawsocket()
    soc.connect((hostname,80))
    message ="GET "+address+" HTTP/1.0\nHost: "+hostname+"\n\n"
    soc.sendmessage(message)
    #print message
    reply = soc.recv(2048)
    
    while 1:
        temp=soc.recv(65000)
        if len(temp)!=0:
            reply=reply+temp
	else:
            break
    soc.close()

    header = reply.split("\n\n")[0].strip("\n\r").split("\r\n")
    status=int(header[0].split(" ")[1])																																													
    if int(status) is 200:
	
	if index:
		var =open('index.html','w')
	else:
		var =open(webaddress[-1],'w')
	reply1=reply.replace(reply.split("\r\n\r\n")[0]+'\r\n\r\n','')
        var.write("".join(reply1))#.split("\r\n\r\n")[1:]).strip("\n\r"))
    else :
        print("Error: Status returned"+str(status))
    


if __name__ == "__main__":
  if len(sys.argv)!=2:
      print sys.argv
      print "Error:Incorrect number of Arguments"
  else:
     main(sys.argv[1:])

