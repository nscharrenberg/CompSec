import aiofiles
import json


class FileUtil:
    def __init__(self, file_path, is_json=True):
        self.file_path = file_path
        self.is_json = is_json

    # Read data from specified file
    async def read(self):
        async with aiofiles.open(self.file_path, mode='r') as file:
            contents = await file.read()

        if self.is_json:
            return json.loads(contents)
        else:
            return contents

    # Write data to specified file
    async def write(self, data):
        async with aiofiles.open(self.file_path, mode='w') as file:
            if self.is_json:
                content = json.dumps(data)
            else:
                content = data
            await file.write(content)

        return content