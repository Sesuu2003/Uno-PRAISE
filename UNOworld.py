from statebuffer import IStateBuffer
from environments import SimulatedEnvironment
from enum import Enum, unique
import random

@unique
class RoundDirection(Enum):
    RIGHT = 1
    LEFT = -1

@unique
class CardColor(Enum):
    RED = "Red"
    BLUE = "Blue"
    GREEN = "Green"
    YELLOW = "Yellow"
    WILD = "Wild"

@unique
class CardValue(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    REVERSE = "Reverse"
    SKIP = "Skip"
    DRAW_TWO = "+2"
    DRAW_FOUR = "+4"
    WILD_CARD = "Wild Card"

    @property
    def copies_per_color(self) -> int:
        if self == CardValue.ZERO:
            return 1
        elif self in (CardValue.DRAW_FOUR, CardValue.WILD_CARD):
            return 0
        return 2


class Card:
    def __init__(self, value: CardValue, color: CardColor):
        self.value = value
        self.color = color
    def __repr__(self):
        return f"[{self.color.value} {self.value.value}]"

class UNOEnvironment(SimulatedEnvironment):
    # def __new__(cls):
    #     return super().__new__(cls)

    def __init__(self, maxplayers = 4):
        super().__init__()
        self._hands = {}
        self._discardPile = []
        self._drawPile = []
        self._turn = 1
        self._deck = []
        self._round = 1
        self._roundDirection = 1
        self._play = ""
        self._create_deck()
        self._create_drawPile(self._deck)
        self._start_discard_pile()
        self._winner = 0
        self._maxplayers = maxplayers #controlar
        self._turns = {}

    def add(self, agent_id: int) -> None:
        if len(self._agents) < self._maxplayers:
            super(UNOEnvironment, self).add(agent_id)
            self._hands[agent_id] = []
            self._turns[agent_id] = len(self._turns) +1
            print("Agent", self._turns[agent_id]," Joined!")
            self._give_hands(agent_id)
            print("Agent", self._turns[agent_id],"'s hand is: ", self._hands[agent_id])

    def remove(self, agent_id: int) -> None:
        super(UNOEnvironment, self).remove(agent_id)

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).add_statebuffer(agent_id, statebuffer)
        statebuffer.update({
                            "hands": self._hands,
                            "discard_pile": self._discardPile[-3:],
                            "draw_pile": self._drawPile,
                            "turn": self._turn,
                            "round": self._round,
                            "play": self._play,
                            "turns": self._turns,
                            "winner": self._winner
                            })

    def remove_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(UNOEnvironment, self).remove_statebuffer(agent_id, statebuffer)


    def _top_discard(self, agent_id) -> Card:
        return self._discardPile[-1]

    def _get_agent_hand(self, agent_id):
        return self._hands[agent_id]

    def get_property(self, agent_id: int, property_name: str) -> dict:
            if agent_id in self._agents:
                response = {"agent": agent_id}
                property_methods = {
                    "topDiscard": self._top_discard,
                    "hand": self._get_agent_hand
                }
                property_method = property_methods.get(property_name)
                if property_method:
                     response[property_name] = property_method(agent_id)

                else:
                    print(f"Invalid property: {property_name}")
                return response
            else: return {}

    def _make_play(self, agent_id: int, card: Card):
        self._hands[agent_id].remove(card)
        self._discardPile.append(card)
        self._play = "played card"
        if card.value == CardValue.REVERSE:
            self._roundDirection *= (-1)
        self._next_turn()

    def _create_deck(self):
        standard_colors = [c for c in CardColor if c!= CardColor.WILD]
        for color in standard_colors:
            for value in CardValue:
                for r in range(value.copies_per_color):
                    self._deck.append(Card(value, color))
        for wild_value in (CardValue.DRAW_FOUR, CardValue.WILD_CARD):
            for r in range(4):
                self._deck.append(Card(wild_value, CardColor.WILD))

    def _create_drawPile(self, deck):
        self._drawPile = deck
        random.shuffle(self._drawPile)

    def _give_hands(self, agent_id):
        hand = []
        for i in range(1,3):
            hand.append(self._drawPile.pop())
        self._hands[agent_id] = hand
        #respetar orden real

    def _start_discard_pile(self):
        self._discardPile.append(self._drawPile.pop())

    def _next_turn(self):
        if self._turn+self._roundDirection > len(self._turns):
            self._turn = 1
        elif self._turn+self._roundDirection < 1:
            self._turn = len(self._turns)
        else:
            self._turn += self._roundDirection



    def _pass_turn(self, agent_id):
        self._play = "pass"
        self._next_turn()

    def is_game_over(self) -> bool:
        return self._winner != 0

    def check_turn(self, agent_id):
        #if self._winner != 0:
        #    return False
        return ( (len(self._hands[agent_id]) > 0) and (self._turn == self._turns[agent_id]) )

    def _restock_piles(self):
        self._drawPile = self._discardPile[:-1]
        random.shuffle(self._drawPile)
        self._discardPile = [self._discardPile[-1]]

    def _draw_card(self, agent_id: int):
        card = self._drawPile.pop()
        self._play = "drawn card"
        self._hands[agent_id].append(card)
        if len(self._drawPile) <= 1:
            self._restock_piles()
        self._next_turn()


    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
        if agent_id in self._agents and self.check_turn(agent_id):
            action_methods = {
                "play": (self._make_play, ["card", "colorChoice"]),
                "pass": (self._pass_turn, []),
                "draw": (self._draw_card, [])
            }
            action_method, expected_params = action_methods.get(action_name, (None, None))
            if action_method:
                args = [agent_id] + [params.get(param) for param in expected_params]
                action_method(*args)
                if len(self._hands[agent_id]) == 0:
                    self._winner = self._turns[agent_id]
                self._update_statebuffers(agent_id)
            else:
                print(f"Invalid action: {action_name}")

    def _update_statebuffers(self, agent_id: int):
        relevant_statebuffers = [entry["statebuffer"] for entry in self._statebuffers if entry["agent_id"] == agent_id]
        for statebuffer in relevant_statebuffers:
            statebuffer.update({
                "hands": self._hands,
                "discard_pile": self._discardPile[-3:],
                "draw_pile": self._drawPile,
                "turn": self._turn,
                "round": self._round,
                "play": self._play,
                "turns": self._turns,
                "winner": self._winner})









