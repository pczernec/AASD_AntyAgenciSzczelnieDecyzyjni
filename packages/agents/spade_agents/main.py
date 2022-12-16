from spade_agents import SmartWatchAgent
from spade import quit_spade
import os
import time

def main():
    name = os.environ['AGENT_NAME']
    password = os.environ['AGENT_PASSWORD']
    xmpp = os.environ['XMPP']

    agent = SmartWatchAgent(f"{name}@{xmpp}", password)
    agent.start().result()

    while agent.is_alive():
        time.sleep(1)

    agent.stop()
    quit_spade()
