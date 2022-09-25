import aiofiles
import asyncio
import json

counter_file_path = 'counter.json'


async def main():
    print(await get_all_user_data())
    await decrease("1", 5)
    await increase("1", 10)
    await increase("2", 5)


async def get_all_user_data():
    async with aiofiles.open(counter_file_path, mode='r') as file:
        contents = await file.read()

    return json.loads(contents)


async def decrease(ID, value):
    data = await get_all_user_data()
    balance = data[ID]

    try:
        new_balance = balance - value
    except Exception:
        raise Exception("The value to decrease must be a valid decimal number")

    if new_balance < 0:
        raise Exception("Balance can not be negative!")

    data[ID] = new_balance

    async with aiofiles.open(counter_file_path, mode='w') as file:
        await file.write(json.dumps(data))

    print(f"{value} has been removed from your balance. It is now {new_balance}")

    # TODO: Update clients through sockets


async def increase(ID, value):
    data = await get_all_user_data()
    balance = data[ID]

    try:
        new_balance = balance + value
    except Exception:
        raise Exception("The value to increase must be a valid decimal number")

    data[ID] = new_balance

    async with aiofiles.open(counter_file_path, mode='w') as file:
        await file.write(json.dumps(data))

    print(f"{value} has been added to your balance. It is now {new_balance}")

    # TODO: Update clients through sockets

asyncio.run(main())
