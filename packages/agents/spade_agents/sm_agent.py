from asyncio.futures import Future
from asyncio.queues import Queue
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from dataclasses import asdict, dataclass
import random
import os
import json
import time

from spade.message import Message

@dataclass
class UserState:
    hp: float
    mana: float
    at: float

class SmartWatchAgent(Agent):
    class StateCollector(PeriodicBehaviour):
        async def run(self) -> None:
            state = UserState(hp=random.random(), mana=random.random(), at=random.random())
            print(f"[[StateCollector]]: Fetching current user state: {state}")

            if self.last_state != state:
                await self.agent.state_broadcaster.myuser_state.put(state)
                self.last_state = state

        async def on_start(self) -> None:
            self.last_state = UserState(0, 0, 0)

    class StateBroadcaster(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.myuser_state = Queue()

        async def run(self) -> None:
            state = await self.myuser_state.get()
            print(f"[[StateBroadcaster]]: Got state from current user: {state}")

            msg = Message(to=f"broadcast@{os.environ['XMPP']}")
            msg.set_metadata('performative', 'inform')
            msg.body = json.dumps(asdict(state))
            await self.send(msg)
            await self.agent.danger_notifier.state_queue.put(state)

    class StateReceiver(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.last_time = 0
            self.user_states = []

        async def run(self) -> None:
            msg = await self.receive(timeout=100)
            while not msg:
                msg = await self.receive(timeout=100)

            state = UserState(**json.loads(msg.body))
            if not str(msg.sender).startswith(f"{self.agent.name}@"):
                print(f"[[StateReceiver]]: Received state: {state} from {msg.sender}")
                self.user_states.append(state)

                t = time.time()
                if t - self.last_time > 10:
                    print(f"[[StateReceiver]]: batching state {self.user_states}")
                    await self.agent.danger_notifier.state_queue.put(self.user_states)
                    self.user_states = []
                    self.last_time = t

    class DangerNotifier(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.state_queue = Queue()

        async def run(self) -> None:
            el = await self.state_queue.get()
            print(f"[[DangerNotifier]]: Received for calculation: {el}")


    async def setup(self) -> None:
        self.state_collector = self.StateCollector(period=1)
        self.add_behaviour(self.state_collector)
        self.state_broadcaster = self.StateBroadcaster()
        self.add_behaviour(self.state_broadcaster)
        self.state_receiver = self.StateReceiver()
        self.add_behaviour(self.state_receiver)
        self.danger_notifier = self.DangerNotifier()
        self.add_behaviour(self.danger_notifier)
