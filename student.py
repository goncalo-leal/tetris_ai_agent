import asyncio
from asyncio.tasks import sleep
import getpass
import json
import os
from grid import Grid

from my_shapes import *
from next_solution import NextSolution
from solver import Solver
from solver2 import Solver2
from constants import *
import random
import timeit

import websockets

# Next 4 lines are not needed for AI agents, please remove them from your code!
# import pygame
# 
# pygame.init()
# program_icon = pygame.image.load("data/icon2.png")
# pygame.display.set_icon(program_icon)
count = 0

count = 0

def find_shape(piece):
    if is_o(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(O)
    elif is_i(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(I)
    elif is_s(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(S)
    elif is_z(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(Z)
    elif is_j(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(J)
    elif is_l(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(L)
    elif is_t(piece):
        #criar uma instância de quadrado, com as coordenadas iniciais da peça
        return Shape(T)
    else:
        # print("---------------------")
        # print("Peça não identificada")
        # print("---------------------")
        global count
        count += 1
        return None

def is_o(piece):

    if ((piece[0][0] == piece[1][0] - 1 and piece[0][0] == piece[2][0]
        and piece[0][0] == piece[3][0] - 1)
        and 
        (piece[0][1] == piece[1][1] and piece[0][1] == piece[2][1] - 1 
        and piece[0][1] == piece[3][1] - 1)):

        # print("sou um O")
        return True

    return False

def is_i(piece):
    
    if (((piece[0][0] == piece[1][0] - 1 and piece[0][0] == piece[2][0] - 2 and piece[0][0] == piece[3][0] - 3)
        and (piece[0][1] == piece[1][1] and piece[0][1] == piece[2][1] and piece[0][1] == piece[3][1]))
        or 
        ((piece[0][1] == piece[1][1] - 1 and piece[0][1] == piece[2][1] - 2 and piece[0][1] == piece[3][1] - 3)
        and (piece[0][0] == piece[1][0] and piece[0][0] == piece[2][0] and piece[0][0] == piece[3][0]))):

        # print("sou um I")
        return True

    return False

def is_s(piece):

    if (((piece[0][0] == piece[1][0] - 1 and piece[0][0] == piece[2][0] + 1 and piece[0][0] == piece[3][0])
        and 
        (piece[0][1] == piece[1][1] and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 1))
        or
        ((piece[0][0] == piece[1][0] and piece[0][0] == piece[2][0] - 1 and piece[0][0] == piece[3][0] - 1) 
        and 
        (piece[0][1] == piece[1][1] - 1 and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 2))):

        # print("sou um S")
        return True

    return False

def is_z(piece):

    if (((piece[0][0] == piece[1][0] - 1 and piece[0][0] == piece[2][0] - 1 and piece[0][0] == piece[3][0] - 2) 
        and 
        (piece[0][1] == piece[1][1] and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 1))
        or
        (piece[0][0] == piece[1][0] + 1 and piece[0][0] == piece[2][0] and piece[0][0] == piece[3][0] + 1) 
        and 
        (piece[0][1] == piece[1][1] - 1 and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 2)):

        # print("sou um Z")
        return True

    return False

def is_j(piece):

    if ((piece[0][0] == piece[1][0] - 1 and piece[0][0] == piece[2][0] and piece[0][0] == piece[3][0])
        and 
        (piece[0][1] == piece[1][1] and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 2)):

        # print("sou um J")
        return True

    return False

def is_l(piece):
    if ((piece[0][0] == piece[1][0] and piece[0][0] == piece[2][0] and piece[0][0] == piece[3][0] - 1)
        and 
        (piece[0][1] == piece[1][1] - 1 and piece[0][1] == piece[2][1] - 2 and piece[0][1] == piece[3][1] - 2)):

        # print("Sou um L")
        return True

    return False

def is_t(piece):

    if ((piece[0][0] == piece[1][0] and piece[0][0] == piece[2][0] - 1 and piece[0][0] == piece[3][0])
        and 
        (piece[0][1] == piece[1][1] - 1 and piece[0][1] == piece[2][1] - 1 and piece[0][1] == piece[3][1] - 2)):

        # print("sou um T")
        return True

    return False
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # receber as dimensões
        state = json.loads(
            await websocket.recv()
        )

        limits = state["grid"]

        if 'dimensions' in state.keys():
            set_width(state['dimensions'][0])
            set_height(state['dimensions'][1])
            # print("ok")

        keys=[]
        # next_keys = []
        # got_next = False
        piece = 0
        grid = Grid(limits)
        # solver = Solver(grid)
        solver2 = Solver2(grid)
        score = 0
        next_piece = None
        next_solution = None
        piece_counter = 0
        prev_position = []
        while True:
            try:
                
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                if state['score'] is not None:
                    score = state['score']

                if 'piece' in state.keys() and state['piece'] is None:
                    piece = None
                    await asyncio.sleep(0)
                    # keys = []
                    # keys.extend(next_keys)
                    # got_next = False
                    # print("Cheguei ao fim, vou trocar de peça")
                    continue

                if len(keys) > 0:
                    key = keys.pop(0)
                
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )

                    await next_solution.choose_next_move(next_rotation)
                    next_rotation += 1
                    continue
                else:
                    # print("State:")
                    # print(state)
                    # print("-----------")
                    if 'dimensions' in state.keys():
                        dimensions = state['dimensions']
                        continue
                    else:
                        if state['piece'] is None:
                            piece = None
                            await sleep(0)
                            if len(keys)>0:
                                keys.pop()
                            continue
                        elif piece == 0 or piece == None:
                            # coordenadas ocupadas
                            grid.set_occupied(state['game'])
                            piece_counter += 1

                            # já calculamos esta peça no ciclo anterior?
                            if next_solution != None and len(next_solution.best_keys) != 0:
                                form = next_solution.piece

                                if next_rotation < next_solution.max_rotation:
                                    print("Rotações feitas: ", next_rotation)
                                    print("Rotações da peça: ", next_solution.max_rotation)
                                    for i in range(next_rotation, next_solution.max_rotation):
                                        await next_solution.choose_next_move(i)

                                keys = next_solution.best_keys
                                
                                # previous_piece_position = next_solution.previous_piece_position
                                next_piece = state['next_pieces'][0]
                                next_form = find_shape(next_piece)
                                next_form.rotate(0)
                                next_rotation = 0
                                keys, position =  await solver2.choose_from_moves(next_solution.piece, next_solution.possible_moves)
                                next_solution = NextSolution(grid, prev_position, position, next_form, piece_counter + 1)
                            
                            # fazer a descoberta de qual peça é
                            else:
                                piece = state['piece']
                                form = find_shape(piece)
                                next_piece = state['next_pieces'][0]
                                next_form = find_shape(next_piece)
                            
                                if form :
                                    form.rotate(0)
                                    next_form.rotate(0)
                                    next_rotation = 0
                                    #next_form=next_shape.peca()
                                    #next_form.rotate(0)
                                    # solver = Solver(grid)
                                    #keys =  await solver.choose_next_move2(shape, form, next_shape, next_form, state['game'])
                                    keys, position =  await solver2.choose_next_move(form)
                                    next_solution = NextSolution(grid, prev_position, position, next_form, piece_counter + 1)

                            prev_position = position

                            # Após a finalização da classe solver os parâmetros rotation e moves serão retornados por essa classe
                
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                global count
                print("Peças não identificadas: ", count)
                print("Score: ", score)
                f = open("results.txt", "a")
                f.write(str(score) + "\n")
                f.close()
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
