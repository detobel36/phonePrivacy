#!/usr/bin/python3

from scapy.all import wrpcap, sniff, IP, ARP, DNS, UDP, IPv6, Dot3, Raw, DNSRR
import os
import socket
import argparse
from datetime import datetime
from math import log10
import ipaddress


## Utils
def sumStepToOneDict(dictionnary):
    result = dict()
    values = list(dictionnary.values())
    for elem in values:
        for key in elem.keys():
            if key not in result:
                result[key] = 0
            result[key] += elem[key]
    return result


def formatBigNumber(number, size = None):
    if(size is None):
        strFormated = '{:,}'
    else:
        sizeLength = int(log10(size)+1)
        # Add space
        sizeLength += int((sizeLength-1) / 3)
        strFormated = '{:' + str(sizeLength) + ',}'

    return strFormated.format(number).replace(',', ' ')

def getCurrentDatetime():
    return str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

def getCurrentDir():
    return str(os.path.dirname(os.path.realpath(__file__)))


class StoreDNS:

    def __init__(self, name, listResponse = None, numRequest = 1):
        if(name[-1] == "."):
            name = name[:-1]

        self.name = name
        if(listResponse == None):
            self.response = list()
        else:
            self.response = listResponse
        self.numRequest = numRequest

    def addResponse(self, response):
        self.response.append(response)

    def incrementNbrRequst(self):
        self.numRequest += 1

    def ipRegisterByDns(self, ip):
        return ip in self.response

    def getName(self):
        return self.name

    def __repr__(self):
        return 'StoreDNS(' + str(self.name) + ", " + str(self.response) + ", " + \
            str(self.numRequest) + ")"

    def __str__(self):
        result = '{:40} ({} requests)\n'.format(self.name, self.numRequest)
        for selectedResponse in set(self.response):
            result += '\t{:>15}\n'.format(selectedResponse)
        return result

    def __add__(self, other):
        if(other.name == self.name):
            return StoreDNS(self.name, list(set(self.response + other.response)), \
                self.numRequest + other.numRequest)
        return TypeError("DNS Name are not the same")

    def __radd__(self, other):
        if(other == 0):
            return self
        return TypeError("Could only be add with zero (which is default value)")

class Analyze:

    # Contant
    SELECT_INTERFACE = 'ap0'
    LOCAL_NETWORK = ipaddress.IPv4Network('192.168.0.0/16')
    DEFAULT_PHONE_IP = "192.168.12.243"
    DEFAULT_LOCAL_IP_ADDRRESS = "192.168.12.1"
    PING_PORT = 12345
    
    def __init__(self, phoneIp, localIp, ignore_step):
        
        self.localIp = self.DEFAULT_LOCAL_IP_ADDRRESS if localIp is None else localIp
        self.phoneIp = self.DEFAULT_PHONE_IP if phoneIp is None else phoneIp
        self.ignore_step = ignore_step

        print("Init analyze of phone: " + str(self.phoneIp) + " with local IP: " + str(self.localIp))

        self.allHost = dict()
        self.allDnsRequest = dict()
        self.allLocalRequest = dict()  # TODO utilise ces données
        self.listStepPackets = list()
        self.registerIpDns = [self.localIp, self.phoneIp, "0.0.0.0"]

        if(self.ignore_step):
            self.currentStep = 0
            self.listStepPackets.append(list())
        else:
            self.currentStep = -1

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
        else:
            print("Analyze " + str(len(self.listStepPackets)) + " steps")

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
                    # print("DNS resquest: ")
                    # packet[DNS].show()

                    dnsRequest = str(packet[DNS].qd.qname.decode("utf-8"))

                    if(dnsRequest not in self.allDnsRequest[step]):
                        self.allDnsRequest[step][dnsRequest] = StoreDNS(dnsRequest)
                    
                    # Check if package contain a response
                    if(packet.haslayer(DNSRR)):
                        a_count = packet[DNS].ancount

                        i = a_count + 4
                        while i > 4:
                            response = packet[0][i]
                            try:
                                if(response.type == 1):
                                    self.registerIpDns.append(response.rdata)
                                    self.allDnsRequest[step][dnsRequest].addResponse(response.rdata)
                            except AttributeError:
                                pass
                            
                            i -= 1
                    else:
                        self.allDnsRequest[step][dnsRequest].incrementNbrRequst()

                    # if(dnsRequest not in self.allDnsRequest[step]):
                    #     self.allDnsRequest[step][dnsRequest] = 0
                    # self.allDnsRequest[step][dnsRequest] += 1

    def _detectStep(self, packet):
        if(self._isPacketLinkedToPhone(packet)):
            ip = self._getPacketIp(packet)

            if(ip == self.localIp and packet.haslayer(UDP) and packet[UDP].dport == self.PING_PORT):
                self.currentStep += 1
                self.listStepPackets.append(list())
                print("New step detected: " + str(packet[Raw].load.decode("utf-8")) + " " + \
                    "(current: " + str(self.currentStep) + ")")

            if(self.currentStep >= 0):
                self.listStepPackets[self.currentStep].append(packet)

    def _getAllPackets(self):
        """
        Join all packets store at each step and produce one big list

        :return: List with all packets
        """
        return [item for sublist in self.listStepPackets for item in sublist]

    def savePackets(self, outputFolder):
        if(outputFolder is None):
            outputFolder = getCurrentDir()

        wrpcap(outputFolder + "/save_" + getCurrentDatetime() + ".pcap", 
            self._getAllPackets())

    def _saveResultRequest(self, resultFile, listDnsRequest, allHost):
        resultFile.write("\n")
        resultFile.write("Number of host: " + str(formatBigNumber(len(allHost))) + "\n")
        resultFile.write("Number of packages: " + str(formatBigNumber(sum(allHost.values()))) + "\n")
        resultFile.write("\n")
        resultFile.write("DNS Request:\n")

        for dnsRequest in listDnsRequest.values():
            resultFile.write(' ' + str(dnsRequest))

        resultFile.write("\n")
        resultFile.write("Requests:\n")
        maxRequestForOneHost = max(allHost.values())
        for host in sorted(allHost, key=allHost.__getitem__, reverse=True):

            hostName = list()
            for dnsRequest in listDnsRequest.values():
                if(dnsRequest.ipRegisterByDns(host)):
                    hostName.append(dnsRequest.getName())
            if(ipaddress.IPv4Address(host) in self.LOCAL_NETWORK):
                hostName.append("LocalNetwork")

            resultFile.write(' ' + formatBigNumber(allHost[host], maxRequestForOneHost) + \
                ' requests {:>15} ({})\n'.format(host, ", ".join(hostName)))

        listPotentialHardCodedIp = list(allHost.keys())
        hardCodedIp = set(listPotentialHardCodedIp) - set(self.registerIpDns)

        resultFile.write("\n")
        if(len(hardCodedIp) > 0):
            resultFile.write("Hard coded IP:\n")

            for selectedIp in hardCodedIp:
                try:
                    reversed_dns = socket.gethostbyaddr(selectedIp)
                except socket.herror:
                    reversed_dns = None

                if(reversed_dns != None and len(reversed_dns) > 0):
                    dnsInfo = str(reversed_dns[0])
                else:
                    dnsInfo = ""

                resultFile.write(' {:40} -> {:>15}\n'.format(dnsInfo, selectedIp))
        else:
            resultFile.write("No hard coded IP\n")


    def saveResults(self, outputFolder):
        if(outputFolder is None):
            outputFolder = getCurrentDir()

        with open(outputFolder + "/results_" + getCurrentDatetime() + ".txt", 'w') as resultFile:

            # General header
            resultFile.write("======== General results =========\n")

            allHostAllStep = sumStepToOneDict(self.allHost)
            allDnsRequestAllStep = sumStepToOneDict(self.allDnsRequest)

            self._saveResultRequest(resultFile, allDnsRequestAllStep, allHostAllStep)

            # General footer
            resultFile.write("\n")
            
            if(len(self.listStepPackets) > 1):
                for step in range(len(self.listStepPackets)):
                    if(self.ignore_step):
                        diplay_step = step-1
                    else:
                        diplay_step = step

                    resultFile.write("============= Step " + str(diplay_step) + " =============\n")

                    hardCodedIp = list(self.allHost[step].keys())
                    self._saveResultRequest(resultFile, self.allDnsRequest[step], self.allHost[step])

                    resultFile.write("==================================\n")
        print("Saved result into: " + str(outputFolder + "/results_" + getCurrentDatetime() + ".txt"))

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

    def readFile(self, filename):
        try:
            sniff(offline=open(filename, "rb"), prn=self._detectStep, 
                stop_filter=self._detectFinishPacket)
        except OSError as e:
            print("Problem with connexion: " + str(e))

        print(str(len(self._getAllPackets())) + " packets captured")
        if(len(self._getAllPackets()) > 0):
            self._analyzePacket()


if __name__ == '__main__':
    # TODO changer la description
    parser = argparse.ArgumentParser(description='Analyze packet')
    parser.add_argument("-p", "--phone-ip", help="IP of the phone analyzed")
    parser.add_argument("-l", "--local-ip", help="Local IP")
    parser.add_argument("-o", "--output", help="Output folder")
    parser.add_argument("-f", "--input-file", help="Analyze packet file and not captured packet")
    parser.add_argument("-i", "--ignore-step", help="Ignore step to begin the analyze", 
        action='store_true')

    args = parser.parse_args()

    analyzeObject = Analyze(args.phone_ip, args.local_ip, args.ignore_step)

    if(args.input_file is None):
        analyzeObject.sniffPacket()
        analyzeObject.savePackets(args.output)
    else:
        analyzeObject.readFile(args.input_file)

    analyzeObject.saveResults(args.output)

