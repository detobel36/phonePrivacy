#!/usr/bin/python3

"""
TODO
- L'appliation doit envoyer une requête PING pour dire à quel étape elle est
- Le server doit détecter le message ping
"""


from scapy.all import wrpcap, sniff, IP, ARP, DNS, UDP, IPv6, Dot3
import os
import socket
from datetime import datetime
import ipaddress

class Analyze:

    # Contant
    SELECT_INTERFACE = 'ap0'
    LOCAL_NETWORK = ipaddress.IPv4Network('192.168.0.0/16')
    
    def __init__(self, phoneIp = "192.168.12.243"):
        self.phoneIp = phoneIp
        self.allHost = list()
        self.allDnsRequest = list()
        self.allLocalRequest = list()
        self.listPackets = None

    def _getPacketIp(self, packet):
        if(packet != None):
            if(packet.haslayer(IP)):
                return packet[IP].dst if packet[IP].src == self.phoneIp else packet[IP].src

            elif(packet.haslayer(ARP)):
                return packet[ARP].pdst if packet[ARP].psrc == self.phoneIp else packet[ARP].psrc

    def _isPacketLinkedToPhone(self, packet):
        if(packet != None):

            if(packet.haslayer(IP)):
                return packet[IP].src == self.phoneIp or packet[IP].dst == self.phoneIp
            elif(packet.haslayer(ARP)):
                return packet[ARP].psrc == self.phoneIp or packet[ARP].pdst == self.phoneIp

            elif(packet.haslayer(IPv6) or packet.haslayer(Dot3)):
                # Ignore IPv6 or Dot3 packet use only in local
                return False

            else:
                print("------------ PACKET NOT FOUND ------------")
                print(str(packet.show()))
                print("------------------------------------------")
                print("")

        return False

    def _currentInterfaceExist(self):
        return self.SELECT_INTERFACE in get_if_list()

    def _analyzePacket(self, packet):
        if(self._isPacketLinkedToPhone(packet)):
            # print("Packet (" + str(int(packet.time)) + "): " + str(packet.summary()))
            # print("")

            ip = self._getPacketIp(packet)
            if(ipaddress.IPv4Address(ip) in self.LOCAL_NETWORK):
                if(ip in self.allLocalRequest):
                    self.allLocalRequest.append(ip)

            elif(ip not in self.allHost):
                self.allHost.append(ip)

            if(packet.haslayer(DNS)):
                dnsRequest = str(packet[DNS].qd.qname.decode("utf-8"))

                if(dnsRequest not in self.allDnsRequest):
                    self.allDnsRequest.append(dnsRequest)

    def _getCurrentDatetime(self):
        return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    def _getCurrentDir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def savePackets(self):
        wrpcap(str(self._getCurrentDir()) + "/save_" + self._getCurrentDatetime() + ".pcap", self.listPackets)

    def sniffPacket(self):
        try:
            self.listPackets = sniff(iface=self.SELECT_INTERFACE, prn=self._analyzePacket)
        except KeyboardInterrupt:
            pass
        except OSError as e:
            print("Problem with connexion: " + str(e))

    def printResult(self):
        allHardCodedIp = self.allHost[:]

        print("All DNS Request:")
        for dnsRequest in self.allDnsRequest:
            try:
                ipDnsRequest = socket.gethostbyname(dnsRequest)
            except OSError:
                print("Error with DNSRequest: " + str(dnsRequest))
            else:
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


print("Start analyze")
analyzeObject = Analyze()
analyzeObject.sniffPacket()
analyzeObject.savePackets()
analyzeObject.printResult()


# phoneIp = "192.168.12.243"

# allHost = []
# allDnsRequest = []
# allLocalRequest = []

# def getIp(packet):
#     global phoneIp
#     if(packet.haslayer(IP)):
#         return packet[IP].dst if packet[IP].src == phoneIp else packet[IP].src

#     elif(packet.haslayer(ARP)):
#         return packet[ARP].pdst if packet[ARP].psrc == phoneIp else packet[ARP].psrc


# def isCorrectHost(packet):
#     global phoneIp

#     if(packet != None):

#         if(packet.haslayer(IP)):
#             return packet[IP].src == phoneIp or packet[IP].dst == phoneIp
#         elif(packet.haslayer(ARP)):
#             return packet[ARP].psrc == phoneIp or packet[ARP].pdst == phoneIp

#         elif(packet.haslayer(IPv6) or packet.haslayer(Dot3)):
#             # Ignore IPv6 packet use only in local
#             return False

#         else:
#             print("------------ PACKET NOT FOUND ------------")
#             print(str(packet.show()))
#             print("------------------------------------------")
#             print("")

#     return False

# def analyzePacket(packet):
#     global allHost

#     if(isCorrectHost(packet)):
#         # print("Packet (" + str(int(packet.time)) + "): " + str(packet.summary()))
#         # print("")

#         ip = getIp(packet)
#         ipV4 = ipaddress.IPv4Address(ip)
#         if(ipV4 in LOCAL_NETWORK):
#             if(ip in allLocalRequest):
#                 allLocalRequest.append(ip)

#         elif(ip not in allHost):
#             allHost.append(ip)

#         if(packet.haslayer(DNS)):
#             dnsRequest = str(packet[DNS].qd.qname.decode("utf-8"))

#             if(dnsRequest not in allDnsRequest):
#                 allDnsRequest.append(dnsRequest)

# def getCurrentDatetime():
#     return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


# if(SELECT_INTERFACE in get_if_list()):

#     liste = None
#     try:
#         liste = sniff(iface=SELECT_INTERFACE, prn=analyzePacket)
#         # liste = sniff(iface="ap0")
#     except KeyboardInterrupt:
#         pass
#     except OSError as e:
#         print("Problem with connexion: ") # + str(e))


#     if(liste == None or len(liste) == 0):
#         print("No message received")
#         exit()

# else:
#     print("Interface " + str(SELECT_INTERFACE) + " not found")
#     exit()

# # print("Allhost: " + str(allHost))
# # print("allDnsRequest: " + str(allDnsRequest))
# # print("Liste: " + str(len(liste)))

# allHardCodedIp = allHost[:]

# print("All DNS Request:")
# for dnsRequest in allDnsRequest:
#     ipDnsRequest = socket.gethostbyname(dnsRequest)
#     if(ipDnsRequest in allHardCodedIp):
#         allHardCodedIp.remove(ipDnsRequest)
#     print(ipDnsRequest + " - " + dnsRequest)


# if(len(allHardCodedIp) > 0):
#     print("")
#     print("Hard coded IP:")
#     for hardCodedIp in allHardCodedIp:
#         try:
#             reversed_dns = socket.gethostbyaddr(hardCodedIp)
#         except socket.herror:
#             reversed_dns = None

#         if(reversed_dns != None and len(reversed_dns) > 0):
#             print(hardCodedIp + " - " + str(reversed_dns[0]))
#         else:
#             print(hardCodedIp)




# dir_path = os.path.dirname(os.path.realpath(__file__))
# wrpcap(str(dir_path) + "/save_" + self._getCurrentDatetime() + ".pcap", liste)
# print("Have save file")
