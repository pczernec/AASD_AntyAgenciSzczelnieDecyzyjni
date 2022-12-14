import asyncio
import json
import os
from threading import Thread

import websockets

from constants.constants import Constants as C


class WSServer:
    def __init__(self) -> None:
        self.thread = None
        self.loop = None
        self.connections = []
        self.state_history = []

    async def _accept_connection(self, websocket):
        self.connections.append(websocket)
        print("added connection")

        await websocket.send(json.dumps(self.state_history))

        try:
            await websocket.wait_closed()
        finally:
            self.connections.remove(websocket)

    async def _listen(self):
        async with websockets.serve(
            self._accept_connection, "0.0.0.0", os.environ["NOTIFY_PORT"]
        ):
            await asyncio.Future()  # run forever

    def _thread_init_fn(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen())
        self.loop.run_forever()

    def start(self) -> None:
        self.thread = Thread(target=self._thread_init_fn, daemon=True)
        self.thread.start()

    async def send(self, el):
        self.state_history = self.state_history[-C.HISTORY_LEN :] + [el]

        el = json.dumps([el])
        print(f"broadcasting: {el}")
        websockets.broadcast(self.connections, el)
