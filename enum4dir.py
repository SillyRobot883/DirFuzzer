import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
import threading
import sys
import signal

console = Console()

# THREADING
open_dir = []
open_count = 0
lock = threading.Lock()

stop_threads = False

def load_payloads(wordlist):
    try:
        with open(wordlist, "r") as f:
            payloads = f.read().splitlines()
        return payloads
    except FileNotFoundError:
        console.log("[bold red]The payload file wasn't found. Please try again.")
        exit(1)

def scan_dir(network, dir):
    global open_count, stop_threads

    if stop_threads:
        return

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
    global open_dir, open_count, stop_threads

    payloads = load_payloads(wordlist)

    console.log(f"[bold cyan]Starting enumeration with {threads} threads...")

    def signal_handler(sig, frame):
        global stop_threads
        console.log("\n[bold red]CTRL+C detected. Stopping enumeration...")
        stop_threads = True
        executor.shutdown(wait=False)

    signal.signal(signal.SIGINT, signal_handler)
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(scan_dir, network, dir) for dir in payloads]

            for future in as_completed(futures):
                if stop_threads:
                    break

    except KeyboardInterrupt:
        pass

    finally:
        # Print results and save them
        console.log("\n[bold yellow]Results:")
        console.log(f"[bold yellow]Directories found: {open_count}")

        for i in range(len(open_dir)):
            console.log(f"[bold yellow]/{open_dir[i]}")

        if output_file:
            with open(output_file, "w") as f:
                for dir in open_dir:
                    f.write(f"/{dir.split(' ')[0]}\n")

            console.log(f"[bold green]Results saved to {output_file}")

        sys.exit(0)

