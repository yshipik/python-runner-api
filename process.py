import asyncio
import subprocess
import sys
import ptyprocess
class Process:
    body: ptyprocess.PtyProcessUnicode
    output_queue: asyncio.Queue
    def __init__(self, filename):
        self.body = ptyprocess.PtyProcessUnicode.spawn(["python3", filename], echo=False)
    async def read_output(self):
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, self.body.read)
            return line
    async def write_data(self, message: str):
        if "\n" not in message:
            message += "\n"
        self.body.write(message)
    