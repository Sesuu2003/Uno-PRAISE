import sys
import time
#import pygame
from renderers import IRenderer

class ConsoleRenderer(IRenderer):
    def __init__(self):
        self.environment_statebuffer = {}

    def observe(self, statebuffer):
        self.environment_statebuffer = statebuffer

    def render(self):
        state = self.environment_statebuffer.get_state()
        if state:

            print("[Round N°", state["round"],"]")
            print("Top Discard: ", state["discard_pile"])
            print("Jugador ", state["turn"], "| Action: ",state["play"])
            print("")
            print("---------------------------------------------------")
            print("")
            if state["winner"] != 0:
                print("Congratulations, Agent ", state["winner"],"! You won!")