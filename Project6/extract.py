import sys
def main(args):
    filename = args
    file=open(filename)
    #print file.read()
    domains={}
    for line in file:
        #print 'here:',line.split(".")
        domain = line.split('.')[-2]
        domains[domain]=line
    #print domains
    print len(domains.keys())

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print "Error:Incorrect number of Arguments"
    else:
        main(sys.argv[1])
