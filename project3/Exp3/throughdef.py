__author__ = 'dhara'
import sys

def throughput(args):
    filename= args[1]
    destnode = args[3]
    sum =0
    flagstart=0
    start=0
    stop=0

    file=open(filename)
    for line in file:
        trace= line.split(" ")
        if trace[2]==destnode and trace[4]=='ack':
            if flagstart==0:
                start=float(trace[1])
                stop=start
                flagstart=1
            else:
                stop=float(trace[1])

        if 'r'==trace[0] and trace[3]==destnode:
            sum=sum+float(trace[5])
    time=stop-start
    throughput=0.000008*sum/time
    return throughput
