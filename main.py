from renderers import NullRenderer
from statebuffer import StateBuffer
from gamerenderer import ConsoleRenderer
from UNOworld import UNOEnvironment
from playeragent import PlayerAgent
import threading
import time

agent_finished_flag = False
event_render_ready = threading.Event()

def agent_thread(agent,id):
    global agent_finished_flag
    for _ in range(1000):
        if env.is_game_over():
            print("Game is over")
            break
        if id == 1:
            event_render_ready.wait(timeout=0.5)
        else:
            time.sleep(0.6)
        agent.behave()
        if id == 1:
            event_render_ready.clear()
    agent_finished_flag = True

def render_thread(renderer):
    while not agent_finished_flag:
        renderer.render()
        event_render_ready.set()

if __name__ == '__main__':
    env = UNOEnvironment(2)
    agent1 = PlayerAgent(env)
    agent2 = PlayerAgent(env)
    # agent3 = PlayerAgent(env)
    # agent4 = PlayerAgent(env)

    renderer = ConsoleRenderer()
    statebuffer = StateBuffer(agent1.id, env)
    env.add_statebuffer(agent1.id, statebuffer)
    renderer.observe(statebuffer=statebuffer)

    #print("agent id is: ",agent1.id)

    thread_agent1 = threading.Thread(target=agent_thread, args=(agent1, 1))
    thread_agent2 = threading.Thread(target=agent_thread, args=(agent2, 2))
    # thread_agent3 = threading.Thread(target=agent_thread, args=(agent3, 3))
    # thread_agent4 = threading.Thread(target=agent_thread, args=(agent4, 4))

    thread_renderer = threading.Thread(target=render_thread, args=(renderer,))

    thread_renderer.start()
    thread_agent1.start()
    thread_agent2.start()
    # thread_agent3.start()
    # thread_agent4.start()

    thread_agent1.join()
    thread_agent2.join()
    # thread_agent3.join()
    # thread_agent4.join()
    thread_renderer.join()