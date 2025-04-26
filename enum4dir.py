import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
import threading

console = Console()

# THREADING
open_dir = []
open_count = 0
lock = threading.Lock()  


def load_payloads(wordlist):
    try:
        with open(wordlist, "r") as f:
            payloads = f.read().splitlines()
        return payloads
    except FileNotFoundError:
        console.log("[bold red]The payload file wasn't found. Please try again.")
        exit(1)


def scan_dir(network, dir):
    global open_count

    try:
        url_mod = network + dir
        res = requests.get(url_mod, timeout=5)

        if res.status_code == 200 or res.status_code == 302:
            with lock:
                open_dir.append(f"{dir} found")
                open_count += 1
            console.log(f"[bold green]/{dir} | status: {res.status_code}")
        else:
            console.log(f"[bold red]/{dir} | status: {res.status_code}")

    except requests.RequestException:
        console.log(f"[bold yellow]Failed to connect: {network + dir}")


def dirEnum(network, wordlist, output_file, threads):
    global open_dir, open_count

    payloads = load_payloads(wordlist)

    console.log(f"[bold cyan]Starting enumeration with {threads} threads...")

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(scan_dir, network, dir) for dir in payloads]

            for _ in as_completed(futures):
                pass  # we just want to wait for all to complete
    except KeyboardInterrupt:
        console.log("\n[bold red]CTRL+C detected. Printing results...")

    finally:
        console.log("\n[bold yellow]Results:")
        console.log(f"[bold yellow]Directories found: {open_count}")

        for i in range(len(open_dir)):
            console.log(f"[bold yellow]/{open_dir[i]}")

        if output_file:
            with open(output_file, "w") as f:
                for dir in open_dir:
                    f.write(f"{dir}\n")

            console.log(f"[bold green]Results saved to {output_file}")

        exit()

