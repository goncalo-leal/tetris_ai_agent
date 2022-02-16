from constants import *
from copy import copy
from grid import Grid
from my_shapes import MyShape

class NextSolution:
    def __init__(self, grid, previous_piece_position, actual_piece_position, piece, piece_counter) -> None:
        self.grid = Grid(copy(grid.limits), copy(grid.grid))
        self.previous_piece_position = previous_piece_position
        # basicamente, vamos andar a ver a next_piece da peça que está a ser jogada agora, 
        # é como se andassemos sempre 2 peças à frente
        # ou seja, a grid da peça atual ainda não tem a peça anterior
        self.grid.add_occupied(previous_piece_position)
        self.grid.add_occupied(actual_piece_position)
        self.piece = piece # piece é uma instância da classe shape
        self.max_rotation = len(self.piece.plan)
        self.best_score = None
        self.best_keys = []
        self.best_position = []
        self.piece_counter = piece_counter
        self.possible_moves = []

    def valid(self, piece):
        return not any([(x, y) in self.grid.grid for x, y in piece]) and not any (
            [[x, y] in self.grid.limits for x, y in piece]
        )

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

        holes_weight = -0.35663 # original: -0.35663
        aggregate_height_weight = -0.510066 # original: -0.510066
        completed_lines_weight = 0.660666 # original: -0.760666
        bumpiness_weight = -0.184483 # original: -0.184483
        current_height_weight = 0 # -0.25
        # valleys_weight = -0 # 0

        bumpiness = self.grid.get_bumpiness(pos)
        holes = self.grid.get_hole_count(pos)
        completed_lines = self.grid.get_completed_lines(pos)
        aggregate_height = self.grid.aggregate_height(pos)
        current_height = self.grid.get_current_height(pos) # não era usado originalmente
        # valleys = self.grid.get_n_valleys(pos)

        # forçar a fazer linhas
        if current_height > 20: # 20
            completed_lines_weight = 4 # 4
            aggregate_height_weight = -0.710066
            bumpiness_weight = -0.284483
            holes_weight = -0.35054
            current_height_weight = -0.25
            # valleys_weight = -0.12 # -0.15

        score = (aggregate_height * aggregate_height_weight + current_height * current_height_weight +
        holes * holes_weight + completed_lines * completed_lines_weight + bumpiness * bumpiness_weight)

        return score, pos

    async def choose_next_move(self, rotation):
        if rotation >= self.max_rotation:
            return

        best_score = None
        # best_score irá ser usado para as heuristicas
        #tenho que colocar o original com as coordenadas da piece
        keys_temp=[]

        original = MyShape(copy(self.piece))
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

            if keys_temp in self.possible_moves: # não queremos ver soluções duplicadas
                continue

            self.possible_moves.append(keys_temp)