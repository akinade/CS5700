__author__ = 'dhara'
import sys


def Latency(args):
    filename = args[1]
    sourcenode = args[2]
    destnode = args[3]
    latency = 0
    start_time = {}
    end_time = {}
    packets = []
    nump = 0

    file = open(filename)
    for line in file:
        trace = line.split(" ")
        if (trace[0] == '+' and trace[4] == 'tcp' and trace[2] == sourcenode):
            start_time[trace[-1]] = float(trace[1])
            end_time[trace[-1]]=-1.0
            packets.append(trace[-1])
        elif (trace[0] == 'r' and trace[4] == 'tcp' and trace[3] == destnode):
            end_time[trace[-1]] = float(trace[1])
        elif (trace[0] == 'd' and trace[4] == 'tcp'):
            end_time[trace[-1]] = -1

    for packet in packets:
        if start_time[packet] < end_time[packet]:
            nump = nump + 1
            latency = latency + end_time[packet] - start_time[packet]
    return latency / nump


if __name__ == "__main__":
    main(sys.argv)
