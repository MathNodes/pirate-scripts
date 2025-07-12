import subprocess
import shlex

CLI = '/sdc/pirate/pirate-cli'
CONF = '/sdc/pirate/.komodo/PIRATE/PIRATE.conf'

def main():
    # Prompt the user for input
    print("======Pirate Send======")
    from_address = input("Enter the From Address: ").strip()
    to_address = input("Enter the To Address: ").strip()
    amount_input = input("Enter the Amount: ").strip()
    fee_input = input("Enter the Fee (default = 0.0001): ").strip() or "0.0001"

    # Validate and convert amount
    try:
        amount = float(amount_input)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
    except ValueError as e:  
        print(f"Invalid amount: {e}")
        return

    # Validate and convert fee
    try:
        fee = float(fee_input)
        if fee < 0:
            raise ValueError("Fee must not be negative.")
    except ValueError as e:  
        print(f"Invalid fee: {e}")
        return

    # Calculate the final amount to send
    amount_to_send = amount - fee
    if amount_to_send <= 0:  
        print("Fee is too high. Resulting amount to send must be greater than zero.")
        return

    # Build the command
    command = (
        f'{CLI} -conf={CONF}'
        f'z_sendmany "{from_address}" '
        f"'[{{\"address\": \"{to_address}\", \"amount\": {amount_to_send:.8f}}}]' "
        f'1 '
        f'{fee:.8f}'
    )

    # Display the command being run
    print("\nRunning command:")
    print(command)

    # Run the command
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

if __name__ == "__main__":   
    main()