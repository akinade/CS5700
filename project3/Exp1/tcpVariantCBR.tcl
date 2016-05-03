set ns [new Simulator]

set f [open my_experimental_output.tr w]
$ns trace-all $f
set a [open cwnd.dat w]

proc finish {} {
	global ns f
	$ns flush-trace
	close $f
	exit 0
}

set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$ns duplex-link $n1 $n2 20Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 20Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

$ns queue-limit $n2 $n3 60

$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down


#$ns duplex-link-op $n2 $n3 queuePos 0.3

#CBR using Udp
set udp1 [new Agent/UDP]
$udp1 set class_ 1
$ns attach-agent $n2 $udp1

set cbr1 [new Application/Traffic/CBR]
$cbr1 attach-agent $udp1
$cbr1 set packetSize_ 1000
$cbr1 set interval_ 0.01
$cbr1 set random_ 1
$cbr1 set rate_ 10Mb

set null0 [new Agent/Null]
$ns attach-agent $n3 $null0
$ns connect $udp1 $null0
$udp1 set fid_ 1

#TCP connection
set tcp1 [new Agent/TCP/Vegas]
$tcp1 set class_ 2
$tcp1 trace cwnd_
$tcp1 attach $a
$tcp1 set window_ 600
$ns attach-agent $n1 $tcp1

set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp1 $sink
$tcp1 set fid_ 1

#setup FTP over TCP
set ftp [new Application/FTP]
$ftp attach-agent $tcp1
$ftp set type_ FTP

$ns at 0.2 "$cbr1 start"
$ns at 0.7 "$ftp start"
$ns at 34.9 "$ftp stop"
$ns at 35.0 "$cbr1 stop"
$ns at 35.1 "finish"

$ns run
