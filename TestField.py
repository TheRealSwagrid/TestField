import signal
import sys
import pickle
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer


class TestField(AbstractVirtualCapability):

    def __init__(self, server):
        super().__init__(server)
        self.TestFieldBoundaries = [[0., 0., 0.], [0., 0., 0.]]
        try:
            self.TestFieldBoundaries = pickle.load("TestFieldBoundaries")
        except:
            pass

    def GetTestFieldBoundaries(self, params: dict) -> dict:
        return {"TestFieldPointA": self.TestFieldBoundaries[0],
                "TestFieldPointB": self.TestFieldBoundaries[1]}

    def SetTestFieldBoundaries(self, params: dict) -> dict:
        self.TestFieldBoundaries[0] = params["TestFieldPointA"]
        self.TestFieldBoundaries[1] = params["TestFieldPointB"]
        pickle.dump("TestFieldBoundaries", self.TestFieldBoundaries)
        return self.GetTestFieldBoundaries(params)

    def loop(self):
        pass


if __name__ == "__main__":
    # Needed for properly closing when process is being stopped with SIGTERM signal
    def handler(signum, frame):
        print("[Main] Received SIGTERM signal")
        listener.kill()
        quit(1)

    try:
        port = None
        if len(sys.argv[1:]) > 0:
            port = int(sys.argv[1])
        server = VirtualCapabilityServer(port)
        listener = TestField(server)
        listener.start()
        signal.signal(signal.SIGTERM, handler)
        listener.join()
        # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")
        server.kill()
        listener.kill()

