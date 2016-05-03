__author__ = 'dhara'

import sys
import throughput
import latency
def all3(args):
    throughput.throughput(args)
    latency.Latency(args)


if __name__ == "__main__":
    all3(sys.argv)