import signal
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer


class TestField(AbstractVirtualCapability):

    def __init__(self, server):
        super().__init__(server)
        self.TestFieldBoundaries = [[0., 0., 0.], [0., 0., 0.]]

    def execute_command(self, command: dict):
        respond = {
            "type": "respond"
        }
        if command["capability"] == "GetTestFieldBoundaries":
            respond["capability"] = "GetTestFieldBoundaries"
            respond["parameters"] = [{"uri": "TestFieldPointA", "content": self.TestFieldBoundaries[0]},
                                     {"uri": "TestFieldPointB", "content": self.TestFieldBoundaries[1]}]
        elif command["capability"] == "SetTestFieldBoundaries":
            for p in command["parameters"]:
                if p["uri"] == "TestFieldPointA":
                    self.TestFieldBoundaries[0] = p["content"]
                elif p["uri"] == "TestFieldPointB":
                    self.TestFieldBoundaries[1] = p["content"]
            respond["capability"] = "SetTestFieldBoundaries"
            respond["parameters"] = [{"uri": "TestFieldPointA", "content": self.TestFieldBoundaries[0]},
                                     {"uri": "TestFieldPointB", "content": self.TestFieldBoundaries[1]}]

        self.send_message(respond)

    def loop(self):
        self.send_message({"HEY!": "alive"})
        sleep(2)
        pass


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
