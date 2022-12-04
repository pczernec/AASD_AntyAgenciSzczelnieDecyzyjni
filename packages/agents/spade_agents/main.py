import time
from spade_agents import DummyAgent

def main():
    dummy = DummyAgent("test@xmpp_server", "test")
    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    dummy.stop()

