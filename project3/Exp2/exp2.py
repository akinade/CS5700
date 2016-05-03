__author__ = 'dhara'

import sys
import os
import re
#import all
def main(args):
    proto1=['Agent/TCP','Agent/TCP/Reno','Agent/TCP/Newreno','Agent/TCP/Vegas']
    proto2=['Agent/TCP','Agent/TCP/Reno','Agent/TCP/Newreno','Agent/TCP/Vegas']
    cbr=['1','2','3','4','5','6','7','8','9','10']
    for variant1 in proto1:
        with open('tcp1.tcl', 'r') as in_file:
            text = in_file.read()
        with open('tcp1Variant.tcl', 'w') as out_file:
            out_file.write(text.replace('set tcp1 [new Agent/]','set tcp1 [new '+variant1+']'))
        for variant2 in proto2:
#            if variant1!=variant2:
                with open('tcp1Variant.tcl', 'r') as in_file:
                    text = in_file.read()
                with open('tcp1VariantVariant.tcl', 'w') as out_file:
                    out_file.write(text.replace('set tcp2 [new Agent/]','set tcp2 [new '+variant2+']'))
                target1=open(args[1],'a')
                target2=open(args[2],'a')
                line=variant1+' '+variant2
                print line
                target1.write(line)
                target1.write("\n")
                target2.write(line)
                target2.write("\n")

                for rate in cbr:
                    with open('tcp1VariantVariant.tcl', 'r') as in_file:
                        text = in_file.read()
                    with open('tcp1VariantVariantCBR.tcl', 'w') as out_file:
                        out_file.write(text.replace('$cbr1 set rate_ Mb','$cbr1 set rate_ '+rate+'Mb'))

                    bashcommand='ns tcp1VariantVariantCBR.tcl'
                    os.system(bashcommand)

                    line=variant1
                    target1.write(line)
                    target1.write("\n")
                    bashcommand='python all.py my_experimental_output.tr 0 3 target1.txt'
                    os.system(bashcommand)
                    line=variant2
                    target2.write(line)
                    target2.write("\n")
                    bashcommand='python all.py my_experimental_output.tr 4 5 target2.txt'
                    os.system(bashcommand)


if __name__ == "__main__":
    main(sys.argv)

