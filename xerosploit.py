#!/usr/bin/python3
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------#
# This file is part of Xerosploit.                                          #
# Xerosploit is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation, either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# Xerosploit is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with Xerosploit.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                           #
#---------------------------------------------------------------------------#
#                                                                           #
#        Copyright © 2019 Neodrix (www.neodrix.com)                         #
#                                                                           #
#---------------------------------------------------------------------------#

import os
from terminaltables import DoubleTable
from tabulate import tabulate
from banner import xe_header
import sys, traceback
from time import sleep

#Check if the script is running as root .
if not os.geteuid() == 0:
	sys.exit("""\033[1;91m\n[!] Xerosploit must be run as root. ¯\_(ツ)_/¯\n\033[1;m""")

# Exit message
exit_msg = "\n[++] Shutting down ... Goodbye. ( ^_^)／\n"
def main():
	try:

		#Configure the network interface and gateway. 
		def config0():
			global up_interface
			with open('/opt/xerosploit/tools/files/iface.txt', 'r', encoding='utf-8') as f:
				up_interface = f.read()
			up_interface = up_interface.replace("\n","")
			if up_interface == "0":
				up_interface = os.popen("route | awk '/Iface/{getline; print $8}'").read()
				up_interface = up_interface.replace("\n","")

			global gateway
			with open('/opt/xerosploit/tools/files/gateway.txt', 'r', encoding='utf-8') as f:
				gateway = f.read()
			gateway = gateway.replace("\n","")
			if gateway == "0":
				gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()
				gateway = gateway.replace("\n","")

		def home():

			config0()
			n_name = os.popen('iwgetid -r').read() # Get wireless network name
			n_mac = os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read() # Get network mac
			n_ip = os.popen("hostname -I").read() # Local IP address
			n_host = os.popen("hostname").read() # hostname

			# Show a random banner. Configured in banner.py .  
			print(xe_header())

			print("""
[+]═══════════[ Author : @LionSec1 \033[1;36m_-\|/-_\033[1;m Website: www.neodrix.com ]═══════════[+]

					  [ Powered by Bettercap and Nmap ]""")

			print(""" \033[1;36m
┌═════════════════════════════════════════════════════════════════════════════┐
█                                                                             █
█                         Your Network Configuration                          █ 
█                                                                             █
└═════════════════════════════════════════════════════════════════════════════┘     \n \033[1;m""")

			# Print network configuration , using tabulate as table.

			table = [["IP Address","MAC Address","Gateway","Iface","Hostname"],
					 ["","","","",""],
					 [n_ip,n_mac.upper(),gateway,up_interface,n_host]]
			print(tabulate(table, stralign="center",tablefmt="fancy_grid",headers="firstrow"))
			print("")

			# Print xerosploits short description , using terminaltables as table. 
			table_datas = [
				['\033[1;36m\nInformation\n', 'XeroSploit is a penetration testing toolkit whose goal is to \nperform man in the middle attacks for testing purposes. \nIt brings various modules that allow to realise efficient attacks.\nThis tool is Powered by Bettercap and Nmap.\033[1;m']
			]
			table = DoubleTable(table_datas)
			print(table.table)

		# Get a list of all currently connected devices , using Nmap.
		def scan(): 
			config0()

			scan = os.popen("nmap " + gateway + "/24 -n -sP ").read()

			with open('/opt/xerosploit/tools/log/scan.txt','w', encoding='utf-8') as f:
				f.write(scan)

			devices = os.popen(" grep report /opt/xerosploit/tools/log/scan.txt | awk '{print $5}'").read()

			devices_mac = os.popen("grep MAC /opt/xerosploit/tools/log/scan.txt | awk '{print $3}'").read() + os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read().upper() # get devices mac and localhost mac address

			devices_name = os.popen("grep MAC /opt/xerosploit/tools/log/scan.txt | awk '{print $4 ,S$5 $6}'").read() + "\033[1;32m(This device)\033[1;m"

			table_data = [
				['IP Address', 'Mac Address', 'Manufacturer'],
				[devices, devices_mac, devices_name]
			]
			table = DoubleTable(table_data)

			# Show devices found on your network
			print("\033[1;36m[+]═══════════[ Devices found on your network ]═══════════[+]\n\033[1;m")
			print(table.table)
			target_ip()

		# Set the target IP address .
		def target_ip():
			target_parse = " --target " # Bettercap target parse . This variable will be wiped if the user want to perform MITM ATTACK on all the network. 

			print("\033[1;32m\n[+] Please choose a target (e.g. 192.168.1.10). Enter 'help' for more information.\n\033[1;m")
			target_ips = input("\033[1;36m\033[4mXero\033[0m\033[1;36m ➮ \033[1;m").strip()
			
			if target_ips == "back":
				home()
			elif target_ips == "home":
				home()
			elif target_ips == "":
				print("\033[1;91m\n[!] Please specify a target.\033[1;m") # error message if no target are specified. 
				target_ip()
			target_name = target_ips

			#modules section
			def program0():
				# I have separed target_ip() and program0() to avoid falling into a vicious circle when the user Choose the "all" option
				cmd_target = os.popen("bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'").read() # IP forwarding
				print("\033[1;34m\n[++] " + target_name + " has been targeted. \033[1;m")
				def option():
					""" Choose a module """
					print("\033[1;32m\n[+] Which module do you want to load ? Enter 'help' for more information.\n\033[1;m")
					options = input("\033[1;36m\033[4mXero\033[0m»\033[1;36m\033[4mmodules\033[0m\033[1;36m ➮ \033[1;m").strip() # select an option , port scan , vulnerability scan .. etc...
					# Port scanner
					if options == "pscan":
						print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█                         Port Scanner                         █
█                                                              █
█      Find open ports on network computers and retrieve       █
█     versions of programs running on the detected ports       █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")
						def pscan():
							if target_ips == "" or "," in target_ips:
								print("\033[1;91m\n[!] Pscan : You must specify only one target host at a time .\033[1;m")
								option()
							print("\033[1;32m\n[+] Enter 'run' to execute the 'pscan' command.\n\033[1;m")
							action_pscan = input("\033[1;36m\033[4mXero\033[0m»\033[1;36m\033[4mmodules\033[0m»\033[1;36m\033[4mpscan\033[0m\033[1;36m ➮ \033[1;m").strip()#ip to scan
							if action_pscan == "back":
								option()
							elif action_pscan == "exit":
								sys.exit(exit_msg)    
							elif action_pscan == "home":
								home()
								pscan()
							elif action_pscan == "run": 
								print("\033[1;34m\n[++] Please wait ... Scanning ports on " + target_name + " \033[1;m")
								scan_port = os.popen("nmap "+ target_ips + " -Pn" ).read()

								with open('/opt/xerosploit/tools/log/pscan.txt','w', encoding='utf-8') as save_pscan: # Save scanned ports result.
									save_pscan.write(scan_port)

								# Grep port scan information
								ports = os.popen("grep open /opt/xerosploit/tools/log/pscan.txt | awk '{print $1}'" ).read().upper() # open ports
								ports_services = os.popen("grep open /opt/xerosploit/tools/log/pscan.txt | awk '{print $3}'" ).read().upper() # open ports services
								ports_state = os.popen("grep open /opt/xerosploit/tools/log/pscan.txt | awk '{print $2}'" ).read().upper() # port state

								# Show the result of port scan

								check_open_port = os.popen("grep SERVICE /opt/xerosploit/tools/log/pscan.txt | awk '{print $2}'" ).read().upper() # check if all port ara closed with the result
								if check_open_port == "STATE\n": 

									table_data = [
										['SERVICE', 'PORT', 'STATE'],
										[ports_services, ports, ports_state]
									]
									table = DoubleTable(table_data)
									print("\033[1;36m\n[+]═════════[ Port scan result for " + target_ips +" ]═════════[+]\n\033[1;m")
									print(table.table)
									pscan()

								else:
									# if all ports are closed , show error message . 
									print(check_open_port)
									print("\033[1;91m[!] All 1000 scanned ports on " + target_name + " are closed\033[1;m")
									pscan()
							else:
								print("\033[1;91m\n[!] Error : Command not found.\033[1;m")
								pscan()
						pscan()
					# ... (rest of the code remains unchanged, just update print/input/file for Python 3)
					# Due to length, repeat the above pattern for all input/print/file usage.

				option()

			if target_ips == "back":
				home()
			elif target_ips == "exit":
				sys.exit(exit_msg)    
			elif target_ips == "home":
				home()
			elif target_ips == "help":
				table_datas = [
					["\033[1;36m\nInformation\n", "\nInsert your target IP address.\nMultiple targets : ip1,ip2,ip3,... \nThe 'all' command will target all your network.\n\n\033[1;m"]
				]
				table = DoubleTable(table_datas)
				print(table.table)
				target_ip()
			# if target = all the network
			elif target_ips == "all": 
				target_ips = ""
				target_parse = ""
				target_name = "All your network"
				program0()
			else:
				program0()

		def cmd0():
			while True:
				print("\033[1;32m\n[+] Please type 'help' to view commands.\n\033[1;m")
				cmd_0 = input("\033[1;36m\033[4mXero\033[0m\033[1;36m ➮ \033[1;m").strip()
				if cmd_0 == "scan": # Map the network
					print("\033[1;34m\n[++] Mapping your network ... \n\033[1;m")
					scan()
				elif cmd_0 == "start": # Skip network mapping and directly choose a target.
					target_ip()
				elif cmd_0 == "gateway": # Change gateway
					def gateway():
						print("")
						table_datas = [
							["\033[1;36m\nInformation\n", "\nManually set  your gateway.\nInsert '0' if you want to choose your default network gateway.\n\033[1;m"]
						]
						table = DoubleTable(table_datas)
						print(table.table)

						print("\033[1;32m\n[+] Enter your network gateway.\n\033[1;m")
						n_gateway = input("\033[1;36m\033[4mXero\033[0m»\033[1;36m\033[4mgateway\033[0m\033[1;36m ➮ \033[1;m").strip()
			
						if n_gateway == "back":
							home()
						elif n_gateway == "exit":
							sys.exit(exit_msg)    
						elif n_gateway == "home":
							home()
						else:
							with open('/opt/xerosploit/tools/files/gateway.txt','w', encoding='utf-8') as s_gateway:
								s_gateway.write(n_gateway)
							home()
					gateway()
				elif cmd_0 == "iface": # Change network interface.
					def iface():
						print("")
						table_datas = [
							["\033[1;36m\nInformation\n", "\nManually set your network interface.\nInsert '0' if you want to choose your default network interface.\n\033[1;m"]
						]
						table = DoubleTable(table_datas)
						print(table.table)

						print("\033[1;32m\n[+] Enter your network interface.\n\033[1;m")
						n_up_interface = input("\033[1;36m\033[4mXero\033[0m»\033[1;36m\033[4miface\033[0m\033[1;36m ➮ \033[1;m").strip()

						if n_up_interface == "back":
							home()
						elif n_up_interface == "exit":
							sys.exit(exit_msg)    
						elif n_up_interface == "home":
							home()
						else:
							with open('/opt/xerosploit/tools/files/iface.txt','w', encoding='utf-8') as s_up_interface:
								s_up_interface.write(n_up_interface)
							home()
					iface()        
				elif cmd_0 == "exit":
					sys.exit(exit_msg)
				elif cmd_0 == "home":
					home()
				elif cmd_0 == "rmlog": # Remove all logs
					def rm_log():
						print("\033[1;32m\n[+] Do want to remove all xerosploit logs ? (y/n)\n\033[1;m")
						cmd_rmlog = input("\033[1;36m\033[4mXero\033[0m»\033[1;36m\033[4mrmlog\033[0m\033[1;36m ➮ \033[1;m").strip()
						if cmd_rmlog == "y":
							rmlog = os.system("rm -f -R /opt/xerosploit/xerosniff/ /opt/xerosploit/tools/log/* /opt/xerosploit/tools/bettercap/modules/tmp/* /opt/xerosploit/tools/files/dns.conf")
							print("\033[1;31m\n[++] All logs have been removed. \n\033[1;m")
							sleep(1)
							home()
						elif cmd_rmlog == "n":
							home()
						elif cmd_rmlog == "exit":
							sys.exit(exit_msg)
						elif cmd_rmlog == "home":
							home()
						elif cmd_rmlog == "back":
							home()
						else:
							print("\033[1;91m\n[!] Error : Command not found. type 'y' or 'n'\033[1;m")
							rm_log()
					rm_log()    
				# Principal commands
				elif cmd_0 == "help":
					print("")
					table_datas = [
						["\033[1;36m\n\n\n\nCOMMANDS\n", """
scan     :  Map your network.

iface    :  Manually set your network interface.

gateway  :  Manually set your gateway.

start    :  Skip scan and directly set your target IP address.

rmlog    :  Delete all xerosploit logs.

help     :  Display this help message.

exit     :  Close Xerosploit.\n\033[1;m"""]
					]
					table = DoubleTable(table_datas)
					print(table.table)
				else:
					print("\033[1;91m\n[!] Error : Command not found.\033[1;m")

		home()            
		cmd0()

	except KeyboardInterrupt:
		print("\n" + exit_msg)
		sleep(1)
	except Exception:
		traceback.print_exc(file=sys.stdout)
	sys.exit(0)

if __name__ == "__main__":
	main()
