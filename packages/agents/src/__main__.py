import os
import sys
import time
from pathlib import Path

from spade import quit_spade  # noqa

# Add `packages` dir to path to allow import of `constants`
sys.path.insert(1, str(Path(__file__).parent.parent.parent.absolute()))

from .sm_agent import SmartWatchAgent


def main():
    name = os.environ["AGENT_NAME"]
    password = os.environ["AGENT_PASSWORD"]
    xmpp = os.environ["XMPP"]

    agent = SmartWatchAgent(f"{name}@{xmpp}", password)
    agent.start().result()

    while agent.is_alive():
        time.sleep(1)

    agent.stop()
    quit_spade()


main()
