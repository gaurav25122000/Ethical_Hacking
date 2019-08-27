import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface , use --help for more info ")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac address , use --help for more info ")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for" + interface + "to" + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_curr_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("[-] Could not find MAC Address")


option = get_args()

curr_mac = get_curr_mac(option.interface)
print("Current MAC =" + str(curr_mac))

change_mac(option.interface, option.new_mac)

curr_mac = get_curr_mac(option.interface)
if curr_mac == option.new_mac:
    print("[+] MAC Address was successfully changed to " + curr_mac)
else:
    print("[-] MAC Address couldn't be changed ")
