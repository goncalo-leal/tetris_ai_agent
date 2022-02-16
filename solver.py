from grid import Grid
from constants import *
from copy import deepcopy
class Solver:
    def __init__(self, grid):
        self.grid = grid

    # def get_completed_lines_score(self, completed_lines, current_height, max_height):
    #     min_weight = 0.55
    #     max_weight = 0.78075

    #     weight = min_weight + ((current_height / max_weight) * (max_height - min_weight))

    #     return completed_lines * weight

    def get_move_score(self, new_position):
        pos = []
        pos.extend(new_position)

        # for x, y in new_position:
        #     pos.append([x, y])
        
        # esta função vai avaliar a pontuação do movimento segundo as nossas heurísticas
        # pos são as coordenadas que a peça atual "quer" ocupar

        # source: https://loonride.github.io/tetris-ai/public/
        
        # completed_lines = self.grid.get_completed_lines(pos) # descomentar a função
        # holes = self.grid.get_hole_count(pos)
        # bumpiness = self.grid.get_bumpiness(pos)
        # rows_with_holes = self.grid.get_rows_with_holes(pos)
        # current_height = self.grid.get_current_height(pos)
        # max_height = get_height()
 
        # holes_weight  = 0.82075
        # bumpiness_weight = 0.3925
        # rows_with_holes_weight = 0.871

        # score = (self.get_completed_lines_score(completed_lines, current_height, max_height) - 
        #     (holes * holes_weight) - (bumpiness * bumpiness_weight) - (rows_with_holes * rows_with_holes_weight))

        # return rows_with_holes, score

        # source: https://github.com/saagar/ai-tetris/blob/master/paper/tetrais.pdf

        # current_height = self.grid.get_current_height(pos)
        # aggregate_height, counter = self.grid.aggregate_height(pos)
        # holes = self.grid.get_hole_count(pos)
        # bumpiness = self.grid.get_bumpiness(pos)
        # valleys = self.grid.get_n_valleys(pos)
        # completed_lines = self.grid.get_completed_lines(pos)

        # score = 20 * completed_lines + (-1.0/1000 * (72 * current_height + 75 * (aggregate_height / counter) + 
        # 442 * holes + 56 * bumpiness + 352 * valleys))

        # return score

        # return (-1.0/1000 * (72 * current_height + 75 * (aggregate_height / counter) + 
        # 442 * holes + 56 * bumpiness + 352 * valleys))

        # source: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/

        # 
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
        holes * holes_weight + completed_lines * completed_lines_weight + bumpiness * bumpiness_weight + valleys * valleys_weight)

        return score

    async def choose_next_move(self, shape, piece):
        best_x = 0
        best_rotation = 0
        best_score = None

        original = deepcopy(piece)
        for rotation in range(shape.rotation):
            translation = 0
            height = 0
            pos = []
            new_position = []        
            
            # print("----------", rotation, "------------")
            # print(original.positions)
            # queremos começar com a peça totalmente à esquerda na rotação atual
            new_position = shape.get_position(rotation, translation, height)
            while (new_position and not self.grid.collide(new_position)): # se não colidir com nenhuma peça, podemos mexer
                pos = [[x, y] for x, y in new_position]

                translation -= 1
                new_position = shape.get_position(rotation, translation, height)
            
            # temos de voltar atrás porque se saiu do while é porque bateu em alguma peça
            translation += 1
            # já temos a peça à esquerda, vamos ver a melhor posição

            new_position = [[x, y] for x, y in pos]      
            while(new_position and not self.grid.collide(new_position)):
              
                # vamos tentar andar o máximo para baixo
                new_position = shape.get_position(rotation, translation, height)
                while (new_position and not self.grid.collide(new_position)): # se não colidir com nenhuma peça, podemos mexer
                    pos = [[x, y] for x, y in new_position]

                    height += 1
                    new_position = shape.get_position(rotation, translation, height)

                # temos de voltar à posição sem colisão
                height -= 1

                new_position = [[x, y] for x, y in pos]

                # ver se é preciso pôr na grid ou não
                score = self.get_move_score(new_position)
                
                if not best_score or score > best_score:
                    best_x = translation
                    best_rotation = rotation
                    best_score = score
                    best_position = new_position

                height = 0
                translation += 1
                
                # new_position = []
                new_position = shape.get_position(rotation, translation, height)
            original.rotate(1)
            original.set_pos(
                (10 - original.dimensions.x) / 2, 0
            )
            shape.setPos(original.positions)
        # esta função deve retornar um array com as teclas a carregar para chegar à melhor posição
        keys=[]
        for x in range(best_rotation):
            keys.append("w")
        
        for x in range(abs(best_x)):
            if (best_x > 0 ):
                keys.append("d")    
            else:
                keys.append("a")   
        keys.append("s") 
        # print(keys)
        return keys, best_position

    def choose_next_move2(self, shape, piece,next_shape,next_piece,new_grid):
        # Vamos fazer aqui, a jogada da primeira peça + o lookahead de 1 
        print("NEW_GRID NO INICIO, ", new_grid)
        best_x = 0
        best_rotation = 0
        g1 = (deepcopy(new_grid))
        # jogar a segunda a peça 
        original_v2= deepcopy(next_piece)
        max_rotation_v2 = next_shape.rotation
        
        scoreTotal=None
        # best_score irá ser usado para as heuristicas
        original= deepcopy(piece)
        max_rotation = shape.rotation
        for rotation in range(max_rotation):
            translation = 0
            height = 0
            pos = []
            new_position = []        
            
            # queremos começar com a peça totalmente à esquerda na rotação atual
            new_position = shape.get_position(rotation, translation, height)
            while (new_position and not self.grid.collide(new_position)): # se não colidir com nenhuma peça, podemos mexer
                pos = []
                
                pos.extend(new_position)

                translation -= 1
                new_position = shape.get_position(rotation, translation, height)
            
            # temos de voltar atrás porque se saiu do while é porque bateu em alguma peça
            translation += 1
            # já temos a peça à esquerda, vamos ver a melhor posição

            new_position = []
            
            new_position.extend(pos)
        
            while(new_position and not self.grid.collide(new_position)):
              
                # vamos tentar andar o máximo para baixo
                new_position = []
                new_position = shape.get_position(rotation, translation, height)
                while (new_position and not self.grid.collide(new_position)): # se não colidir com nenhuma peça, podemos mexer
                    pos = []
                    
                    pos.extend(new_position)

                    height += 1
                    new_position = shape.get_position(rotation, translation, height)

                # temos de voltar à posição sem colisão
                height -= 1

                new_position = []
             
                new_position.extend(pos)

                # ver se é preciso pôr na grid ou não

                score= self.get_move_score(new_position)
                self.grid.add_occupied(new_position)
                #colocar o for 
                ##### AQUIIIIIIIIIIII
                
                for rotation_2 in range(max_rotation_v2):
                   
                    translation_2 = 0
                    height_2 = 0
                    pos_2 = []
                    new_position_2 = []        
                    
                   
                    # queremos começar com a peça totalmente à esquerda na rotação atual
                    new_position_2 = next_shape.get_position(rotation_2, translation_2, height_2)
                    while (new_position_2 and not self.grid.collide(new_position_2)): # se não colidir com nenhuma peça, podemos mexer
                        pos_2 = []
                        
                        pos_2.extend(new_position_2)

                        translation_2 -= 1
                        new_position_2 = next_shape.get_position(rotation_2, translation_2, height_2)
                    
                    # temos de voltar atrás porque se saiu do while é porque bateu em alguma peça
                    translation_2 += 1
                    # já temos a peça à esquerda, vamos ver a melhor posição

                    new_position_2 = []
                    
                    new_position_2.extend(pos_2)
                    while(new_position_2 and not self.grid.collide(new_position_2)):
                        # vamos tentar andar o máximo para baixo
                        new_position_2 = []
                        new_position_2 = next_shape.get_position(rotation_2, translation_2, height_2)
                        while (new_position_2 and not self.grid.collide(new_position_2)): # se não colidir com nenhuma peça, podemos mexer
                            pos_2 = []
                            pos_2.extend(new_position_2)


                            height_2 += 1
                            new_position_2 = next_shape.get_position(rotation_2, translation_2, height_2)

                        # temos de voltar à posição sem colisão
                        height_2 -= 1

                        new_position_2 = []
                        new_position_2.extend(pos_2)

                        score_2 = self.get_move_score(new_position_2)
                   
                        
                        if not scoreTotal or scoreTotal <   score :
                            best_x = translation
                            best_rotation = rotation
                            scoreTotal =    score
                            

                        height_2 = 0
                        translation_2 += 1
                        
                        new_position_2 = []
                        new_position_2 = next_shape.get_position(rotation_2, translation_2, height_2)
                    original_v2.rotate(1)
                    original_v2.set_pos(
                        (10 - original_v2.dimensions.x) / 2, 0
                    )
                    next_shape.setPos(original_v2.positions)
                        # esta função deve retornar o número de movimentos horizontais e número de rotações
                #aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                
                # if not scoreTotal or scoreTotal <   score :
                #             best_x = translation
                #             best_rotation = rotation
                #             scoreTotal =    score
                #Limpar a grid para o estado em que começou algo que não esta a acontecer
                self.grid.set_occupied(deepcopy(g1))
                
                height = 0
                translation += 1
                
                new_position = []
                new_position = shape.get_position(rotation, translation, height)
            original.rotate(1)
            original.set_pos(
                (10 - original.dimensions.x) / 2, 0
            )
            shape.setPos(original.positions)
                # esta função deve retornar o número de movimentos horizontais e número de rotações
        #aqui devia de colocar na grid a primeira peça 
        
     
        
        keys=[]
       
        for x in range(best_rotation):
            keys.append("w")
        
        for x in range(abs(best_x)):
            if (best_x > 0 ):
                keys.append("d")    
            else:
                keys.append("a")   
        keys.append("s") 
        print(keys)
        return keys

