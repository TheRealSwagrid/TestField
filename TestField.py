import signal
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer


class TestField(AbstractVirtualCapability):

    def __init__(self, server):
        super().__init__(server)

    def execute_command(self, command: dict):
        if command["capability"] is "GetTestFieldBoundaries":
            pass
        elif command["capability"] is "SetTestFieldBoundaries":
            pass

    def loop(self):
        sleep(5)
        self.send_message({"alive":True})


if __name__ == "__main__":
    # Needed for properly closing when process is being stopped with SIGTERM signal
    def handler(signum, frame):
        print("[Main] Received SIGTERM signal")
        listener.kill()
        quit(1)

    try:
        server = VirtualCapabilityServer()
        listener = TestField(server)
        listener.start()
        signal.signal(signal.SIGTERM, handler)
        listener.join()
        # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")
        listener.kill()
