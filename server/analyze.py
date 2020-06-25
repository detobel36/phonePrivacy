#!/usr/bin/python3

from scapy.all import wrpcap, sniff, IP, ARP, DNS, UDP, IPv6
import os
import socket
import datetime import datetime
import ipaddress

localNetwork = ipaddress.IPv4Network('192.168.0.0/16')

phoneIp = "192.168.12.243"

allHost = []
allDnsRequest = []
allLocalRequest = []

def getIp(packet):
    global phoneIp
    if(packet.haslayer(IP)):
        return packet[IP].dst if packet[IP].src == phoneIp else packet[IP].src

    elif(packet.haslayer(ARP)):
        return packet[ARP].pdst if packet[ARP].psrc == phoneIp else packet[ARP].psrc


def isCorrectHost(packet):
    global phoneIp

    if(packet != None):

        if(packet.haslayer(IP)):
            return packet[IP].src == phoneIp or packet[IP].dst == phoneIp
        elif(packet.haslayer(ARP)):
            return packet[ARP].psrc == phoneIp or packet[ARP].pdst == phoneIp

        elif(packet.haslayer(IPv6)):
            # Ignore IPv6 packet use only in local
            return False

        else:
            print("------------ PACKET NOT FOUND ------------")
            print(str(packet.show()))
            print("------------------------------------------")
            print("")

    return False

def analyzePacket(packet):
    global allHost

    if(isCorrectHost(packet)):
        # print("Packet (" + str(int(packet.time)) + "): " + str(packet.summary()))
        # print("")

        ip = getIp(packet)
        ipV4 = ipaddress.IPv4Address(ip)
        if(ipV4 in localNetwork):
            if(ip in allLocalRequest):
                allLocalRequest.append(ip)

        elif(ip not in allHost):
            allHost.append(ip)

        if(packet.haslayer(DNS)):
            dnsRequest = str(packet[DNS].qd.qname.decode("utf-8"))

            if(dnsRequest not in allDnsRequest):
                allDnsRequest.append(dnsRequest)

def getCurrentDatetime():
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')



try:
    liste = sniff(iface="ap0", prn=analyzePacket)
    # liste = sniff(iface="ap0")
except KeyboardInterrupt:
    pass

# print("Allhost: " + str(allHost))
# print("allDnsRequest: " + str(allDnsRequest))
# print("Liste: " + str(len(liste)))

allHardCodedIp = allHost[:]

print("All DNS Request:")
for dnsRequest in allDnsRequest:
    ipDnsRequest = socket.gethostbyname(dnsRequest)
    if(ipDnsRequest in allHardCodedIp):
        allHardCodedIp.remove(ipDnsRequest)
    print(ipDnsRequest + " - " + dnsRequest)


if(len(allHardCodedIp) > 0):
    print("")
    print("Hard coded IP:")
    for hardCodedIp in allHardCodedIp:
        try:
            reversed_dns = socket.gethostbyaddr(hardCodedIp)
        except socket.herror:
            reversed_dns = None

        if(reversed_dns != None and len(reversed_dns) > 0):
            print(hardCodedIp + " - " + str(reversed_dns[0]))
        else:
            print(hardCodedIp)




dir_path = os.path.dirname(os.path.realpath(__file__))
wrpcap(str(dir_path) + "/save_" + getCurrentDatetime() + ".pcap", liste)
print("Have save file")
