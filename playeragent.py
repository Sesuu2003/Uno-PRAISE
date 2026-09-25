from agents import Agent
from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
import uuid
from UNOworld import Card

# Temporalmente descartada
# (¿Es necesario que el agente sepa que es su turno?
#  ¿o se lo indica el entorno?)
class TurnSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="turn")
        return response["turn"]

class DiscardPileSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="topDiscard")
        return response["topDiscard"]

class HandSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="hand")
        return response["hand"]

class DrawActuator(SimulatedActuator):
    def act(self):
        self._env.take_action(self._agent.id, "draw")


class PlayActuator(SimulatedActuator):
    def act(self, card: Card):
        request_info = {"card": card}
        self._env.take_action(self._agent.id, "play", request_info)

class PassActuator(SimulatedActuator):
    def act(self):
        self._env.take_action(self._agent.id, "pass")



from enum import Enum, unique
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

       drawer = DrawActuator(env)
       drawer.agent = self
       self.add_actuator("drawer", drawer)

       player = PlayActuator(env)
       player.agent = self
       self.add_actuator("player", player)

       passTurn = PassActuator(env)
       passTurn.agent = self
       self.add_actuator("passTurn", passTurn)


    def compareCard(self, percept):
        hand = percept["hand"]
        card = percept["discardPile"]
        for c in hand:
            if (card.value == c.value or card.color == c.color):
                return c
        return None

    def function(self, percept):
        action = {}
        card = self.compareCard(percept)
        if card != None:
            action["name"] = "play"
            action["params"] = {"card": card}
        else:
            action["name"] = "draw"
        return action


    def print_state(self):
        print("Me quedan {} cartas".format(len(self._sensors["hand"].sense())))

    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)
        action_actuators = {
            "play": (self._actuators["player"], ["card"]),
            "draw": (self._actuators["drawer"], []),
            "pass": (self.actuators["passTurn"], [])
        }
        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)
    def behave(self):
        percept = self._perceive()
        self._act(percept)

