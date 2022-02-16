from grid import Grid
from constants import *
from copy import copy, deepcopy

from my_shapes import MyShape
class Solver2:
    def __init__(self, grid):
        self.grid = grid

    def valid(self, piece):
        return not any([(x, y) in self.grid.grid for x, y in piece]) and not any (
            [[x, y] in self.grid.limits for x, y in piece]
        )

    def get_completed_lines_score(self, completed_lines, current_height, max_height):
        min_weight = 0.55
        max_weight = 0.78075

        weight = min_weight + ((current_height / max_weight) * (max_height - min_weight))

        return completed_lines * weight

    def get_move_score(self, new_position):
        pos = [(x, y) for x, y in new_position]
        # for x, y in new_position:
        #     pos.append((x, y))

        # esta função vai avaliar a pontuação do movimento segundo as nossas heurísticas
        # pos são as coordenadas que a peça atual "quer" ocupar
        
        # completed_lines = self.grid.get_completed_lines(pos) # número de linhas que ficam completas com a peça nesta posição
        # holes = self.grid.get_hole_count(pos)
        # bumpiness = self.grid.get_bumpiness(pos)
        # rows_with_holes = self.grid.get_rows_with_holes(pos)
        # current_height = self.grid.get_current_height(pos)
        # max_height = GAME_HEIGHT
 
        # holes_weight  = 0.82075
        # bumpiness_weight = 0.3925
        # rows_with_holes_weight = 0.871

        # score = (self.get_completed_lines_score(completed_lines, current_height, max_height) - 
        #     (holes * holes_weight) - (bumpiness * bumpiness_weight) - (rows_with_holes * rows_with_holes_weight))

        # return rows_with_holes, score

        holes_weight = -0.32663 # original: -0.35663
        aggregate_height_weight = -0.550066 # original: -0.510066
        completed_lines_weight = 0.660666 # original: -0.760666
        bumpiness_weight = -0.204483 # original: -0.184483
        current_height_weight = 0 # -0.25
        #valleys_weight = 0 #-0.203421 # original: 0

        bumpiness = self.grid.get_bumpiness(pos)
        holes = self.grid.get_hole_count(pos)
        completed_lines = self.grid.get_completed_lines(pos)
        aggregate_height = self.grid.aggregate_height(pos)
        current_height = self.grid.get_current_height(pos) # não era usado originalmente
        #valleys = self.grid.get_n_valleys(pos) # não era usado originalmente

       
        # forçar a fazer linhas
        if current_height > 20: # 20
            completed_lines_weight = 4 # 4
            aggregate_height_weight = -0.710066
            bumpiness_weight = -0.284483
            holes_weight = -0.35663

        score = (aggregate_height * aggregate_height_weight + current_height * current_height_weight +
        holes * holes_weight + completed_lines * completed_lines_weight + bumpiness * bumpiness_weight)

        return score, pos

    async def choose_next_move(self, form):
        best_score = None
        # best_score irá ser usado para as heuristicas
        #NOTA O PIECE DE ANTES AGORA É FORM
        max_rotation = len(form.plan)
        #tenho que colocar o original com as coordenadas da piece
        keys_temp=[]
        solutions = []
        for rotation in range(max_rotation):
            original = MyShape(copy(form))
            original.shape.rotate(rotation)
            original.shape.set_pos(
                (10 - original.shape.dimensions.x) / 2, 0
            )

            min_x = original.get_min_x()
            max_x = original.get_max_x()

            for coluna in range(1, get_width() - 1):
                keys_temp = []

                keys_temp += ["w"] * (rotation)
                if coluna < min_x:
                    #andar para a esquerda logo colocar 'a'
                    a_s = min_x - coluna
                    keys_temp += ["a"] * a_s

                elif coluna > max_x:
                    #colocar d's 
                    d_s = coluna - max_x
                    keys_temp += ["d"] * d_s

                keys_temp.append("s")

                #ja tenho as keys agora vamos ver se é fiavel 

                if keys_temp in solutions: # não queremos ver soluções duplicadas
                    continue

                tmp = MyShape(copy(form))
                tmp.shape.set_pos(
                    (10 - tmp.shape.dimensions.x) / 2, 0
                )

                i = 0
                while self.valid(tmp.shape.positions):
                    tmp.shape.y += 1
                    key = keys_temp[i]

                    if key == "s":
                        while self.valid(tmp.shape.positions):
                            #print("s")
                            tmp.shape.y += 1
                        tmp.shape.y -= 1
                    elif key == "w":
                        tmp.shape.rotate()
                        # if not self.valid(tmp.positions):
                        #     tmp.rotate(-1)
                    elif key == "a":
                        shift = -1
                    elif key == "d":
                        shift = +1

                    if key in ["a", "d"]:
                        tmp.shape.translate(shift, 0)

                    i += 1
                    if len(keys_temp) == i:
                        break

                if len(keys_temp) == i:
                    solutions.append(keys_temp)
                    score, position = self.get_move_score(tmp.shape.positions)
                    if not best_score or score > best_score:
                        keys_res = keys_temp
                        best_score = score
                        best_position = position

        return keys_res, best_position

    def choose_from_moves(self, form, moves):
        for move in moves:
            tmp = MyShape(copy(form))
            tmp.shape.set_pos(
                (10 - tmp.shape.dimensions.x) / 2, 0
            )

            i = 0
            while self.valid(tmp.shape.positions):
                tmp.shape.y += 1
                key = move[i]

                if key == "s":
                    while self.valid(tmp.shape.positions):
                        #print("s")
                        tmp.shape.y += 1
                    tmp.shape.y -= 1
                elif key == "w":
                    tmp.shape.rotate()
                    # if not self.valid(tmp.positions):
                    #     tmp.rotate(-1)
                elif key == "a":
                    shift = -1
                elif key == "d":
                    shift = +1

                if key in ["a", "d"]:
                    tmp.shape.translate(shift, 0)

                i += 1
                if len(move) == i:
                    break

            if len(move) == i:
                score, position = self.get_move_score(tmp.shape.positions)
                if not best_score or score > best_score:
                    keys_res = moves
                    best_score = score
                    best_position = position

        return keys_res, position