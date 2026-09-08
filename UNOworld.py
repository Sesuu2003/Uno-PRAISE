from statebuffer import IStateBuffer
from environments import SimulatedEnvironment


class Card:
     def __init__(self, value, color):
          self.value = value
          self.color = color

class UNOEnvironment(SimulatedEnvironment):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self._agents_locations = {}
        self._hands = {}
        self._discardPile = []
        self._drawPile = []
        self._turn = int

    def add(self, agent_id: int) -> None:
        super(UNOEnvironment, self).add(agent_id)
        self._agents_locations[agent_id] = 0

    def remove(self, agent_id: int) -> None:
        super(UNOEnvironment, self).remove(agent_id)
        self._agents_locations.pop(agent_id, None)

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).add_statebuffer(agent_id, statebuffer)
        statebuffer.update({"agent_location": self._location_of(agent_id),
                            "hands": self._hands,
                            "discard_pile": self._discardPile,
                            "draw_pile": self._drawPile,
                            "turn": self._turn})

    def remove_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).remove_statebuffer(agent_id, statebuffer)

    def _location_of(self, agent_id: int) -> int:
            return self._agents_locations[agent_id] if agent_id in self._agents_locations else None

    def _top_discard(self) -> Card:
         return self._discardPile[-1]

    def get_property(self, agent_id: int, property_name: str) -> dict:
         if agent_id in self._agents:
            response = {"agent": agent_id}
            property_methods = {
                 "location" : self._location_of
            }

            property_method = property_methods.get(property_name)

            if property_method:
                 response[property_name] = property_method(agent_id)
            else:
                 print(f"Invalid property: {property_name}")

            return response
         else:
              return {}

    def _make_play(self, agent_id: int, card: Card):
         #quitar carta de la mano


         self._discardPile.append(card)

    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
         if agent_id in self._agents:
              action_methods = {
                   "play": (self._make_play, [])
              }
              action_method, expected_params = action_methods.get(action_name, (None, None))
              if action_method:
                   args = [agent_id] + [params.get(param) for param in expected_params]
                   action_method(*args)
                   self._update_statebuffers(agent_id)
              else:
                   print(f"Invalid action: {action_name}")

    def _update_statebuffers(self, agent_id: int):
         relevant_statebuffers = [entry["statebuffer"] for entry in self._statebuffers if entry["agent_id"] == agent_id]
         for statebuffer in relevant_statebuffers:
              statebuffer.update({
                   "agent_location": self._location_of(agent_id),
                   "hands": self._hands,
                   "discard_pile": self._discardPile,
                   "draw_pile": self._drawPile,
                   "turn": self._turn})








