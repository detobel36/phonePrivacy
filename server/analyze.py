#!/usr/bin/python3

from scapy.all import wrpcap, sniff, IP, ARP, DNS, UDP, IPv6, Dot3, Raw
import os
import socket
import argparse
from datetime import datetime
import ipaddress


## Utils
def mergeListInDict(dictionnary):
    result = list()
    values = list(dictionnary.values())
    for i in range(len(values)):
        result.extend(values[i])
    return result


def getCurrentDatetime():
    return str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

def getCurrentDir():
    return str(os.path.dirname(os.path.realpath(__file__)))


class Analyze:

    # Contant
    SELECT_INTERFACE = 'ap0'
    LOCAL_NETWORK = ipaddress.IPv4Network('192.168.0.0/16')
    DEFAULT_PHONE_IP = "192.168.12.243"
    DEFAULT_LOCAL_IP_ADDRRESS = "192.168.12.1"
    PING_PORT = 12345
    
    def __init__(self, phoneIp, localIp):
        
        self.localIp = DEFAULT_LOCAL_IP_ADDRRESS if localIp is None else localIp
        self.phoneIp = DEFAULT_PHONE_IP if phoneIp is None else phoneIp

        print("Init analyze of phone: " + str(self.phoneIp) + " with local IP: " + str(self.localIp))

        self.allHost = dict()
        self.allDnsRequest = dict()
        self.allLocalRequest = dict()  # TODO utilise ces données
        self.listPackets = list()
        self.listStepPackets = list()
        self.currentStep = -1;

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

    def _analyzePacket(self):
        if(len(self.allLocalRequest) > 0 or len(self.allHost) > 0 or len(self.allDnsRequest) > 0):
            print("The analyze has already been done")
            return

        for step in range(len(self.listStepPackets)):
            self.allLocalRequest[step] = dict()
            self.allHost[step] = dict()
            self.allDnsRequest[step] = dict()

            for packet in self.listStepPackets[step]:
                ip = self._getPacketIp(packet)
                
                # Local request
                if(ipaddress.IPv4Address(ip) in self.LOCAL_NETWORK):
                    if(ip not in self.allLocalRequest[step]):
                        self.allLocalRequest[step][ip] = 0
                    self.allLocalRequest[step][ip] += 1

                # Save all host
                if(ip not in self.allHost[step]):
                    self.allHost[step][ip] = 0
                self.allHost[step][ip] += 1

                # Check DNS Request
                if(packet.haslayer(DNS)):
                    dnsRequest = str(packet[DNS].qd.qname.decode("utf-8"))

                    if(dnsRequest not in self.allDnsRequest[step]):
                        self.allDnsRequest[step][dnsRequest] = 0
                    self.allDnsRequest[step][dnsRequest] += 1

    def _detectStep(self, packet):
        if(self._isPacketLinkedToPhone(packet)):
            ip = self._getPacketIp(packet)

            if(ip == self.localIp and packet.haslayer(UDP) and packet[UDP].dport == self.PING_PORT):
                self.currentStep += 1
                self.listStepPackets.append(list())
                print("New step detected: " + str(packet[Raw].load.decode("utf-8")) + " " + \
                    "(current: " + str(self.currentStep) + ")")

            if(self.currentStep >= 0):
                self.listPackets.append(packet)
                self.listStepPackets[self.currentStep].append(packet)

    def savePackets(self, outputFolder):
        if(outputFolder is None):
            outputFolder = getCurrentDir()

        wrpcap(outputFolder + "/save_" + getCurrentDatetime() + ".pcap", 
            self.listPackets)

    def _saveResultRequest(self, resultFile, listDnsRequest, listHardCodedIp):
        resultFile.write("\n")
        resultFile.write("DNS Request:\n")
        for dnsRequest in listDnsRequest:
            dnsRequest = str(dnsRequest)
            try:
                ipDnsRequest = socket.gethostbyname(dnsRequest)
            except OSError:
                print("Error with DNS request: " + str(dnsRequest))
                resultFile.write("   ?   - " + dnsRequest + "\n")
            else:
                if(ipDnsRequest in listHardCodedIp):
                    listHardCodedIp.remove(ipDnsRequest)
                resultFile.write("  " + ipDnsRequest + " - " + dnsRequest + "\n")


        if(len(listHardCodedIp) > 0):
            resultFile.write("\n")
            resultFile.write("Hard coded IP:\n")

            for hardCodedIp in listHardCodedIp:
                try:
                    reversed_dns = socket.gethostbyaddr(hardCodedIp)
                except socket.herror:
                    reversed_dns = None

                if(reversed_dns != None and len(reversed_dns) > 0):
                    resultFile.write("  " + hardCodedIp + " - " + str(reversed_dns[0]) + "\n")
                else:
                    resultFile.write("  " + hardCodedIp + "\n")

    def saveResults(self):
        if(outputFolder is None):
            outputFolder = getCurrentDir()

        with open(outputFolder + "/results_" + getCurrentDatetime() + ".txt", 'w') as resultFile:

            # General header
            resultFile.write("======== General results =========\n")

            allHostAllStep = mergeListInDict(self.allHost)
            allDnsRequestAllStep = mergeListInDict(self.allDnsRequest)
            allHardCodedIp = allHostAllStep[:]

            self._saveResultRequest(resultFile, allDnsRequestAllStep, allHardCodedIp)

            # General footer
            resultFile.write("\n")
            

            for step in range(len(self.listStepPackets)):
                resultFile.write("============= Step " + str(step) + " =============\n")

                hardCodedIp = self.allHost[step][:]
                self._saveResultRequest(resultFile, self.allDnsRequest[step], hardCodedIp)

                resultFile.write("==================================\n")

    def _detectFinishPacket(self, packet):
        return self._getPacketIp(packet) == self.localIp and packet.haslayer(UDP) and \
            packet[UDP].dport == self.PING_PORT and packet[Raw].load.decode("utf-8") == "Finish"

    def sniffPacket(self):
        try:
            sniff(iface=self.SELECT_INTERFACE, prn=self._detectStep, 
                stop_filter=self._detectFinishPacket)
        except OSError as e:
            print("Problem with connexion: " + str(e))

        self._analyzePacket()


if __name__ == '__main__':
    # TODO changer la description
    parser = argparse.ArgumentParser(description='Analyze packet')
    parser.add_argument("-p", "--phone-ip", help="IP of the phone analyzed")
    parser.add_argument("-l", "--local-ip", help="Local IP")
    parser.add_argument("-o", "--output", help="Output folder")

    args = parser.parse_args()

    analyzeObject = Analyze(args.phone_ip, args.local_ip)
    analyzeObject.sniffPacket()
    analyzeObject.savePackets(args.output)
    analyzeObject.saveResults(args.output)

