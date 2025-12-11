import random

from statebuffer import IStateBuffer
from environments import SimulatedEnvironment

class UNOEnvironment(SimulatedEnvironment):
    def __new__(cls):
            return super().__new__(cls)

    def __init__(self):
        super(UNOEnvironment, self).__init__()
        self._agent_ids = []
        self._hands = {}
        self._deck = [] #mazo de cartas
        self._discard_pile = []
        self._current_player_index = 0
        self._direction = 1 #sentido de la ronda (1 o -1)
        self._current_color = None

    def add(self, agent_id: int) -> None:
        super(UNOEnvironment, self).add(agent_id)
        self._agents_locations[agent_id] = 0

    def remove(self, agent_id: int) -> None:
        super(UNOEnvironment, self).remove(agent_id)
        self._agents_locations.pop(agent_id, None)

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).add_statebuffer(agent_id, statebuffer)
        statebuffer.update({"length": self._length, "agent_location": self._location_of(agent_id),
                         "dirt_location": self._dirt_locations})

    def remove_statebuffer(self, agent_id: int,statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).remove_statebuffer(agent_id, statebuffer)

    def _location_of(self, agent_id: int) -> int:
        return self._agents_locations[agent_id] if agent_id in self._agents_locations else None

    def get_property(self, agent_id: int, property_name: str) -> dict:
        if agent_id in self._agent_ids:
            response = {"agent": agent_id}

            property_methods = {
                "hand": self._hands[agent_id],
                "your_turn": agent_id== self._agent_ids[self._current_player_index],
                "top_discard": self._discardpile[-1],
                "current_color": self._current_color,
                
            }
            
            property_method = property_methods.get(property_name)

            if property_method:
                response[property_name] = property_method(agent_id)
            else:
                print(f"Invalid property: {property_name}")

            return response
        else:
            return {}
        
    def _play_card(self, agent_id:int, card):
        #validar, mover al descarte, aplicar sus efectos
        self._advance_turn()
        
    def _draw_card(self, agent_id:int):
        card = self._deck.pop()
        self._hands[agent_id].append(card)
        self._advance_turn()
        
    def _advance_turn(self):
        self._current_player_index = (self._current_player_index + self._direction)

    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
        if agent_id in self._agents:
            action_methods = {
                "play_card": (self._play_card(agent_id, params["card"])),
                "draw_card":(self._draw_card(agent_id)),
                "declare_color":(self._current_color = params["color"]),
                "pass":(self._advance_turn())
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
            statebuffer.update({"length": self._length, "agent_location": self._location_of(agent_id),
                             "dirt_location": self._dirt_locations})