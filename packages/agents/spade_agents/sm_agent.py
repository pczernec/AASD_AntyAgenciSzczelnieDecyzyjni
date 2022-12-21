import json
import os
import random
import socket
import time
import math
from asyncio.queues import Queue
from copy import copy
from dataclasses import asdict, dataclass

import numpy as np
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

from .ws import WSServer


@dataclass
class UserState:
    x: float
    y: float
    hp: float
    angle: float
    velocity: float

    @staticmethod
    def default():
        return UserState(0, 0, 0, 0, 0)


class UserStateEncoder(json.JSONEncoder):
    def default(self, z):
        return asdict(z) if isinstance(z, UserState) else super().default(z)


SIM_STEP = 0.1


class SmartWatchAgent(Agent):
    class StateCollector(PeriodicBehaviour):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.last_state = UserState.default()
            self.state = UserState(
                x=random.random(),
                y=random.random(),
                hp=0.5 + random.random() / 2 * random.choice([-1, 1]),
                angle=random.random()*math.pi*2 - math.pi,
                velocity=random.random(),
            )

        async def run(self) -> None:

            radians = random.random()*math.pi*2 - math.pi
            velocity = 1-min((2 * math.pi) - abs(radians - self.state.angle), abs(radians - self.state.angle)) / math.pi
            self.state.x += math.sin(radians * math.pi)*velocity * SIM_STEP
            self.state.y += math.cos(radians * math.pi)*velocity * SIM_STEP
            self.state.angle = radians
            self.state.velocity = velocity
            
            if self.state.x < 0.0:
                self.state.x = 0.0
            if self.state.x > 1.0:
                self.state.x = 1.0
            
            if self.state.y < 0.0:
                self.state.y = 0.0
            if self.state.y > 1.0:
                self.state.y = 1.0

            rand_hp_factor = random.random()
            if rand_hp_factor < 0.1:
                hp_change_scale = 3.0
            else:
                hp_change_scale = 1.0
            self.state.hp += hp_change_scale*(rand_hp_factor-self.state.hp)*SIM_STEP
            if self.state.hp < 0.0:
                self.state.hp = 0.0
            if self.state.hp > 1.0:
                self.state.hp = 1.0

            print(f"[[StateCollector]]: Fetching current user state: {self.state}")

            if self.last_state != self.state:
                await self.agent.state_broadcaster.my_user_state.put(self.state)
                self.last_state = copy(self.state)

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
        SMALL_DANGER = 0.2
        MEDIUM_DANGER = 0.5
        RUN_TYPE_OF_DANGER = 0.8

        DANGER_THRESHOLD = 0.4
        ZONE_AREA_RADIUS = 0.3

        def __init__(self):
            super().__init__()
            self.state_queue = Queue()
            self.others_score = 0.0
            self.states_list = []
            self.my_state: UserState = UserState.default()
            self.my_state: UserState = UserState.default()
            self.my_zone_danger_score = self.SMALL_DANGER
            self.server = WSServer()

        async def run(self) -> None:
            el = await self.state_queue.get()

            if isinstance(el, UserState):
                self.my_state = el
            else:
                self.states_list = el

            print(f"[[DangerNotifier]]: Received for calculation: {el}")

            states = [self.my_state] + self.states_list

            if self.states_list:
                # filter based on distance
                my_location = np.array([self.my_state.x, self.my_state.y])
                others_locations = np.vstack([
                    [s.x for s in self.states_list],
                    [s.y for s in self.states_list],
                ]).T

                results = (np.linalg.norm(others_locations[:, :2] - my_location, axis=1) <= self.ZONE_AREA_RADIUS)
                agents_in_zone = [state for state, in_zone in zip(self.states_list, results) if in_zone]

                agents_in_danger = sum([s.hp < self.DANGER_THRESHOLD for s in agents_in_zone])

                if agents_in_danger <= 1:
                    self.my_zone_danger_score = self.SMALL_DANGER
                elif agents_in_danger <= 3:
                    self.my_zone_danger_score = self.MEDIUM_DANGER
                else:
                    self.my_zone_danger_score = self.RUN_TYPE_OF_DANGER

            await self.server.send(
                json.dumps(
                    {
                        "states": states,
                        "my_score": states[0].hp,
                        "area_danger": self.my_zone_danger_score,
                    },
                    cls=UserStateEncoder,
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
