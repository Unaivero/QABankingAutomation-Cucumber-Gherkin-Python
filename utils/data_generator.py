from faker import Faker
import random
import json
import os
from datetime import datetime, timedelta
from decimal import Decimal

class DataGenerator:
    """
    Utility class for generating test data for bank automation tests
    """
    
    def __init__(self):
        self.faker = Faker()
        self.test_data_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'test_data'
        )
        os.makedirs(self.test_data_path, exist_ok=True)
    
    def generate_user(self, with_2fa=False):
        """
        Generate a test user with banking profile
        
        :param with_2fa: Whether the user has 2FA enabled
        :return: Dictionary with user data
        """
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        
        user = {
            "username": f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}",
            "password": self.faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "email": self.faker.email(),
            "first_name": first_name,
            "last_name": last_name,
            "address": {
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state(),
                "zipcode": self.faker.zipcode(),
                "country": "United States"
            },
            "phone": self.faker.phone_number(),
            "date_of_birth": self.faker.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
            "ssn_last_4": f"{random.randint(1000, 9999)}",
            "has_2fa": with_2fa
        }
        
        if with_2fa:
            user["totp_secret"] = "BASE32SECRET" + ''.join(random.choice('234567ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(10))
        
        return user
    
    def generate_account(self, account_type="checking", starting_balance=None):
        """
        Generate a bank account
        
        :param account_type: Type of account (checking, savings, etc.)
        :param starting_balance: Initial balance (if None, a random balance is generated)
        :return: Dictionary with account data
        """
        if starting_balance is None:
            if account_type.lower() == "checking":
                starting_balance = Decimal(str(round(random.uniform(500, 10000), 2)))
            elif account_type.lower() == "savings":
                starting_balance = Decimal(str(round(random.uniform(1000, 50000), 2)))
            else:
                starting_balance = Decimal(str(round(random.uniform(100, 5000), 2)))
        
        return {
            "account_id": f"{account_type.upper()}-{self.faker.random_number(digits=10)}",
            "account_type": account_type,
            "balance": starting_balance,
            "currency": "USD",
            "open_date": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
            "status": "active",
            "interest_rate": Decimal(str(round(random.uniform(0.01, 2.5), 2))) if account_type.lower() == "savings" else None
        }
    
    def generate_transaction(self, account_id, is_debit=None, amount=None, days_ago=None):
        """
        Generate a bank transaction
        
        :param account_id: ID of the account for the transaction
        :param is_debit: Whether the transaction is a debit (withdrawal)
        :param amount: Amount of the transaction (if None, a random amount is generated)
        :param days_ago: How many days ago the transaction occurred (if None, a random date is used)
        :return: Dictionary with transaction data
        """
        if is_debit is None:
            is_debit = random.choice([True, False])
        
        if amount is None:
            amount = Decimal(str(round(random.uniform(1, 1000), 2)))
        
        if days_ago is None:
            days_ago = random.randint(0, 90)
        
        transaction_date = datetime.now() - timedelta(days=days_ago)
        
        transaction_types = {
            True: ["ATM Withdrawal", "Debit Card Purchase", "Bill Payment", "Transfer Out", "Check"],
            False: ["Deposit", "Direct Deposit", "Interest Payment", "Transfer In", "Refund"]
        }
        
        description = random.choice(transaction_types[is_debit])
        if description == "Debit Card Purchase":
            merchants = ["Amazon", "Walmart", "Target", "Starbucks", "Netflix", "Uber", "Gas Station", "Restaurant", "Grocery Store"]
            description += f" - {random.choice(merchants)}"
        
        return {
            "transaction_id": f"TX-{self.faker.random_number(digits=12)}",
            "account_id": account_id,
            "date": transaction_date.strftime("%Y-%m-%d"),
            "amount": amount,
            "is_debit": is_debit,
            "description": description,
            "category": self._get_transaction_category(description),
            "balance_after": None,  # Would be calculated based on previous transactions
            "status": "cleared"
        }
    
    def _get_transaction_category(self, description):
        """
        Determine transaction category based on description
        
        :param description: Transaction description
        :return: Category string
        """
        description = description.lower()
        
        if "withdrawal" in description:
            return "Cash"
        elif "deposit" in description:
            return "Income"
        elif "interest" in description:
            return "Interest"
        elif "transfer" in description:
            return "Transfer"
        elif "bill payment" in description:
            return "Bill Payment"
        elif any(merchant in description.lower() for merchant in ["restaurant", "starbucks"]):
            return "Dining"
        elif any(merchant in description.lower() for merchant in ["amazon", "walmart", "target"]):
            return "Shopping"
        elif "netflix" in description:
            return "Entertainment"
        elif "uber" in description:
            return "Transportation"
        elif "gas" in description:
            return "Auto & Transport"
        elif "grocery" in description:
            return "Groceries"
        else:
            return "Miscellaneous"
    
    def generate_payee(self):
        """
        Generate a bill payment payee
        
        :return: Dictionary with payee data
        """
        company_name = self.faker.company()
        
        return {
            "payee_id": f"PAYEE-{self.faker.random_number(digits=8)}",
            "name": company_name,
            "nickname": company_name,
            "account_number": self.faker.random_number(digits=10),
            "routing_number": self.faker.random_number(digits=9),
            "address": {
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state(),
                "zipcode": self.faker.zipcode()
            },
            "phone": self.faker.phone_number(),
            "category": random.choice(["Utilities", "Housing", "Insurance", "Subscriptions", "Other"]),
            "last_payment_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "last_payment_amount": Decimal(str(round(random.uniform(10, 500), 2)))
        }
    
    def generate_test_data_set(self, num_users=3, num_accounts_per_user=2, num_transactions=50, num_payees=5):
        """
        Generate a complete test data set and save to JSON files
        
        :param num_users: Number of test users to generate
        :param num_accounts_per_user: Number of accounts per user
        :param num_transactions: Number of transactions to generate per account
        :param num_payees: Number of payees to generate
        """
        users = []
        accounts = []
        transactions = []
        payees = []
        
        # Generate users
        for i in range(num_users):
            with_2fa = i == 1  # Make one user have 2FA
            user = self.generate_user(with_2fa=with_2fa)
            users.append(user)
            
            # Generate accounts for each user
            for j in range(num_accounts_per_user):
                account_type = "checking" if j == 0 else "savings"
                account = self.generate_account(account_type=account_type)
                account["user_id"] = user["username"]
                accounts.append(account)
                
                # Generate transactions for each account
                for _ in range(num_transactions):
                    transaction = self.generate_transaction(account["account_id"])
                    transactions.append(transaction)
        
        # Generate payees
        for _ in range(num_payees):
            payee = self.generate_payee()
            payees.append(payee)
        
        # Save to JSON files
        self._save_json(users, "users.json")
        self._save_json(accounts, "accounts.json")
        self._save_json(transactions, "transactions.json")
        self._save_json(payees, "payees.json")
    
    def _save_json(self, data, filename):
        """
        Save data to a JSON file
        
        :param data: Data to save
        :param filename: Filename to save to
        """
        file_path = os.path.join(self.test_data_path, filename)
        
        # Convert decimal values to strings
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            raise TypeError
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, default=decimal_default)
            
        print(f"Saved {len(data)} records to {file_path}")


if __name__ == "__main__":
    # Example usage
    generator = DataGenerator()
    generator.generate_test_data_set()
    print("Test data generation complete!")
