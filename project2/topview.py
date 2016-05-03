__author__ = 'dhara'
import socket
import sgmllib
import sys
import time


class MyParser(sgmllib.SGMLParser):
    "A simple parser class child class of the SGML parser."
    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
        self.secretflags=[]
        self.secretfound=False

    def start_a(self, attributes):
        "Function to do when a tag starts"
        for name,value in attributes:
            if name == "href" and "/fakebook" in value:
                if (value) not in self.hyperlinks:
                    self.hyperlinks.append(value)
    def start_h2(self,attributes):
        "Function to do when an h2 tag starts"
        for name,value in attributes:
            if name == "class" and "secret_flag" in value:
                self.secretfound=True

    def handle_data(self, data):
        "Function to work on the data when a tag starts"
        if self.secretfound:
            data= data.split(" ")[1]
            print data
            self.secretflags.append(data)

    def end_h2(self):
        "Function to do when h2 tag ends"
        if self.secretfound:
           self.secretfound=False


    def get_flags(self):
        "Returns secret flags from the parser class"
        return self.secretflags

    def get_hyperlinks(self):
        "Returns hyperlinks on the last page parsed"
        hyperlinks = self.hyperlinks
        self.hyperlinks=[]
        return hyperlinks

class HTTP:
    "docstring for HTTP"
    def __init__(self):
        "Initialise HTTP class object to have a proper hostname and port to 80 for HTTP"
        self.hostname = "cs5700sp16.ccs.neu.edu"
        self.port=80

    def get(self, address,cookie):
        "Get request to the host"
        tempsoc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc =tempsoc
        try:
            soc.connect((self.hostname,self.port))
            message ="GET "+address+" HTTP/1.0\nHost: cs5700sp16.ccs.neu.edu\n\n"
            if len(cookie) >0 :
                message ="GET "+address+" HTTP/1.0\nHost: cs5700sp16.ccs.neu.edu\nCookie: csrftoken="+cookie["csrftoken"]+"; sessionid="+cookie["sessionid"]+"\n\n"
            soc.send(message)
            reply = soc.recv(4098)
            soc.close()
            return reply
        except socket.error,exc:
            assert ("Error : Socket connection %s" % exc)

    def post(self,request):
        "post request to host"
        tempsoc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc =tempsoc
        try: 
            soc.connect((self.hostname,self.port))
            soc.send(request)
            reply = soc.recv(4098)
            soc.close()
            return reply
        except socket.error,exc:
	    assert ("Error: Socket connection %s" % exc)

def getCookie(reply,cookie):
    "to parse the given html file and return the cookie"
    header = reply.split("\n\n")[0].strip("\n\r").split("\r\n")
    cookielines = [line for line in header[1:] if "Set-Cookie" in line]
    cookielms = [line.split(" ")[1].strip(";") for line in cookielines]
    for line in cookielms:
        cookie[line.split("=")[0]]=line.split("=")[1]
    return cookie

def request(address,cookie):
    "function to form and send a request to a hostname"
    http =HTTP()
    response=http.get(address,cookie)
    header = response.split("\n\n")[0].strip("\n\r").split("\r\n")
    status=int(header[0].split(" ")[1])
    if 200<= status < 300:
        return response
    elif 300<= status < 400:
        header = response.split("\n\n")[0].strip("\n\r").split("\r\n")
        redirectlocations = [line for line in header[1:] if "Location" in line]
        redirectlocation = redirectlocations[0]
        addr= redirectlocation.split(" ")[1].strip("http://cs5700sp16.ccs.neu.edu")
        return request(addr,cookie)
    elif 400<= status < 500:
        return ""
    elif 500<= status < 600:
        return request(address,cookie)
    else:
        print "invalid response code received"

def login(args):
    cookie={}
    address="/accounts/login/?next=/fakebook/"
    response = request(address,cookie)
    cookie= getCookie(response,cookie)
    body="username="+args[1]+"&password="+args[2]+"&csrfmiddlewaretoken="+cookie["csrftoken"]
    header ='POST /accounts/login/ HTTP/1.1\nHost: cs5700sp16.ccs.neu.edu\nContent-Length: '+str(len(body))+'\nCookie: csrftoken='+cookie["csrftoken"]+'; sessionid='+cookie["sessionid"]+'384284964b8d50a19c3416ba457c1f87'
    requestmessage=header+"\n\n"+body
    http =HTTP()
    response=http.post(requestmessage)
    header = response.split("\n\n")[0].strip("\n\r").split("\r\n")
    responsecode=int(header[0].split(" ")[1])
    return [getCookie(response,cookie),responsecode]

class Crawler:
    def __init__(self,cookie):
        "initialising crawler with root node at /fakebook"
        self.cookie=cookie
        root="/fakebook/"
        self.visted=[]
        self.unvisited=[root]
        self.flags=[]
        self.parser = MyParser()

    def crawl(self):
        "Crawler function using the dijkstra's algoritm"
        while(len(self.unvisited)>0 and len(self.flags)<5):
            url= self.unvisited.pop(0)
            if url in self.visted:
                continue
            self.visted.append(url)
            page=request(url,self.cookie)
            self.parser.parse(page)
            links = self.parser.get_hyperlinks()
            self.flags= self.parser.get_flags()
            for link in links:
                if link in self.visted or link in self.unvisited:
                    continue
                self.unvisited.append(link)

        return self.flags


def main(args):
    [cookie,responsecode]=login(args)
    if responsecode == 302:
        crawler=Crawler(cookie)
        flags=crawler.crawl()
    else:
        print "Error: Invalid credentials"

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print "Error:Incorrect number of Arguments"
    else:
        t = time.time()
        main(sys.argv)
        elapsed = time.time() - t
     
