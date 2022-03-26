import requests
import sys
from pwn import *

def fuzz(url, port):
	print(f"\n$$$$ FUZZING $$$$$\n")


	rutas = [".git", "vendor", "robots.txt", "maps"]

	p1 = log.progress("Fuzzing")

	if port == 80:
		http = "http://"
	elif port == 443:
		http = "https://"

	for ruta in rutas:
		p1.status(f"Probando con la ruta -> {ruta}")
		web = f"{http}{url}/{ruta}"
		req = requests.get(web)
		if req.status_code != 404:
			print(f"  [{req.status_code}] -- {web}")
			continue

if __name__ == '__main__':
	if len(sys.argv) > 1:
		url = sys.argv[1]
		if len(sys.argv) == 3 and sys.argv[2] == "-s":
			port = 443
		else:
			port = 80
	fuzz(url, port)
