import asyncio
from fileutils import FileUtil
from transactionmanager import TransactionManager
import rsa

counter_file_path = 'counter.json'

async def main():
    program = Program()
    await program.start()
    await program.increase("1", "1", 50)
    await program.get_data("1")



# Basic Usage of the transactionmanager logic -> Take as inspiration for the websocket logic
class Program:
    def __init__(self):
        self.public_util = None
        self.private_util = None
        self.file_utils = None

    async def start(self):
        self.private_util = FileUtil('private.pem', is_json=False)
        self.public_util = FileUtil('public.pem', is_json=False)

        private_key = await self.private_util.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        public_key = await self.public_util.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.file_utils = TransactionManager(counter_file_path, private_key, public_key)

    # Util function to generate public and private keys
    async def generate_keys(self):
        public_key, private_key = rsa.newkeys(1024)

        await self.private_util.write(private_key.save_pkcs1().decode(), is_json=False)
        await self.public_util.write(public_key.save_pkcs1().decode(), is_json=False)

    async def get_data(self, user_id):
        print("--------------------", user_id, "--------------------")
        user_data = await self.file_utils.get_user_transactions(user_id)
        print(user_data)

        user_data = await self.file_utils.get_user_balance(user_id)
        print(user_data)

    async def increase(self, user_id, session_id, value):
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "value": value
        }

        await self.file_utils.increase(data)

    async def decrease(self, user_id, session_id, value):
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "value": value
        }

        await self.file_utils.decrease(data)


#asyncio.run(main())
