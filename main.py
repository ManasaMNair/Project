import json
import os
import random
from datetime import datetime


class ATM:

    def __init__(self):
        self.filename = "atm_accounts.json"
        self.accounts = {}
        self.load_accounts()

    # Load account details from file
    def load_accounts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.accounts = json.load(file)

            except (json.JSONDecodeError, OSError):
                print("Error loading account data.")
                self.accounts = {}

        # Create sample accounts for first-time execution
        if not self.accounts:
            self.create_account("12345", "1234", 5000)
            self.create_account("23456", "5678", 8000)
            self.create_account("34567", "9012", 10000)

    # Save account details to file
    def save_accounts(self):
        with open(self.filename, "w") as file:
            json.dump(self.accounts, file, indent=4)

    # Create a new account
    def create_account(self, account_number, pin, balance):
        self.accounts[account_number] = {
            "pin": pin,
            "balance": balance,
            "transactions": []
        }
        self.save_accounts()

    # Generate a unique account number
    def generate_account_number(self):
        while True:
            account_number = str(random.randint(10000, 99999))

            if account_number not in self.accounts:
                return account_number

    # Register a new account
    def register_account(self):
        print("\n===== CREATE NEW ACCOUNT =====")

        while True:
            pin = input("Create a 4-digit PIN: ")

            if pin.isdigit() and len(pin) == 4:
                break

            print("PIN must contain exactly 4 digits.")

        account_number = self.generate_account_number()

        self.create_account(account_number, pin, 5000)

        print("\nAccount created successfully!")
        print("Your Account Number:", account_number)
        print("Initial Balance: Rs. 5000.00")
        print("Please remember your account number.")

    # Record a transaction
    def record_transaction(self, account_number, message):
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        transaction = (
            f"{message} | Date and Time: {timestamp}"
        )

        self.accounts[account_number]["transactions"].append(
            transaction
        )

        self.save_accounts()

    # Login to an account
    def login(self):
        while True:
            account_number = input(
                "\nEnter your account number: "
            )

            if account_number not in self.accounts:
                print("Account not found.")

                retry = input(
                    "Would you like to try again? (yes/no): "
                ).lower()

                if retry != "yes":
                    return None

                continue

            attempts = 3

            while attempts > 0:
                pin = input("Enter your PIN: ")

                if pin == self.accounts[account_number]["pin"]:
                    print("\nLogin successful!")
                    return account_number

                attempts -= 1
                print("Incorrect PIN.")
                print("Attempts remaining:", attempts)

                if attempts > 0:
                    retry = input(
                        "Would you like to try again? (yes/no): "
                    ).lower()

                    if retry != "yes":
                        return None

            print("Too many incorrect attempts. Login denied.")
            return None

    # Check balance
    def check_balance(self, account_number):
        balance = self.accounts[account_number]["balance"]

        print(f"Current Balance: Rs. {balance:.2f}")

    # Deposit money
    def deposit(self, account_number):
        while True:
            try:
                amount = float(
                    input("Enter deposit amount: Rs. ")
                )

                if not (0 < amount < float("inf")):
                    print("Enter a valid positive amount.")
                    continue

                self.accounts[account_number]["balance"] += amount

                self.record_transaction(
                    account_number,
                    f"Deposited Rs. {amount:.2f}"
                )

                print("Amount deposited successfully.")
                self.check_balance(account_number)
                break

            except ValueError:
                print("Invalid input. Enter a numeric amount.")

                retry = input(
                    "Would you like to try again? (yes/no): "
                ).lower()

                if retry != "yes":
                    break

    # Withdraw money
    def withdraw(self, account_number):
        while True:
            try:
                amount = float(
                    input("Enter withdrawal amount: Rs. ")
                )

                balance = self.accounts[account_number]["balance"]

                if not (0 < amount < float("inf")):
                    print("Enter a valid positive amount.")

                elif amount > balance:
                    print("Insufficient balance.")

                else:
                    self.accounts[account_number]["balance"] -= amount

                    self.record_transaction(
                        account_number,
                        f"Withdrawn Rs. {amount:.2f}"
                    )

                    print("Please collect your cash.")
                    self.check_balance(account_number)
                    break

                retry = input(
                    "Would you like to try again? (yes/no): "
                ).lower()

                if retry != "yes":
                    break

            except ValueError:
                print("Invalid input. Enter a numeric amount.")

                retry = input(
                    "Would you like to try again? (yes/no): "
                ).lower()

                if retry != "yes":
                    break

    # Display mini statement
    def mini_statement(self, account_number):
        print("\n===== MINI STATEMENT =====")

        transactions = self.accounts[account_number]["transactions"]

        if not transactions:
            print("No transactions available.")
        else:
            for transaction in transactions:
                print(transaction)

        self.check_balance(account_number)

    # Change PIN
    def change_pin(self, account_number):
        old_pin = input("Enter your current PIN: ")

        if old_pin != self.accounts[account_number]["pin"]:
            print("Incorrect current PIN.")
            return

        while True:
            new_pin = input("Enter your new 4-digit PIN: ")

            if new_pin.isdigit() and len(new_pin) == 4:
                self.accounts[account_number]["pin"] = new_pin
                self.save_accounts()

                print("PIN changed successfully.")
                break

            print("PIN must contain exactly 4 digits.")

            retry = input(
                "Would you like to try again? (yes/no): "
            ).lower()

            if retry != "yes":
                break

    # ATM menu
    def atm_menu(self, account_number):
        while True:
            print("\n===== ATM MENU =====")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Mini Statement")
            print("5. Change PIN")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.check_balance(account_number)

            elif choice == "2":
                self.deposit(account_number)

            elif choice == "3":
                self.withdraw(account_number)

            elif choice == "4":
                self.mini_statement(account_number)

            elif choice == "5":
                self.change_pin(account_number)

            elif choice == "6":
                print("Logged out successfully.")
                break

            else:
                print("Invalid choice. Please try again.")

    # Main program
    def run(self):
        while True:
            print("\n===== ATM MANAGEMENT SYSTEM =====")
            print("1. Login")
            print("2. Create New Account")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                account_number = self.login()

                if account_number is not None:
                    self.atm_menu(account_number)

            elif choice == "2":
                self.register_account()

            elif choice == "3":
                print("Thank you for using the ATM.")
                break

            else:
                print("Invalid choice. Please try again.")


# Execute the program
if __name__ == "__main__":
    try:
        atm = ATM()
        atm.run()

    except (OSError, EOFError, KeyboardInterrupt) as error:
        print("\nProgram interrupted or a file operation failed.")
        print("Details:", error)

    finally:
        print("ATM session ended.")
