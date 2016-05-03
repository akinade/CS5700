import os
import subprocess
import sys
import threading
import socket
import hashlib
import httplib
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn

def memCheck(cache):
    while True:
        if int(sum(os.path.getsize(f) for f in os.listdir('./content') if os.path.isfile(f))) > 999000 :
            leasthits = min(cache.values())
            for file, hits in cache.iteritems():
                if hits == leasthits:
                    del cache[file]
                    name = "./content/" +file
                    os.remove(name)

# Base HTTP server muti threaded running at described input port
class RequestHandler(BaseHTTPRequestHandler):
    origin = None
    cache=None
    port=None

class HTTPHandler(RequestHandler):

    def do_GET(self):
        rootdir = "content/"  # current dir
        filename= hashlib.md5(self.path).hexdigest()
        if filename in self.cache.keys() :
            try:
                f = open(rootdir +filename)
                self.send_response(200)
                #self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                self.cache[filename]= self.cache.get(filename,0)+1
            #    self.cache.insert(0, self.cache.pop(self.cache.index(filename)))
            except IOError:
                self.send_error(404, 'File not found')
        else:
            #query="http://www."+self.origin+"/"+self.path
            conn=httplib.HTTPConnection(self.origin,8080)
            conn.debuglevel=1
            conn.request("GET",self.path,headers={'User-Agent':'Python httplib'})
            reply=conn.getresponse()
            if reply.status == 200:
                content = reply.read()
                self.send_response(200)
                #self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content)
                self.cache[filename] = self.cache.get(filename, 0) + 1
                f = open('./'+rootdir+filename, 'w+')
                # content.replace(self.origin+":8080",socket.gethostname()+":"+str(self.port))
                f.write(content)
                f.close()
            elif reply.status == 302:
                temp=self.origin+':8080'
                redirect=reply.getheader('location').split(temp)[-1]
                print "this is the redirect", redirect
                conn = httplib.HTTPConnection(self.origin, 8080)
                conn.request("GET",redirect,headers={'User-Agent':'Python httplib'})
                reply=conn.getresponse()
                self.send_response(200)
                self.end_headers()
                content = reply.read()
                print "this is the  content:",content
                self.wfile.write(content)
                #self.cache.insert(0, filename)
            elif reply.status == 301:
                temp=self.origin+':8080'
                redirect=reply.getheader('location').split(temp)[-1]
                print "this is the redirect", redirect
                conn = httplib.HTTPConnection(self.origin, 8080)
                conn.request("GET",redirect,headers={'User-Agent':'Python httplib'})
                reply=conn.getresponse()
                self.send_response(200)
                self.end_headers()
                f = open(rootdir + filename, 'w+')
                content = reply.read()
                print "this is the  content:",content
                f.write(content)
                self.wfile.write(content)
                self.cache[filename] = self.cache.get(filename, 0) + 1
                #self.cache.insert(0, filename)
                f.close()
            else :
                content = reply.read()
                #content.replace(self.origin+":8080",socket.gethostname()+":"+self.port)
                self.send_response(reply.status)
                #self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content)

class Server(HTTPServer):
    def serve_forever(self, origin, cache , port):
        self.RequestHandlerClass.origin = origin
        self.RequestHandlerClass.cache = cache
        self.RequestHandlerClass.port = port
        HTTPServer.serve_forever(self)

class ThreadedServer(ThreadingMixIn,Server):
    "handling requests in a seperate thread"

def runServer(PortNumber,Origin, cache):
    #myServer = Server(('', PortNumber), HTTPHandler)
    myServer = ThreadedServer(('', PortNumber), HTTPHandler)
    print 'Started httpserver on port ', PortNumber
    try:
        myServer.serve_forever(Origin, cache, PortNumber)
    except KeyboardInterrupt:
        Server.server_close()

# RTT Sever running muti threaded running at described input port +/- 1
class RTThandler(RequestHandler):

    def do_GET(self):
        host = self.path.strip('/')
        request= "ping -c 1 -i 1 " + host + " | grep rtt"
        response = subprocess.check_output(request, shell=True)
        #response = os.system("ping -c 1 -i 1 " + host + " | grep rtt")
        rtt = response.split()[-2].split("/")[1]
        print rtt
        self.send_response(200)
        self.end_headers()
        self.wfile.write(rtt)

class RTTServer(HTTPServer):
    def serve_forever(self, PortNumber):
        self.RequestHandlerClass.port=PortNumber
        HTTPServer.serve_forever(self)

class ThreadedRTT(ThreadingMixIn,RTTServer):
    "handling rtt requestes in sep threads"

def rttCheck(PortNumber):
    #myServer = RTTServer(('', PortNumber), RTThandler)
    myServer = ThreadedRTT(('', PortNumber), RTThandler)
    try:
        myServer.serve_forever(PortNumber)
    except KeyboardInterrupt:
        Server.server_close()

def main(args):
    PortNumber = 0
    Origin = ""
    cache={}
    if args[1] == '-p':
        PortNumber = int(args[2])
    elif args[3] == '-p':
        PortNumber = int(args[4])
    if args[1] == '-o':
        Origin = args[2]
    elif args[3] == '-o':
        Origin = args[4]

    if PortNumber == 65535:
        rttPort = 65534
    else:
        rttPort = PortNumber + 1
    try:
        t1 = threading.Thread(target=runServer,args=(PortNumber,Origin ,cache))
        t2 = threading.Thread(target=rttCheck ,args=(rttPort,))
        t3 = threading.Thread(target=memCheck , args=(cache,))
        t1.daemon=True
        t2.daemon=True
        t3.daemon=True
        #t1.start()
        t2.start()
        t3.start()
        #runServer(PortNumber,Origin,cache)
        #while t2.isAlive():
        #    print 'is alive'

        #print rttPort
        #rttCheck(rttPort)
        runServer(PortNumber,Origin,cache)
        while 1:
		t1.join()
	        t2.join()
        	t3.join()
		#runServer(PortNumber,Origin,cache)

    except (KeyboardInterrupt,SystemExit):
        t1.join()
        t2.join()
        t3.join()

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print "Error:Incorrect number of Arguments"
    else:
        main(sys.argv)
