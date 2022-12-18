from asyncio.queues import Queue
from json import dumps
from threading import Thread
import websockets
import asyncio

class WSServer:
    def __init__(self) -> None:
        self.last_state = None

    async def _accept_connection(self, websocket):
        self.connections.append(websocket)
        print(f"added connection")

        if self.last_state is not None:
            await websocket.send(self.last_state)

        try:
            await websocket.wait_closed()
        finally:
            self.connections.remove(websocket)

    async def _do_broadcast(self):
        el = await self.queue.get()
        print(f"broadcasting: {el}")
        websockets.broadcast(self.connections, el)

    async def _listen(self):
        self.queue = Queue()
        self.connections = []

        async with websockets.serve(self._accept_connection, "0.0.0.0", 8080):
            while True:
                await self._do_broadcast()

    def _thread_init_fn(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen())
        self.loop.run_forever()

    def start(self) -> None:
        self.thread = Thread(target=self._thread_init_fn, daemon=True)
        self.thread.start()

    async def send(self, el):
        if isinstance(el, dict):
            el = dumps(el)
        self.last_state = el
        await self.queue.put(el)
