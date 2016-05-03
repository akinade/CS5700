#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'dhara'

import socket
import sys
import os
from struct import *
import random
import math
import time
import commands
import sys


class rawsocket:

    def __init__(self):
        self.IP_Version = 4
        self.IP_IHL = 5
        self.IP_ToS = 0
        self.IP_TotalLength = 0
        self.IP_Id = 45
        self.IP_Flag = 0
        self.IP_FOffset = 0
        self.IP_TTL = 255
        self.IP_Protocol = socket.IPPROTO_TCP
        self.IP_Checksum = 0
        self.dip = ''
        self.lip = ''
        self.dhostname = ''

        self.lmac = (commands.getoutput('/sbin/ifconfig').split('\n')[0].split()[4])[:]
        self.dmac = '005056fb928d'#self.getmacAddress()
        self.ETH_Protocol = '\x08\x00'

        self.tcp_source = 1234  # source port
        self.tcp_dest = 80  # destination port
        self.tcp_seq = 454
        self.next_seq = 0
        self.tcp_ack_seq = 0
        self.net_ack_seq = 0
        self.tcp_doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes

        # tcp flags

        self.tcp_fin = 0
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0
        self.tcp_ack = 0
        self.tcp_urg = 0

        # flags end

        self.tcp_window = socket.htons(2008)  #   maximum allowed window size
        self.tcp_check = 0
        self.tcp_urg_ptr = 0

        self.rcvbuffer = []
        self.rcvwindow = []
        self.timeout = 60  # sec
        self.timer = time.time()
        self.ack_timer = 0
        self.seq_timer = 0
        self.tcp_dup = 0
        self.data = ''
        self.bufferdic = {}
        self.sortedbuf = []
        self.tcp_message_seq = ''
        self.tcp_message = ''
        self.cwnd = 0x01
        self.tcp_seq_clk = 0
        self.lastpacket = ''
        '''

        try:
            self.sendsoc = socket.socket(socket.AF_INET,
                    socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error, msg:
            print 'error in creating send socket'
            sys.exit()
        '''
        try:
            self.sendsoc = socket.socket(socket.AF_PACKET,
                                         socket.SOCK_RAW)
            self.sendsoc.bind(("eth0",0))
        except socket.error, msg:
            print 'error in creating send socket'
            sys.exit()

        try:
            self.rcvsoc = socket.socket(socket.AF_INET,
                    socket.SOCK_RAW, socket.IPPROTO_TCP)
        except socket.error, msg:
            print 'error in creating rcv socket'
            sys.exit()

    def checksum(self, msg):
        s = 0
        mslen = len(msg)
        if len(msg) % 2 == 0x01:
            mslen = 2 * (len(msg) / 2)

        # loop taking 2 characters at a time

        for i in range(0, mslen, 2):
            w = ord(msg[i]) + (ord(msg[i + 0x01]) << 8)
            s = s + w
        if len(msg) % 2 == 0x01:
            w = ord(msg[-0x01])
            s = s + w

        s = (s >> 0x10) + (s & 0xffff)
        s = s + (s >> 0x10)

        # complement and mask to 4 byte short

        s = ~s & 0xffff

        return s

    def Ethheader(self):
	#print  self.lmac.replace(':','').decode('hex'),self.lmac
	#print  self.dmac,self.dmac.decode('hex')
        eth_hdr = pack("!6s6s2s", self.dmac.decode('hex'), self.lmac.replace(':','').decode('hex'), '\x08\x00')
        return eth_hdr

    def processEth(self, data):
        rcv_eth_hdr= unpack("!6s6s2s",data)
        if rcv_eth_hdr[0]==self.lmac.replace(':','').decode('hex') and rcv_eth_hdr[1]==self.dmac.decode('hex') and rcv_eth_hdr[0]=='\x08\x00':
            return True
        else:
            False


    def Tcpheader(self, user_data):

        tcp_offset_res = (self.tcp_doff << 4) + 0
        tcp_flags = self.tcp_fin + (self.tcp_syn << 0x01) \
            + (self.tcp_rst << 2) + (self.tcp_psh << 0x0003) \
            + (self.tcp_ack << 4) + (self.tcp_urg << 5)
        tcp_header = pack(
            '!HHLLBBHHH',
            self.tcp_source,
            self.tcp_dest,
            self.tcp_seq,
            self.tcp_ack_seq,
            tcp_offset_res,
            tcp_flags,
            self.tcp_window,
            self.tcp_check,
            self.tcp_urg_ptr,
            )
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)
        psh = pack(
            '!4s4sBBH',
            self.IP_SAddress,
            self.IP_DAddress,
            placeholder,
            protocol,
            tcp_length,
            )
        psh = psh + tcp_header + user_data
        tcp_check = self.checksum(psh)
        tcp_header = pack(
            '!HHLLBBH',
            self.tcp_source,
            self.tcp_dest,
            self.tcp_seq,
            self.tcp_ack_seq,
            tcp_offset_res,
            tcp_flags,
            self.tcp_window,
            ) + pack('H', tcp_check) + pack('!H', self.tcp_urg_ptr)

    # print tcp_check

        return tcp_header

    def processTcp(
        self,
        Tcpheader,
        ip_header,
        datapac,
        ):

        data = datapac
        if len(datapac) > 40:
            data = datapac[40:]
        else:
            data = ''

        tcp_header = unpack('!HHLLBBHHH', Tcpheader)
        Tcpheader_psudo = pack(
            '!HHLLBBHHH',
            tcp_header[0],
            tcp_header[0x01],
            tcp_header[2],
            tcp_header[0x0003],
            tcp_header[4],
            tcp_header[5],
            tcp_header[6],
            0,
            tcp_header[8],
            )
        tcp_length = len(Tcpheader) + len(data)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        psh = pack(
            '!4s4sBBH',
            ip_header[0],
            ip_header[0x01],
            placeholder,
            protocol,
            tcp_length,
            )
        psh = psh + Tcpheader_psudo + data
        tcp_check = self.checksum(psh)
	tcp_check = unpack('!H', pack('H', tcp_check))
        validChk = tcp_check[0] == tcp_header[7]

        validdst = self.tcp_source == tcp_header[0x01]

        validsrc = self.tcp_dest == tcp_header[0]
        if not validChk:
            print 'not a valid checksum'

        return validdst & validsrc & validChk

    def Ipheader(self,data):
        self.IP_SAddress = socket.inet_aton(self.lip)
        self.IP_DAddress = socket.inet_aton(self.dip)
        ip_ihl_ver = (self.IP_Version << 4) + self.IP_IHL
	self.IP_TotalLength=40+len(data)
	self.IP_Checksum=0
	ip_psudoheader = pack(
            '!BBHHHBBH4s4s',
            ip_ihl_ver,
            self.IP_ToS,
            self.IP_TotalLength,
            self.IP_Id,
            self.IP_FOffset,
            self.IP_TTL,
            self.IP_Checksum,
	    self.IP_Protocol,
            self.IP_SAddress,
            self.IP_DAddress,
            )
	self.IP_Checksum=unpack('!H',pack('H',self.checksum(ip_psudoheader)))[0]
	ip_header = pack(
            '!BBHHHBBH4s4s',
            ip_ihl_ver,
            self.IP_ToS,
            self.IP_TotalLength,
            self.IP_Id,
            self.IP_FOffset,
            self.IP_TTL,
            self.IP_Protocol,
            self.IP_Checksum,
            self.IP_SAddress,
            self.IP_DAddress,
            )
	return ip_header

    def processIp(self, ipHeader):
        ipheader = unpack('!BBHHHBBH4s4s', ipHeader)
        ip_header = (ipheader[8], ipheader[9])
        return ip_header

    def sendEth(self,packet):
        ethheader= self.Ethheader()
        final_packet= ethheader+packet
        self.sendsoc.send(final_packet) 

    def resend(self):
        packet = self.lastpacket

    # print 'packet contents:',packet

        #self.sendsoc.sendto(packet, (self.dip, 0))
        self.sendEth(packet)

    def send(self, message):
        tcpheader = self.Tcpheader(message)
        ipheader = self.Ipheader(message)
        packet = ipheader + tcpheader + message
        #self.sendsoc.sendto(packet, (self.dip, 0))
	#print "sending message",message
        self.sendEth(packet)
        self.tcp_seq = self.tcp_seq + len(message)
        self.tcp_seq_clk = time.time()
        self.lastpacket = packet

    def send_message(self):
        self.tcp_fin = 0
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0x01
        self.tcp_ack = 0x01
        self.tcp_urg = 0
        a = self.tcp_seq - self.tcp_message_seq
        b = a + self.cwnd
        self.send(self.tcp_message[a:b])

    def sendmessage(self, message):
        self.tcp_fin = 0
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0x01
        self.tcp_ack = 0x01
        self.tcp_urg = 0
        if self.tcp_message == '':
            self.tcp_message_seq = self.tcp_seq
        self.tcp_message = self.tcp_message + message
        self.send_message()

    def send_fin(self, message):
        self.tcp_fin = 0x01
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0
        self.tcp_ack = 0x01
        self.tcp_urg = 0
        self.send('')

    def send_ack(self):
        self.tcp_fin = 0
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0
        self.tcp_ack = 0x01
        self.tcp_urg = 0
        self.send('')
        self.ack_timer = time.time()

    def send_syn(self):
        self.tcp_fin = 0
        self.tcp_syn = 0x01
        self.tcp_rst = 0
        self.tcp_psh = 0
        self.tcp_ack = 0
        self.tcp_urg = 0
        self.send('')

    def recv_flowpac(self, integer):

        data = self.rcvsoc.recv(integer)
        timer = time.time()
        while True:
            ipHeader = data[0:20]
            tcpHeader = data[20:40]
            prot = unpack('!BBHHHBBH4s4s', ipHeader)[6]
            tcp = socket.IPPROTO_TCP == int(prot)

            # tcp=False

            if tcp:
                ip_header = self.processIp(ipHeader)
                ip_h = unpack('!4s4s', pack('!4s4s', self.IP_DAddress,
                              self.IP_SAddress))
                if ip_h == ip_header:
                    valid = self.processTcp(tcpHeader, ip_header, data)
                    flag = (int(unpack('!HHLLBBHHH', tcpHeader)[-4])
                            >> 4) % 2
                    tcp_header = unpack('!HHLLBBHHH', tcpHeader)
                    if valid:
                        return data
            timeout = time.time() - self.tcp_seq_clk
            if timeout > 60:
                self.resend()
		self.tcp_seq_clk=time.time()

        # print 'check'

            elapsed = time.time() - timer
            if elapsed > 180:
                print 'Error: no data received in last 3 min'
                sys.exit(0)
                break
            data = self.rcvsoc.recv(integer)
        return ''

    def update_buffer(self, data):
        temp = ''
        seq = unpack('!HHLLBBHHH', data[20:40])[2]
        self.bufferdic[seq] = data[40:]

    def check_buffer(self, data):
        temp = data[40:]
        tcpHeader = data[20:40]
        tcp_header = unpack('!HHLLBBHHH', tcpHeader)
        self.tcp_ack_seq = self.tcp_ack_seq + len(temp)

        sortedbuf = sorted(self.bufferdic.keys())
        if len(sortedbuf):
            while self.tcp_ack_seq == sortedbuf[0]:
                seq = sortedbuf.pop(0)
                tempdata = self.bufferdic[seq]
                temp = temp + tempdata
                self.tcp_ack_seq = self.tcp_ack_seq + len(tempdata)
                del self.bufferdic[seq]
                if len(sortedbuf) == 0:
                    break
        return temp

    def recv(self, integer):
        data = self.recv_flowpac(integer)

# ....if data == '':
# ........return ''

        while True:
            if len(data) > 40:

        # ethHeader = data[0:14]

                ipHeader = data[0:20]
                tcpHeader = data[20:40]
                ip_header = self.processIp(ipHeader)
                tcp_header = unpack('!HHLLBBHHH', tcpHeader)
                if int(tcp_header[2]) == self.tcp_ack_seq:
                    data = self.check_buffer(data)
                    self.send_ack()
                    return data
                elif int(tcp_header[2]) < self.tcp_ack_seq:
                    self.send_ack()
                elif int(tcp_header[2]) > self.tcp_ack_seq:
                    self.update_buffer(data)
            else:
                tcpHeader = data[20:40]
                tcp_header = unpack('!HHLLBBHHH', tcpHeader)
                finF = 0x01
                ackF = 0x10
                D = 0x01 & tcp_header[5]
                af = 0x10 & tcp_header[5]
                if af == 0x10:
                    if tcp_header[0x0003] == self.tcp_seq:
                        if self.cwnd < 1000:
                            self.cwnd = self.cwnd + 0x01
                        self.send_message()
                    else:
                        timeout = time.time() - self.tcp_seq_clk
                        if timeout > 60:
                            self.resend()
                            self.cwnd = 0x01
                        else:
                            self.tcp_dup = self.tcp_dup + 0x01
                            if self.tcp_dup == 0x0003:
                                self.tcp_seq = tcp_header[0x0003]
                                self.cwnd = 0x01
                                self.send_message()
                if D == 0x01:
                    self
                    self.send_ack()
                    return ''
            data = self.recv_flowpac(integer)

# ....    if data == '':
# ........return ''

        return data

    def recv_finack(self, integer):
        data = self.recv_flowpac(integer)

# ....if data == '':
# ........return ''

        while True:
            if len(data) == 40:
                tcpHeader = data[20:40]
                tcp_header = unpack('!HHLLBBHHH', tcpHeader)
                fak = 0x11 & tcp_header[5]
                if fak == 0x11:
                    self.tcp_ack_seq = self.tcp_ack_seq + 0x01
                    self.send_ack()
                    break
            data = self.recv_flowpac(integer)

# ....    if data == '':
# ........return ''

        return data

    def syn_recv(self, integer):
        data = self.recv_flowpac(integer)
        while True:
            if len(data) > 40:
                ipHeader = data[0:20]
                tcpHeader = data[20:40]
                prot = unpack('!BBHHHBBH4s4s', ipHeader)[6]
                tcp = socket.IPPROTO_TCP == int(prot)
                if tcp:
                    ip_header = self.processIp(ipHeader)
                    ip_h = unpack('!4s4s', pack('!4s4s',
                                  self.IP_DAddress, self.IP_SAddress))
                    if ip_h == ip_header:

                        valid = self.processTcp(tcpHeader, ip_header,
                                data)

                        if valid:
                            tcp_header = unpack('!HHLLBBHHH', tcpHeader)

                            if int(tcp_header[0x0003]) == self.tcp_seq \
                                + 0x01:
                                self.tcp_ack_seq = int(tcp_header[2]) \
                                    + 0x01
                                self.tcp_seq = self.tcp_seq + 0x01
                                self.send_ack()
                                break

            # elapsed = time.time() - self.timer
            # if elapsed > self.timeout:
            #    self.send_syn()
            #    self.timer = time.time()
            # data = self.rcvsoc.recv(integer)

            data = self.recv_flowpac(integer)

    def getmacAddress(self):
        rawsock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                                socket.htons(0x0003))
        rawsock.bind(('eth0', 0x0806))
        hostAddr = (commands.getoutput('/sbin/ifconfig').split('\n'
                    )[0].split()[4])[:]
        hostIpaddr = (commands.getoutput('/sbin/ifconfig').split('\n'
                      )[0x01].split()[0x01])[5:]
        destinationIp = commands.getoutput('route -n').split('\n'
                )[2].split()[0x01]
        destinationMac = ''
        eth_hdr = pack('!6s6s2s', '\xff\xff\xff\xff\xff\xff',
                       hostAddr.replace(':', '').decode('hex'),
                       '\x08\x06')

        arp_hdr = pack(
            '!2s2s1s1s2s',
            '\x00\x01',
            '\x08\x00',
            '\x06',
            '\x04',
            '\x00\x01',
            )
        arp_sender = pack('!6s4s', hostAddr.replace(':', ''
                          ).decode('hex'), socket.inet_aton(hostIpaddr))
        arp_target = pack('!6s4s', '\x00\x00\x00\x00\x00\x00',
                          socket.inet_aton(destinationIp))

        rawsock.send(eth_hdr + arp_hdr + arp_sender + arp_target)
        while True:
            rawsock.send(eth_hdr + arp_hdr + arp_sender + arp_target)
            packet = rawsock.recv(2048)
            ether = packet[0:14]
            arpdata = packet[14:42]

            packet_hdr = arpdata[0:8]
            packet_sender = arpdata[8:18]
            packet_target = arpdata[18:28]
            if unpack('!6s4s', packet_target)[0x01] == unpack('!6s4s',
                    arp_sender)[0x01]:
                if unpack('!6s4s', packet_sender)[0x01] \
                    == unpack('!6s4s', arp_target)[0x01]:
                    mac = unpack('!6s4s',
                                 packet_sender)[0x01].encode('hex')
                    return mac

    def connect(self, tuple):

        # need to do the three way handshake

        self.dhostname = tuple[0]
        self.dip = socket.gethostbyname(self.dhostname)
        self.lip = (commands.getoutput('/sbin/ifconfig').split('\n'
                    )[0x01].split()[0x01])[5:]
        self.handshake()

    def handshake(self):
        self.tcp_source = random.randint(49152, 0xffff)  # source port
        self.tcp_dest = 80  # destination port
        self.tcp_seq = random.randint(0, math.pow(2, 31))  # L
        self.tcp_ack_seq = 0
        self.tcp_doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes

        # tcp flags

        self.tcp_urg = 0
        self.tcp_ack = 0
        self.tcp_psh = 0
        self.tcp_rst = 0
        self.tcp_syn = 0x01
        self.tcp_fin = 0

        # flags end

        self.tcp_window = socket.htons(5840)  #   maximum allowed window size
        self.tcp_check = 0
        self.tcp_urg_ptr = 0

        ipheader = self.Ipheader('')
        tcpheader = self.Tcpheader('')
        packet = ipheader + tcpheader
        self.lastpacket = packet
        self.timer = time.time()
        #self.sendsoc.sendto(packet, (self.dip, 0))
	
        self.sendEth(packet)

        device = commands.getoutput('/sbin/ifconfig').split('\n'
                )[0].split()[0]

        self.syn_recv(2048)

    def close(self):
        self.send_fin('')
        self.tcp_seq = self.tcp_seq + 0x01
        self.recv_finack(2048)
        self.sendsoc.close()
        self.rcvsoc.close()



