import requests
import argparse
from termcolor import colored
from pyfiglet import Figlet
from enum4dir import dirEnum
import validators as v

# TITLE
custom_fig = Figlet(font="small", width=300)
print(custom_fig.renderText("dirEnumeration"))
print(colored('\n[*] Web Directory Enumeration\n', 'cyan'))
print(colored('[*] Works on HTTP protocol only\n', 'cyan'))

def validate_url(url):
    if not url.startswith("http://"):
        url = "http://" + url

    if not v.url(url):
        raise ValueError("Invalid URL format")

    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print("\nURL:", colored(url, "green"))
            print(colored("[+] Connected successfully!\n", "green"))
            return url
        else:
            raise ValueError(f"Website responded with status: {res.status_code}")
    except Exception as e:
        raise ValueError(f"Couldn't connect to the URL: {e}")

def main():
    parser = argparse.ArgumentParser(description="Directory Enumeration Tool")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target URL (http://example.com)")
    parser.add_argument('-w', '--wordlist', type=str, default="common.txt", help="Path to wordlist")
    parser.add_argument('-o', '--output', type=str, help="Save results to a file")

    args = parser.parse_args()

    try:
        network = validate_url(args.url)
        dirEnum(network, wordlist=args.wordlist, output_file=args.output)
    except KeyboardInterrupt:
        print(colored("\n[*] Exiting program...\n", 'red'))
    except Exception as e:
        print(colored(f"\nError: {e}", 'red'))

if __name__ == "__main__":
    main()
