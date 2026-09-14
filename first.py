from collections import deque
import time
from datetime import datetime


# =====================================================
# TRANSACTION
# =====================================================

class Transaction:

    def __init__(self, transaction_type, amount, description):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.time = time.time()

    def display(self):
        date_time = datetime.fromtimestamp(self.time)

        print(
            f"{self.transaction_type:<10} | "
            f"Rs.{self.amount:<10.2f} | "
            f"{self.description:<30} | "
            f"{date_time}"
        )


# =====================================================
# LINKED LIST NODE
# =====================================================

class TransactionNode:

    def __init__(self, transaction):
        self.transaction = transaction
        self.next = None


# =====================================================
# TRANSACTION LEDGER - LINKED LIST
# =====================================================

class TransactionLedger:

    def __init__(self):
        self.head = None

    def add_transaction(self, transaction):

        new_node = TransactionNode(transaction)

        if self.head is None:
            self.head = new_node
            return

        temp = self.head

        while temp.next is not None:
            temp = temp.next

        temp.next = new_node

    def display_history(self):

        if self.head is None:
            print("\nNo transactions found.")
            return

        print("\n" + "=" * 90)
        print("                     TRANSACTION HISTORY")
        print("=" * 90)

        temp = self.head

        while temp is not None:
            temp.transaction.display()
            temp = temp.next


# =====================================================
# BANK ACCOUNT
# =====================================================

class BankAccount:

    def __init__(self, account_number, name, balance):

        self.account_number = account_number
        self.name = name
        self.balance = balance

        # Linked List
        self.ledger = TransactionLedger()

        # Sliding Window
        self.transaction_times = deque()

    def show_account(self):

        print("\n" + "=" * 40)
        print("           ACCOUNT DETAILS")
        print("=" * 40)

        print("Account Number :", self.account_number)
        print("Name           :", self.name)
        print(f"Balance        : Rs.{self.balance:.2f}")


# =====================================================
# BST NODE
# =====================================================

class BSTNode:

    def __init__(self, account_number):

        self.account_number = account_number
        self.left = None
        self.right = None


# =====================================================
# BINARY SEARCH TREE
# =====================================================

class AccountBST:

    def __init__(self):
        self.root = None

    def insert(self, root, account_number):

        if root is None:
            return BSTNode(account_number)

        if account_number < root.account_number:

            root.left = self.insert(
                root.left,
                account_number
            )

        elif account_number > root.account_number:

            root.right = self.insert(
                root.right,
                account_number
            )

        return root

    def add_account(self, account_number):

        self.root = self.insert(
            self.root,
            account_number
        )

    def search(self, root, account_number):

        if root is None:
            return False

        if root.account_number == account_number:
            return True

        if account_number < root.account_number:

            return self.search(
                root.left,
                account_number
            )

        return self.search(
            root.right,
            account_number
        )

    def contains(self, account_number):

        return self.search(
            self.root,
            account_number
        )

    def inorder(self, root):

        if root is None:
            return

        self.inorder(root.left)

        print(root.account_number, end=" ")

        self.inorder(root.right)

    def display_sorted_accounts(self):

        print("\nAccounts in sorted order:")

        self.inorder(self.root)

        print()


# =====================================================
# FRAUD DETECTOR - SLIDING WINDOW
# =====================================================

class FraudDetector:

    WINDOW_SIZE = 60
    MAX_TRANSACTIONS = 5

    @staticmethod
    def check_fraud(account):

        current_time = time.time()

        # Old transactions ko remove karo
        while (
            account.transaction_times
            and current_time - account.transaction_times[0]
            > FraudDetector.WINDOW_SIZE
        ):

            account.transaction_times.popleft()

        # Current transaction add karo
        account.transaction_times.append(current_time)

        # 60 seconds ke andar 5 transactions
        if len(account.transaction_times) >= FraudDetector.MAX_TRANSACTIONS:

            print("\n" + "!" * 60)
            print("              FRAUD ALERT")
            print("!" * 60)

            print(
                f"Account {account.account_number} "
                f"has made {len(account.transaction_times)} "
                f"transactions within 60 seconds."
            )

            print("Please verify this account.")

            return True

        return False


# =====================================================
# BANK MANAGEMENT SYSTEM
# =====================================================

class Bank:

    def __init__(self):

        # HASHING
        # Account Number -> BankAccount
        self.accounts = {}

        # BST
        self.account_bst = AccountBST()

    # -------------------------------------------------
    # CREATE ACCOUNT
    # -------------------------------------------------

    def create_account(
        self,
        account_number,
        name,
        initial_balance
    ):

        # HashMap/Dictionary search
        if account_number in self.accounts:

            print("\nAccount already exists!")
            return

        if initial_balance < 0:

            print("\nInvalid initial balance!")
            return

        account = BankAccount(
            account_number,
            name,
            initial_balance
        )

        # Hashing
        self.accounts[account_number] = account

        # BST
        self.account_bst.add_account(account_number)

        print("\nAccount created successfully!")

    # -------------------------------------------------
    # FIND ACCOUNT
    # -------------------------------------------------

    def find_account(self, account_number):

        # Dictionary gives fast lookup
        return self.accounts.get(account_number)

    # -------------------------------------------------
    # DEPOSIT
    # -------------------------------------------------

    def deposit(self, account_number, amount):

        account = self.find_account(account_number)

        if account is None:

            print("\nAccount not found!")
            return

        if amount <= 0:

            print("\nAmount must be greater than 0.")
            return

        account.balance += amount

        transaction = Transaction(
            "DEPOSIT",
            amount,
            "Money deposited"
        )

        # Linked List
        account.ledger.add_transaction(transaction)

        # Sliding Window
        FraudDetector.check_fraud(account)

        print("\nDeposit successful!")
        print(f"New Balance: Rs.{account.balance:.2f}")

    # -------------------------------------------------
    # WITHDRAW
    # -------------------------------------------------

    def withdraw(self, account_number, amount):

        account = self.find_account(account_number)

        if account is None:

            print("\nAccount not found!")
            return

        if amount <= 0:

            print("\nAmount must be greater than 0.")
            return

        if amount > account.balance:

            print("\nInsufficient balance!")
            return

        account.balance -= amount

        transaction = Transaction(
            "WITHDRAW",
            amount,
            "Money withdrawn"
        )

        # Linked List
        account.ledger.add_transaction(transaction)

        # Sliding Window
        FraudDetector.check_fraud(account)

        print("\nWithdrawal successful!")
        print(f"New Balance: Rs.{account.balance:.2f}")

    # -------------------------------------------------
    # TRANSFER
    # -------------------------------------------------

    def transfer(
        self,
        sender_number,
        receiver_number,
        amount
    ):

        sender = self.find_account(sender_number)
        receiver = self.find_account(receiver_number)

        if sender is None:

            print("\nSender account not found!")
            return

        if receiver is None:

            print("\nReceiver account not found!")
            return

        if sender_number == receiver_number:

            print("\nSender and receiver cannot be same.")
            return

        if amount <= 0:

            print("\nInvalid amount!")
            return

        if amount > sender.balance:

            print("\nInsufficient balance!")
            return

        # Balance update
        sender.balance -= amount
        receiver.balance += amount

        # Sender transaction
        sender_transaction = Transaction(
            "TRANSFER",
            amount,
            f"Transferred to {receiver_number}"
        )

        # Receiver transaction
        receiver_transaction = Transaction(
            "RECEIVED",
            amount,
            f"Received from {sender_number}"
        )

        # Linked List
        sender.ledger.add_transaction(
            sender_transaction
        )

        receiver.ledger.add_transaction(
            receiver_transaction
        )

        # Fraud detection for sender
        FraudDetector.check_fraud(sender)

        print("\nTransfer successful!")

        print(
            f"Rs.{amount:.2f} transferred "
            f"from {sender_number} "
            f"to {receiver_number}"
        )

    # -------------------------------------------------
    # SEARCH ACCOUNT
    # -------------------------------------------------

    def search_account(self, account_number):

        account = self.find_account(account_number)

        if account is None:

            print("\nAccount not found!")

        else:

            account.show_account()

    # -------------------------------------------------
    # TRANSACTION HISTORY
    # -------------------------------------------------

    def transaction_history(self, account_number):

        account = self.find_account(account_number)

        if account is None:

            print("\nAccount not found!")
            return

        account.ledger.display_history()

    # -------------------------------------------------
    # BST SEARCH
    # -------------------------------------------------

    def bst_search(self, account_number):

        if self.account_bst.contains(account_number):

            print(
                f"\nAccount {account_number} "
                "exists in BST."
            )

        else:

            print(
                f"\nAccount {account_number} "
                "not found in BST."
            )

    # -------------------------------------------------
    # DISPLAY ALL ACCOUNTS
    # -------------------------------------------------

    def display_all_accounts(self):

        if not self.accounts:

            print("\nNo accounts available.")
            return

        print("\n" + "=" * 60)
        print("                    ALL ACCOUNTS")
        print("=" * 60)

        for account in self.accounts.values():

            print(
                f"Account: {account.account_number} | "
                f"Name: {account.name} | "
                f"Balance: Rs.{account.balance:.2f}"
            )


# =====================================================
# MAIN PROGRAM
# =====================================================

def main():

    bank = Bank()

    while True:

        print("\n")
        print("=" * 50)
        print("          BANK MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Search Account")
        print("6. Transaction History")
        print("7. Search Account using BST")
        print("8. Display Sorted Account Numbers")
        print("9. Display All Accounts")
        print("10. Exit")

        print("=" * 50)

        try:

            choice = int(
                input("Enter your choice: ")
            )

        except ValueError:

            print("\nPlease enter a valid number.")
            continue

        # ---------------------------------------------
        # CREATE ACCOUNT
        # ---------------------------------------------

        if choice == 1:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                name = input("Enter Name: ")

                balance = float(
                    input("Enter Initial Balance: ")
                )

                bank.create_account(
                    account_number,
                    name,
                    balance
                )

            except ValueError:

                print("\nInvalid input!")

        # ---------------------------------------------
        # DEPOSIT
        # ---------------------------------------------

        elif choice == 2:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                amount = float(
                    input("Enter Amount: ")
                )

                bank.deposit(
                    account_number,
                    amount
                )

            except ValueError:

                print("\nInvalid input!")

        # ---------------------------------------------
        # WITHDRAW
        # ---------------------------------------------

        elif choice == 3:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                amount = float(
                    input("Enter Amount: ")
                )

                bank.withdraw(
                    account_number,
                    amount
                )

            except ValueError:

                print("\nInvalid input!")

        # ---------------------------------------------
        # TRANSFER
        # ---------------------------------------------

        elif choice == 4:

            try:

                sender = int(
                    input("Enter Sender Account: ")
                )

                receiver = int(
                    input("Enter Receiver Account: ")
                )

                amount = float(
                    input("Enter Amount: ")
                )

                bank.transfer(
                    sender,
                    receiver,
                    amount
                )

            except ValueError:

                print("\nInvalid input!")

        # ---------------------------------------------
        # SEARCH ACCOUNT
        # ---------------------------------------------

        elif choice == 5:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                bank.search_account(
                    account_number
                )

            except ValueError:

                print("\nInvalid account number!")

        # ---------------------------------------------
        # TRANSACTION HISTORY
        # ---------------------------------------------

        elif choice == 6:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                bank.transaction_history(
                    account_number
                )

            except ValueError:

                print("\nInvalid account number!")

        # ---------------------------------------------
        # BST SEARCH
        # ---------------------------------------------

        elif choice == 7:

            try:

                account_number = int(
                    input("Enter Account Number: ")
                )

                bank.bst_search(
                    account_number
                )

            except ValueError:

                print("\nInvalid account number!")

        # ---------------------------------------------
        # SORTED ACCOUNTS
        # ---------------------------------------------

        elif choice == 8:

            bank.account_bst.display_sorted_accounts()

        # ---------------------------------------------
        # ALL ACCOUNTS
        # ---------------------------------------------

        elif choice == 9:

            bank.display_all_accounts()

        # ---------------------------------------------
        # EXIT
        # ---------------------------------------------

        elif choice == 10:

            print("\nThank you for using Bank Management System!")
            break

        else:

            print("\nInvalid choice!")


# =====================================================
# PROGRAM START
# =====================================================

if __name__ == "__main__":
    main()