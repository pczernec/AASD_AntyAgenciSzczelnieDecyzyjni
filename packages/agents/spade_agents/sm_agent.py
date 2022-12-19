import json
import os
import random
import socket
import time
from asyncio.queues import Queue
from copy import copy
from dataclasses import asdict, dataclass
from typing import Tuple

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade_agents.ws import WSServer


@dataclass
class UserState:
    x: float
    y: float
    hp: float
    mana: float

    @staticmethod
    def default():
        return UserState(0, 0, 0, 0)


class UserStateEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, UserState):
            return asdict(z)
        else:
            return super().default(z)


SIM_STEP = 0.01


class SmartWatchAgent(Agent):
    class StateCollector(PeriodicBehaviour):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.state = UserState(
                x=random.random(),
                y=random.random(),
                hp=random.random(),
                mana=random.random(),
            )

        async def run(self) -> None:
            self.state.x += random.random() * SIM_STEP - SIM_STEP / 2
            self.state.y += random.random() * SIM_STEP - SIM_STEP / 2
            self.state.hp += random.random() * SIM_STEP - SIM_STEP / 2

            print(f"[[StateCollector]]: Fetching current user state: {self.state}")

            if self.last_state != self.state:
                await self.agent.state_broadcaster.my_user_state.put(self.state)
                self.last_state = copy(self.state)

        async def on_start(self) -> None:
            self.last_state = UserState.default()

    class StateBroadcaster(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.my_user_state = Queue()

        async def run(self) -> None:
            state = await self.my_user_state.get()
            print(f"[[StateBroadcaster]]: Got state from current user: {state}")

            msg = Message(
                to=f"broadcast@{os.environ['XMPP']}",
                metadata={"agent_id": socket.gethostname()},
            )
            msg.set_metadata("performative", "inform")
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
            if msg.metadata["agent_id"] != socket.gethostname():
                print(
                    f"[[StateReceiver]]: Received state: {state} from {msg.metadata['agent_id']}"
                )
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
            self.others_score = 0.0
            self.scores_list = []
            self.myscore: UserState = UserState.default()
            self.server = WSServer()

        async def run(self) -> None:
            el = await self.state_queue.get()

            if isinstance(el, UserState):
                self.myscore = el
            else:
                self.scores_list = el

            print(f"[[DangerNotifier]]: Received for calculation: {el}")

            states = [self.myscore] + self.scores_list
            await self.server.send(
                json.dumps(
                    {"scores": states, "myscore": self.myscore}, cls=UserStateEncoder
                )
            )

        async def on_start(self) -> None:
            self.server.start()

    async def setup(self) -> None:
        self.state_collector = self.StateCollector(period=1)
        self.add_behaviour(self.state_collector)
        self.state_broadcaster = self.StateBroadcaster()
        self.add_behaviour(self.state_broadcaster)
        self.state_receiver = self.StateReceiver()
        self.add_behaviour(self.state_receiver)
        self.danger_notifier = self.DangerNotifier()
        self.add_behaviour(self.danger_notifier)
