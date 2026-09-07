from agents import Agent
from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
import uuid

# Temporalmente descartada 
# (¿Es necesario que el agente sepa que es su turno?
#  ¿o se lo indica el entorno?)
class TurnSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="turn")
        return response["turn"]

class DiscardPileSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="TopDiscard")
        return response["TopDiscard"]

class HandSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="hand")
        return response["hand"]

class CardDrawer(SimulatedActuator):
    def act(self):
        self._env.take_action(self._agent.id, "draw")


class CardPlayer(SimulatedActuator):
    def act(self, card):
        self._env.take_action(self._agent.id, "play", card)

class TurnPasser(SimulatedActuator):
    def act(self):
        self._env.take_action(self._agent.id, "pass")

@unique
class CardColor(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

class ColorDeclarer(SimulatedActuator):
    def act(self, color: CardColor):
        self._env.take_action(self._agent.id, "declareColor", color)


class PlayerAgent(Agent):
    def __init__(self, env: SimulatedEnvironment):
       super().__init__()
       env.add(self.id)

       discardPile = DiscardPileSensor(env)
       discardPile.agent = self
       self.add_sensor("discardPile", discardPile)

       hand = HandSensor(env)
       hand.agent = self
       self.add_sensor("hand", hand)

       drawer = CardDrawer(env)
       drawer.agent = self
       self.add_actuator("drawer", drawer)

       player = CardPlayer(env)
       player.agent = self
       self.add_actuator("player", player)

       passTurn = TurnPasser(env)
       passTurn.agent = self
       self.add_actuator("passTurn", passTurn)


    def function(self, percept):
        action = {}
        #recibir turno
        #escanear pila descarte
        #escanear mano
        #jugar o pedir
        card = self.compareCard(self, card, percept)
        if card != None:
            action["name"] = "play"
            action["params"] = card
        else:
        #pasar turno
            action["name"] = "pass"

        return action

    def compareCard(self, card, percept):
        mano = percept["hand"]
        for c in mano:
            if (card[0] == c[0] or card[1] == c[1]):
                return c
            else:
                return None

            
    
    def _percecive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)
        action_actuators = {}

        
    def behave(self):
        percept = self._perceive()
        self._act(percept)

