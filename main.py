import argparse
import requests
from termcolor import colored
from pyfiglet import Figlet
from enum4dir import dirEnum
import validators as v

# TITLE
custom_fig = Figlet(font="small", width=300)
print(custom_fig.renderText("dirEnumeration"))
print(colored('\n[*] Web Directory Enumeration\n', 'cyan'))
print(colored('[*] Works on HTTP protocol only\n', 'cyan'))

parser = argparse.ArgumentParser(description="Web directory enumerator")
parser.add_argument("-u", "--url", required=True, help="Target URL (without http://)")
parser.add_argument("-w", "--wordlist", required=True, help="Wordlist file")
parser.add_argument("-o", "--output", required=False, help="Output file to save results")
parser.add_argument("-t", "--threads", required=False, type=int, default=10, help="Number of threads (default 10)")

args = parser.parse_args()

network = args.url
if network[-1] != "/":
    network += ("/")
if not network.startswith("http://"):
    network = "http://" + network

# URL validation
try:
    if v.url(network):
        try:
            res = requests.get(network)
            if res.status_code == 200:
                print("URL: ", colored(network, "green") + "\n")
                print(colored("Connected successfully!\n", "green"))
            else:
                print(colored("Could not connect to URL. Exiting...", "red"))
                exit(1)
        except Exception:
            print("Make sure the website uses", colored("HTTP", 'red'), "protocol")
            exit(1)
    else:
        print(colored("Invalid URL. Exiting...", "red"))
        exit(1)
except KeyboardInterrupt:
    print(colored("\n[*] Exiting program...\n", 'red'))
    exit(1)

dirEnum(network, args.wordlist, args.output, args.threads)
