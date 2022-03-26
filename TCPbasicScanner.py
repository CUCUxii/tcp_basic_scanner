#!/usr/bin/python3

import re, sys, subprocess, socket
from fuzzxii import *

ports = []
services = []

if len(sys.argv) != 2:
	print("\n [!] Uso: python3 " + sys.argv[0] + " IP\n")
	sys.exit(1)

def get_ttl(ip_adress):
	proc = subprocess.Popen(["/usr/bin/ping -c 1 {}" .format(ip_adress), ""], stdout=subprocess.PIPE, shell=True)
	(out,err) = proc.communicate()
	out = out.split()
	out = out[12].decode('utf-8')
	ttl_value = re.findall(r"\d{1,3}", out)[0]
	return ttl_value

def get_os(ttl):
	ttl = int(ttl)
	if ttl >= 0 and ttl <= 64:
		return "Linux"
	elif ttl >= 65 and ttl <= 128:
		return "Windows"
	else:
		return "Error"

def scan(ip_adress, port, open_ports):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((ip_adress, port))
		sock.send(b"\r\n")
		open_ports.append(port)
	except socket.error as e:
		if 'timeout' in str(e):
			pass
		else:
			pass
	finally:
		sock.close()

def get_services(x, services, ports):
	num_indx = ports.index(x)
	padding = " " * (4 - len(str(x)))
	print("  > port {}{} -> service {} ".format(x, padding, services[num_indx]))

def main(ports, SERVICES):
	ip_adress = sys.argv[1]
	ttl = get_ttl(ip_adress)
	os_name = get_os(ttl)

	if os_name == "Windows":
		ports = [20, 21, 22, 25, 80, 88, 135, 139, 443, 445, 1433]
		services = ["ftp", "ftp", "ssh", "smtp", "http", "kerberos", "rpc", "ldap", "https", "Samba", "MsSQL"]
	elif os_name == "Linux":
		ports = [20, 21, 22, 25, 80, 139, 443]
		services = ["ftp", "ftp", "ssh", "smtp", "http", "ldap", "https"]

	print(" [*] For ip: {},\n [*] ttl value -> {}, then SO is: -> {}" .format(ip_adress, ttl, os_name))
	socket.setdefaulttimeout(1)
	open_ports = []
	for port in ports:
		scan(ip_adress, port, open_ports)
	print("----------------------------------------------")

	for x in open_ports:
		if x in ports:
			get_services(x, services, ports)
			
	if 80 in open_ports:
		fuzz(ip_adress, 80)
	elif 443 in open_ports:
		fuzz(ip_adress, 443)
	else:
		print("No webs to fuzz")

if __name__ == '__main__':
	main(ports, services)
