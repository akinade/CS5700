__author__ = 'dhara'

import socket
from struct import *
from cStringIO import StringIO
import Queue
import threading
import urllib2
import sys


class CDN:
    def __init__(self, file ,port):
        self.replicas=[]
        self.port=int(port)
        inputs=open(file)
        #validin=[line for line in inputs if ".com" in line and "Origin" not in line]
        validin=[line.strip('\r\n') for line in inputs]
        for line in validin:
            self.replicas.append(line)#socket.gethostbyname(line.split()[0]))
        #self.q = Queue.Queue()
    # called by each thread
    def get_url(self, url,ip, ips):
        query = "http://" + url +':'+str(self.port)+"/" + ip
        #query = "http://www.google.com"
        rtt = urllib2.urlopen(query).read()
        ips[float(rtt)]=url
        #self.q.put(rtt)

    def bestrtt(self,ip):
        threads = []
        ips={}
        for u in self.replicas:
            t = threading.Thread(target=self.get_url, args=(u, ip, ips))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        #s = self.q.get()
        #print s
        #print ips, ips[s]
        #while not self.q.empty():
        #    print self.q.get()
        s = min(ips.keys())
        print ips
        return ips[s]

class DNSQuery:
    def __init__(self, data, addr):
        self.data=data
        self.clientIP=str(addr[0])
        print addr[0]
        #unpack query header
        #print data[12:],len(data),type(data)
        id, misc, qdcount, ancount, nscount, arcount = unpack('!6H', data[:12])
        self.isquery= (misc & 0x8000) == 0
        if self.isquery:
            #print 'yes', data[12:],'done'
            #get the first question
            '''
            queries = StringIO(data[12:])
            C = unpack("!c", queries.read(1))[0]
            #print C
            dstart=0
            Domain = []
            while C !='\x00':
                dstart=dstart+1
                N = ord(C)
                dstart=dstart+N
                Domain.append(''.join(queries.read(N)))
                C = unpack("!c", queries.read(1))[0]
            Domain = '.'.join(Domain)
            #Qclass, qtype = unpack("!2H", queries.read())
            self.domain= Domain
            self.domainlength = dstart
            self.qtype= unpack('!H',queries.read(2))[0]
            self.qclass=unpack('!H',queries.read(2))[0]
            print Domain, data[12:12+dstart]
            '''
            index=12
            C = unpack("!c", data[index])[0]
            # print C
            Domain = []
            while C != '\x00':
                N = ord(C)
                index=index+1
                indexend=index+N
                Domain.append(''.join(data[index:indexend]))
                index=indexend
                C = unpack("!c", data[index])[0]
            Domain = '.'.join(Domain)
            self.Qclass, self.qtype = unpack("!2H", data[index:index+4])
            self.domain = Domain
            self.todomainlength = index
            print Domain

    def checkCdn(self, cdn):
        ip=cdn.bestrtt(self.clientIP)
        print ip
        return ip

    def respuesta(self, cdn):
        packet=''
        #ip = socket.inet_aton(self.getip(self.domain))
        ip = socket.inet_aton (self.checkCdn(cdn))
        print ip,len(ip)
        if len(ip)>0:
            packet+=self.data[:2] + "\x81\x80"
            packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
            packet+=self.data[12:self.todomainlength+5]                                         # Original Domain Name Question
            packet+='\xc0\x0c'                                           # Pointer to domain name
            packet+='\x00\x01'                                    # Response type,
            packet+='\x00\x01'                                    # Response class,
            packet+= '\x00\x00\x00\x0F'                                  # ttl
            packet+='\x00\x04'                                          #data length -> 4 bytes
            #packet+= pack('!H',len(ip))
            packet+= ip                        # 4bytes of IP
        else:
            packet=''
        return packet

    def getip(self, data):
        record=open("example.txt",'r').read()
        if data in record:
            for line in record.split('\n'):
                if data==line.split()[0]:
                    #print line.split()[-1]
                    return line.split()[-1]
        else:
            return ""

def handleQuery(udps,data,add,cdn,name):
    query = DNSQuery(data, add)
    if query.domain==name:
    	reply = query.respuesta(cdn)
    	if len(reply) > 0:
        	udps.sendto(reply, add)

def main(args):
    port = 0
    name = ""
    if args[1] == '-p':
        port = int(args[2])
    elif args[3] == '-p':
        port = int(args[4])
    if args[1] == '-n':
        name = args[2]
    elif args[3] == '-n':
        name = args[4]

    #port = 40200 #args[0]
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(("", port))
    file="testme.txt"
    if port == 65535:
        rttPort = 65534
    else:
        rttPort = port + 1
    cdn =  CDN(file,rttPort)
    print "reaching here"
    #data, add = udps.recvfrom(1024)

    while 1:
        try:
            data,add = udps.recvfrom(1024)
            #print "thread is being created even though no data received"
            #print len(data)
            t = threading.Thread(target=handleQuery, args=(udps,data,add,cdn,name))
            t.daemon=True
            t.start()
            """
            reply = DNSQuery(data, add).respuesta(cdn)
            if len(reply)>0:
                udps.sendto(reply,add)
            """
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
  if len(sys.argv)!=5:
      #print sys.argv
      print "Error:Incorrect number of Arguments"
  else:
     main(sys.argv)
