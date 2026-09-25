from statebuffer import IStateBuffer, StateBuffer
from UNOworld import UNOEnvironment
import Pyro4

class UNOWorldPyroAdapter:
    def __init__(self, daemon, ns):
        self.unoenv = None
        self._daemon = daemon
        self._ns = ns
        self._buffers = {}

    @Pyro4.expose
    def build_env(self):
        self._unoenv = UNOEnvironment()

    @Pyro4.expose
    def create_statebuffer(self, agent_id: int) -> str:
