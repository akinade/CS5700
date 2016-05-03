__author__ = 'dhara'
import sys
import os
import re
#import all
def main(args):
    proto=['Agent/TCP','Agent/TCP/Reno','Agent/TCP/Newreno','Agent/TCP/Vegas']
    cbr=['1','2','3','4','5','6','7','8','9','10']
    cbrs=['0.7']#['0.3','0.6','0.9','1.2','1.5','1.8','2.1','2.4','2.7','3.0']#['0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1','1.1','1.2']
    for variant in proto:
        with open('tcp.tcl', 'r') as in_file:
            text = in_file.read()
        with open('tcpVariant.tcl', 'w') as out_file:
            out_file.write(text.replace('Agent/]',variant+']'))
        target=open(args[1],'a')
        line=variant
        print line
        target.write(line)
        target.write("\n")
        target.close()

        for start in cbrs:
            target=open(args[1],'a')
            with open('tcpVariant.tcl', 'r') as in_file:
                text = in_file.read()
            with open('tcpVariantr.tcl', 'w') as out_file:
                temp='$ns at '+start+' "$ftp start"'
                out_file.write(text.replace('$ns at 0.7 "$ftp start"',temp))
            #print start
            #target.write(start)
            #target.write("\n")
            target.close()

            for rate in cbr:
                with open('tcpVariantr.tcl', 'r') as in_file:
                    text = in_file.read()
                with open('tcpVariantCBR.tcl', 'w') as out_file:
                    out_file.write(text.replace('$cbr1 set rate_ Mb','$cbr1 set rate_ '+rate+'Mb'))

                bashcommand='ns tcpVariantCBR.tcl'
                os.system(bashcommand)
                bashcommand='python all.py my_experimental_output.tr 0 3 target.txt'
                os.system(bashcommand)

if __name__ == "__main__":
    main(sys.argv)

