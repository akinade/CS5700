__author__ = 'dhara'
import sys

def throughput(args):
    filename= args[1]
    Tsum =0
    Csum=0
    granularity=1
    thruT=[]
    thruC=[]

    file=open(filename)
    target=open(args[2],'a')
    for line in file:
        trace= line.split(" ")
        if 'r'==trace[0] and trace[3]=='3':
            Tsum=Tsum+float(trace[5])
        if 'r'==trace[0] and trace[3]=='5':
            Csum=Csum+float(trace[5])
        if granularity<float(trace[1]):
            line=str(granularity)+' '+str(0.000008*Tsum/1)+"  "+str(0.000008*Csum/1)+"\n"
            thruT.append(line)
            target.write(line)
            print line
            granularity=granularity+1
            Tsum=0
            Csum=0


if __name__ == "__main__":
    throughput(sys.argv)

