#!/bin/env python3
import subprocess
import shlex
import requests

API_URL = "https://api.test.me/v1/pirate/getbalances"
EXCLUDED_ADDRESS = ""
TO_ADDRESS = ""
GENERAL_FUND_WALLET = "zs1ymgqg9dnt20q3y6lk8za2a7cq53evmqwy4lvnfruq5z4z9g3tj8znejw28e39r64yakgvcgurv2"
FEE = 0.0005
CLI = '/sdc/pirate/pirate-cli'
CONF = '/sdc/pirate/.komodo/PIRATE/PIRATE.conf'

def fetch_balances():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print(f"Failed to fetch balances: {e}")
        return []

def build_and_run_command(from_addr, amount_to_send):
    gf_tax = round(float(amount_to_send*0.05),8)
    command = (
        f'/sdc/pirate/pirate-cli -conf=/sdc/pirate/.komodo/PIRATE/PIRATE.conf '
        f'z_sendmany "{from_addr}" '
        f"'[{{\"address\": \"{TO_ADDRESS}\", \"amount\": {amount_to_send:.8f}}},"
        f"{{\"address\": \"{GENERAL_FUND_WALLET}\", \"amount\": {gf_tax:.8f}}}]' "
        f'1 '
        f'{FEE:.8f}'
    )




    print("\nRunning command:")
    print(command)

    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            check=True
        )
        print("\nCommand output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("\nError running command:")
        print(e.stderr)

def main():
    print("====== Pirate Auto Send ======")
    balances = fetch_balances()

    if not balances:
        print("No balances found.")
        return

    for entry in balances:
        address = entry.get("address")
        balance = entry.get("balance", 0.0)
        spendable = entry.get("spendable", False)

        if address != EXCLUDED_ADDRESS and spendable and balance > FEE:
            amount_to_send = balance - FEE
            print(f"\nPreparing to send from {address} with balance {balance:.8f} (sending {amount_to_send:.8f})")
            build_and_run_command(address, amount_to_send)
        else:
            print(f"\nSkipping address {address}: not valid or balance too low")

if __name__ == "__main__":
    main()
