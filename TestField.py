import signal
import sys
import pickle
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint


class TestField(AbstractVirtualCapability):

    def __init__(self, server):
        super().__init__(server)
        self.TestFieldBoundaries = [[2., -2., 0.], [-2., 2., 0.]]
        '''
        try:
            self.TestFieldBoundaries = pickle.loads("TestFieldBoundaries")
        except:
            pickle.dumps("TestFieldBoundaries", self.TestFieldBoundaries)
        '''
        formatPrint(self, f"positions : {self.TestFieldBoundaries}")

    def GetTestFieldBoundaries(self, params: dict) -> dict:
        #formatPrint(self, f"Sending TestFieldBountaries: {self.TestFieldBoundaries}")
        return {"TestFieldPointA": self.TestFieldBoundaries[0],
                "TestFieldPointB": self.TestFieldBoundaries[1]}

    def SetTestFieldBoundaries(self, params: dict) -> dict:
        self.TestFieldBoundaries[0] = params["TestFieldPointA"]
        self.TestFieldBoundaries[1] = params["TestFieldPointB"]
        #pickle.dump("TestFieldBoundaries", self.TestFieldBoundaries)
        return self.GetTestFieldBoundaries(params)

    def loop(self):
        pass


if __name__ == "__main__":
    try:
        port = None
        if len(sys.argv[1:]) > 0:
            port = int(sys.argv[1])
        server = VirtualCapabilityServer(port)
        tf = TestField(server)
        tf.start()
        while server.running:
            pass
        # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")


