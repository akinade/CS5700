__author__ = 'dhara'
import sys
import os
import re
#import all
def main(args):
    proto=['Agent/TCP/Reno','Agent/TCP/Sack1']
    queue=['DropTail','RED']
    for variant in proto:
        with open('tcp2.tcl', 'r') as in_file:
            text = in_file.read()
        with open('tcpVariant.tcl', 'w') as out_file:
            out_file.write(text.replace('Agent/]',variant+']'))
        target=open(args[1],'a')
        line=variant
        print line
        target.write(line)
        target.write("\n")
        target.close()

        for q in queue:
            target=open(args[1],'a')
            print q
            target.write(q)
            target.write("\n")
            with open('tcpVariant.tcl', 'r') as in_file:
                text = in_file.read()
            with open('tcpVariantCBR.tcl', 'w') as out_file:
                out_file.write(text.replace('DropTail',q))
            target.close()

            bashcommand='ns tcpVariantCBR.tcl'
            os.system(bashcommand)
            bashcommand='python all3.py my_experimental_output.tr '+args[1]
            os.system(bashcommand)


if __name__ == "__main__":
    main(sys.argv)

