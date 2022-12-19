import os
import time

from spade import quit_spade
from spade_agents import SmartWatchAgent


def main():
    name = os.environ["AGENT_NAME"]
    password = os.environ["AGENT_PASSWORD"]
    xmpp = os.environ["XMPP"]

    agent = SmartWatchAgent(f"{name}@{xmpp}", password)
    agent.start().result()

    while True:
        time.sleep(1)

    agent.stop()
    quit_spade()
