__author__ = 'dhara'
# command line all.py filename.tr sourcenode destinationnode target.txt
import sys
import throughdef
import drop
import Latencydef
def all(args):
    filename= args[1]
    sourcenode=args[2]
    destnode = args[3]
    target=open(args[4],'a')
    throughput=throughdef.throughput(args)
    droprate=drop.drop(args)
    latency=Latencydef.Latency(args)
    line=str(throughput)+"   "+str(droprate)+"    "+str(latency)
    target.write(line)
    target.write("\n")
    print "Throughput:",throughput,"Droprate:",droprate,"Latency:",latency


if __name__ == "__main__":
    all(sys.argv)


