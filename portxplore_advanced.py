import subprocess
import json
import datetime
import threading
import logging
import sys
from report_generator import generate_pdf_report

logging.basicConfig(filename="portxplore.log", level=logging.INFO)

commands = {
    "1": ["nmap", "-T4"],
    "2": ["nmap", "-p-"],
    "3": ["nmap", "-sV"],
    "4": ["nmap", "-O"],
    "5": ["nmap", "--script=vuln"]
}

def run_scan(command, target):
    try:
        full_cmd = command + [target]
        output = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT, text=True)
        logging.info(f"Scan completed on {target}")
        return output
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error executing scan: {e}"

def threaded_scan(command, target):
    output_data = {}

    def scan():
        output_data["result"] = run_scan(command, target)

    thread = threading.Thread(target=scan)
    thread.start()
    thread.join()

    return output_data["result"]

def main():
    print("\033[96m\n=== PortXplore – Advanced Port Scanner ===\033[0m")
    target = input("Enter target IP/Domain: ")

    print("""
\033[93mSelect Scan Type:\033[0m
1. Quick Scan
2. Full Port Scan
3. Service Version Detection
4. OS Detection
5. Vulnerability Script Scan
""")

    scan_type = input("Enter scan number: ")

    if scan_type not in commands:
        print("\033[91mInvalid choice.\033[0m")
        return

    print("\033[92mRunning scan in thread…\033[0m")
    output = threaded_scan(commands[scan_type], target)

    print("\033[95m\n=== Scan Output ===\n\033[0m")
    print(output)

    # Save JSON
    json_file = f"scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w") as f:
        json.dump({"target": target, "output": output}, f, indent=4)

    print("\nJSON saved as:", json_file)

    # PDF Report
    save = input("\nGenerate PDF report? (y/n): ")
    if save.lower() == "y":
        pdf_name = f"PortXplore_Adv_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generate_pdf_report(target, output, pdf_name)
        print("\033[92mPDF Report saved as:\033[0m", pdf_name)


if __name__ == "__main__":
    main()
