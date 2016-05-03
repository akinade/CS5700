__author__ = 'dhara'
import sys

def drop(args):
    filename= args[1]
    destination=float(args[3])
    start  = 0
    stop = 0
    granularity=0.5
    drop=0.0
    sent=0.0
    flagstart=0

    file=open(filename)
    for line in file:
        trace= line.split(" ")
        if flagstart==0:
            start=float(trace[1])
            flagstart=1
        else:
            stop=float(trace[1])
        if(trace[0]=='+' and trace[4]=='tcp'and trace[2]=='0'):
            sent=sent+1.0
        if(trace[0]=='d' and trace[4]=='tcp'and float(trace[9])==destination):
            drop=drop+1.0
            #print granularity,drop
    time=stop-start
    return drop/sent

