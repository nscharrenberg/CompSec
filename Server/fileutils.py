import aiofiles
import json


class FileUtil:
    def __init__(self, file_path):
        self.file_path = file_path

    # Read data from specified file
    async def read(self):
        async with aiofiles.open(self.file_path, mode='r') as file:
            contents = await file.read()

        return json.loads(contents)

    # Write data to specified file
    async def write(self, data):
        async with aiofiles.open(self.file_path, mode='w') as file:
            await file.write(json.dumps(data))

        return data
