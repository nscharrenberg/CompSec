import base64
import sys

import aiofiles
import json
from fileutils import FileUtil
import rsa


class TransactionManager:
    def __init__(self, file_path, private_key, public_key):
        private_key = open(private_key, "r").read().encode('utf-8')
        self.private_key = rsa.PrivateKey.load_pkcs1(private_key)
        public_key = open(public_key, "r").read().encode('utf-8')
        self.public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.file_path = file_path
        self.file_utils = FileUtil(file_path)

    # Append a transaction to the file
    async def append(self, record):
        data = await self.file_utils.read()
        transactions = data['transactions']
        transactions.append(record)

        async with aiofiles.open(self.file_path, mode='w') as file:
            await file.write(json.dumps({"transactions": transactions}))

    # Get all the transactions of a specific user
    async def get_user_transactions(self, user_id):
        file_data = await self.file_utils.read()
        file_data = file_data['transactions']

        transactions = []

        for key, element in enumerate(file_data):
            decrypted_user_id = self.decrypt(element['user_id'])
            if decrypted_user_id == user_id:
                transactions.append({
                    "user_id": decrypted_user_id,
                    "session_id": self.decrypt(element['session_id']),
                    "old_balance": self.decrypt(element['old_balance'], is_numeric=True),
                    "action": self.decrypt(element['action']),
                    "value": self.decrypt(element['value'], is_numeric=True)
                })

        return transactions

    # Get the balance of a specific user
    async def get_user_balance(self, user_id):
        transactions = await self.get_user_transactions(user_id)

        balance = 0

        for key, element in enumerate(transactions):
            if element['action'] == 'increase':
                balance += element['value']
            elif element['action'] == 'decrease':
                balance -= element['value']
            else:
                raise Exception("Invalid action performed while calculating balance")

        return balance

    async def increase(self, data):
        user_id = data['user_id']
        value = data['value']

        if int(value) > sys.maxsize or int(value) < 0:
            raise Exception("Value has exceeded the limit")

        balance = await self.get_user_balance(user_id)

        try:
            formatted_value = float(value)
        except Exception:
            raise Exception("Given value must be a numeric value")

        transaction = {
            "user_id": self.encrypt(data['user_id']),
            "session_id": self.encrypt(data['session_id']),
            "old_balance": self.encrypt(balance, is_numeric=True),
            "action": self.encrypt("increase"),
            "value": self.encrypt(value, is_numeric=True)
        }

        await self.append(transaction)

    async def decrease(self, data):
        user_id = data['user_id']
        value = data['value']
        balance = await self.get_user_balance(user_id)

        if int(value) > sys.maxsize or int(value) < 0:
            raise Exception("Value has exceeded the limit")

        try:
            formatted_value = float(value)
        except Exception:
            raise Exception("Given value must be a numeric value")

        new_balance = balance - formatted_value

        if new_balance < 0:
            raise Exception("You can not decrease the value as much as to get a negative balance.")

        transaction = {
            "user_id": self.encrypt(data['user_id']),
            "session_id": self.encrypt(data['session_id']),
            "old_balance": self.encrypt(balance, is_numeric=True),
            "action": self.encrypt("increase"),
            "value": self.encrypt(value, is_numeric=True)
        }

        await self.append(transaction)

    # Encrypt the plain data such that it can be stored on the logs
    def encrypt(self, data, is_numeric=False):
        if is_numeric:
            element = str(data)
        else:
            element = data

        return base64.b64encode(rsa.encrypt(element.encode('utf-8'), self.public_key)).decode('utf-8')

    # Decrypt the encrypted data such that the server can read it
    def decrypt(self, data, is_numeric=False):
        decoded = rsa.decrypt(base64.b64decode(data), self.private_key).decode("utf-8")

        if is_numeric:
            element = int(decoded)
        else:
            element = decoded

        return element

