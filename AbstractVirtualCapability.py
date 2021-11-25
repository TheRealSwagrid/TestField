import json
import os
import socket
import sys
from abc import abstractmethod
from subprocess import Popen
from threading import Thread
from time import sleep


def formatPrint(c, string: str) -> None:
    """Prints the given string in a formatted way: [Classname] given string

    Parameters:
        c       (class)  : The class which should be written inside the braces
        string  (str)    : The String to be printed
    """
    sys.stderr.write(f"[{type(c).__name__}] {string}\n")


class NoConnectionException(Exception):
    pass


class CommandNotFoundException(Exception):
    pass


class WrongNumberOfArgumentsException(Exception):
    pass


class VirtualCapabilityServer(Thread):
    '''Server meant to be run inside of a docker container as a Thread.

    '''

    def __init__(self, connectionPort: int = None):
        super().__init__()
        self.connectionPort = 9999
        self.running = False
        self.connected = False
        self.virtualCapabilities = list()
        formatPrint(self, "initialized")

    def run(self) -> None:
        formatPrint(self, "started")
        self.running = True
        formatPrint(self, f"Connecting on 0.0.0.0, {self.connectionPort}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", self.connectionPort))
        self.socket.listen(1)
        self.sock, self.adr = self.socket.accept()
        self.connected = True
        formatPrint(self, f"connected on {str(self.sock)}")
        while self.running:
            self.loop()

    def loop(self) -> None:
        try:
            data = self.sock.recv(512)
            if data != b'':
                # print("[Server] received: " + str(data))
                try:
                    self.message_received(data.decode())
                except Exception as e:
                    self.send_message(f"ERROR: {repr(e)}")
        except:
            pass

    def message_received(self, msg: str):
        if msg == "kill":
            # Kill the container
            Popen(["pkill", "python"])
        for vc in self.virtualCapabilities:
            vc.execute_command(json.loads(msg))

    def send_message(self, msg: str):
        if self.connected:
            formatPrint(self, f"Sending {msg}")
            self.sock.send(msg.encode("UTF-8"))

    def addVirtualCapability(self, vc):
        self.virtualCapabilities.append(vc)

    def kill(self):
        self.running = False
        self.socket.close()
        self.socket.shutdown(socket.SHUT_RDWR)


class AbstractVirtualCapability(Thread):
    def __init__(self, server: VirtualCapabilityServer):
        Thread.__init__(self)
        self.uri = None
        self.dynamix = {}
        self.dev_name = None
        self.server = server
        self.server.addVirtualCapability(self)
        self.running = True

    def run(self) -> None:
        self.server.start()
        formatPrint(self, "starting...")
        while self.running:
            self.loop()

    def execute_command(self, command: dict):
        formatPrint(self, f"Got Command {command}")
        ret = {"type":"respond",
               "capability":command["capability"],
               "src":command["src"]
               }
        params = {}

        for p in command["parameters"]:
            params[p["uri"]] = p["content"]
        params = self.__getattribute__(command["capability"])(params)

        ret["parameters"] = [{"uri": p, "content":params[p]} for p in params.keys()]
        formatPrint(self, f"Executed Command {ret}")
        self.send_message(ret)

    @abstractmethod
    def loop(self):
        raise NotImplementedError

    def send_message(self, command: dict):
        self.server.send_message(json.dumps(command))

    def kill(self):
        self.server.kill()
