Project3
TeamName : anikadharani


Members:

	1) Dharanish	Kedarisetti	001667566

	2) Anika	Ramachandran    001630313

The benchmarks for deciding the “best” TCP variant would be the following:
1)	Throughput: Ratio of total data transferred to the time taken to transfer.
2)	Latency: Roundtrip time for a packet 
3)	Packet Drops: Number of packet loss during transmission

Calculations:

All the graphs are plotted using the same scale so that it is easier to compare the results from different scenarios.
Tabular and Graphical results of the parameters are observed for both the average and standard deviation for each scenario taken into consideration.
T-test is conducted to check the statistical significance of the results.
Standard deviation is calculated to obtain a stable result.


Experiment 1: TCP Performance Under Congestion
Performance of TCP variants (Tahoe, Reno, NewReno, and Vegas) under the influence of various load conditions:
That is to perform tests that analyze the performance of these TCP variants in the presence of Constant Bit Rate (CBR) flow. Record the performance of the TCP flow by changing the CBR's rate until it reaches the bottleneck capacity 


Experiment 2: Fairness between TCP Variants
Conduct experiments to analyze the fairness between different TCP variants. Two variants are compared in the same environment for the distribution of bandwidth with a common CBR. Ideally, each variant should share equal bandwidth, but this is not practical. It varies due to different protocol designs.
As an extension of Experiment 1, here we compare the average throughput, packet loss rate, and latency of each TCP flow as a function of the bandwidth used by the CBR flow to determine the fairness of the protocols to one another.


Experiment 3: Influence of Queuing
Study the influence of the queuing discipline used by nodes on the overall throughput of flows. Packet losses, throughput and latency are affected by queue managements. 
Here, we compare the effect of CBR after the TCP is steady over a certain amount of time and not by varying the bandwidth of CBR as in Experiment 1.
Queue management refers to the algorithms that manage the length of packet queues by dropping packets when necessary or appropriate. 
The following two Queuing disciplines are used study the influence on the overall throughput of flows:
1)	DropTail
2)	Random Early Drop (RED) 


How to Run the project:

********************************************************************
Run the following commands on the terminal before you use the files.
PATH=$PATH:/course/cs4700f12/ns-allinone-2.35/bin
export=PATH
********************************************************************
Files:

Experiments.xls =>All the observed data used in project report

Exp1:
	--> tcp.tcl 
	--> tcpVariant.tcl
	--> tcpVariantCBR.tcl
	--> tcpVariantr.tcl
	--> exp1.py		=> Main scripting file to generate thorughput, packetdrop, latency, use command "python exp1.py target.txt" where target.txt is the output file
	--> all.py		=> run command "python all.py out.tr node1 node2 target.txt" 
				   command to generate throughput, packetdrop and latency between node1 node2 from the trace file out.tr and save it in target.txt file
	--> throughdef.py	=> script to get throughput
	--> Latencydef.py	=> script to get latency
	--> drop.py		=> script to get drop
Exp2 
	--> tcp1.tcl
	--> tcp1VariantVariant.tcl
	--> tcp1VariantVariantCBR.tcl
	--> exp2.py		=> Main scripting file to generate thorughput, packetdrop, latency, 
				use command "python exp1.py target1.txt target2.txt" where target1.txt and target2.txt are the output files
	--> all.py		=> run command "python all.py out.tr 0 3 target.txt" 
				   command to generate throughput, packetdrop and latency between node1 node2 from the trace file out.tr and save it in target.txt file
	--> throughdef.py	=> script to get throughput
	--> Latencydef.py	=> script to get latency
	--> drop.py		=> script to get drop

Exp3
	--> tcp.tcl
	--> tcpVariant.tcl
	--> tcpVariantCBR.tcl
	--> tcpVariantQ.tcl
	--> exp3.py		=> Main scripting file to generate thorughput, packetdrop, latency, 
				use command "python exp1.py target1.txt target2.txt" where target1.txt and target2.txt are the output files
	--> all3.py		
	--> all.py		=> run command "python all.py out.tr 0 3 target.txt" 
				   command to generate throughput, packetdrop and latency between node1 node2 from the trace file out.tr and save it in target.txt file
	--> Throughput.py	=> run command "python thorguput.py out.tr target.txt" to get thoughput at node n4 and n6 where target.txt is output file 
	--> throughdef.py	=> script to get throughput
	--> Latencydef.py	=> script to get latency
	--> drop.py		=> script to get drop
	--> latency.py		=> run command "python latency.py out.tr target.txt" to get latency 
				   for flow between n1 and n4 where the trace file out.tr is used and output is saved in target.txt file

***************************************************************************
To run the first experiment 

1) Make sure that /course/cs4700f12/ns-allinone-2.35/bin/ is added to the PATH variable
2) CD into the folder Exp1
3) python exp1.py target.txt
4) outputs will be printed in target.txt
*************************************************************************
To run the second experiment 
1) Make sure that /course/cs4700f12/ns-allinone-2.35/bin/ is added to the PATH variable
2) CD into the folder Exp2
3) run command "python exp2.py target1.txt target2.txt"
4) outputs will be printed in target1.txt and target2.txt
***********************************************************************
To run the second experiment 
1) Make sure that /course/cs4700f12/ns-allinone-2.35/bin/ is added to the PATH variable
2) CD into the folder Exp3
3) run command "python exp3.py target.txt 
4) outputs will be printed in target.txt
**********************************************************************
