__author__ = 'dhara'
import sys


def Latency(args):
    filename = args[1]
    sourcenode = '0'#args[2]
    destnode = '3'#args[3]
    latency = 0
    start_time = {}
    end_time = {}
    packets = []
    nump = 0
    granularity=1

    file = open(filename)
    target = open(args[2],'a')
    for line in file:
        trace = line.split(" ")
        if (trace[0] == '+' and trace[4] == 'tcp' and trace[2] == sourcenode):
            start_time[trace[-1]] = float(trace[1])
            end_time[trace[-1]] = -1
            packets.append(trace[-1])
        elif (trace[0] == 'r' and trace[4] == 'tcp' and trace[3] == destnode):
            end_time[trace[-1]] = float(trace[1])
        elif (trace[0] == 'd' and trace[4] == 'tcp' and float(trace[9])==float(destnode)):
            end_time[trace[-1]] = -1
        if granularity<float(trace[1]):
            granularity=granularity+1
            for packet in packets:
                if start_time[packet] < end_time[packet]:
                    nump = nump + 1
                    latency = latency+end_time[packet] - start_time[packet]
            target.write(str(granularity)+"    "+str(latency/nump))
            target.write('\n')
            latency = 0
            start_time = {}
            end_time = {}
            packets = []
            nump = 0


if __name__ == "__main__":
    main(sys.argv)
