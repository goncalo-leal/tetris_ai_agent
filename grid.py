from constants import *
from copy import deepcopy
from re import findall

# a grid tem 10 colunas (0 a 9), mas a coluna 0 e a 9 são as paredes do jogo
# se queremos correr a grid em largura só podemos ir de 1 a 8

class Grid:
    def __init__(self, limits, grid=None) -> None:
        if grid != None:
            self.grid = grid
        else:
            self.grid = []
        
        self.limits = limits

    def get_grid(self):
        return self.grid

    def clear(self):
        self.grid=[]

    def set_occupied(self, occupied):
        self.grid = [(x, y) for x, y in occupied]

    def add_occupied(self, occupied):
        # for x, y in occupied:
        #     self.grid.append((x, y))
        
        self.grid.extend([(x, y) for x, y in occupied if (x, y) not in self.grid])

    def get_grid_copy(self):
        return deepcopy(self.grid)

    def add_to_grid_copy(self, pos):
        tmp_grid = self.get_grid_copy()
        tmp_grid.extend(pos)
        return tmp_grid

    def collide(self, piece):
        return any({(x, y) in self.grid for x, y in piece}) or any (
            {[x, y] in self.limits for x, y in piece}
        )

    def check_line(self, y, tmp_grid):
        # verifica se já existe algum 1 na linha 
        # for x in range(1, get_width() - 1):
        #     if [x, y] in tmp_grid:
        #         return True
        # return False

        return any({(x, y) in tmp_grid for x in range(1, get_width() -1)})

    def line_is_full(self, y, tmp_grid):
        # verifica se a linha está completa

        # for x in range(1, get_width() - 1):
        #     if [x, y] not in tmp_grid:
        #         return False
        # return True

        return all({(x, y) in tmp_grid for x in range(1, get_width() -1)})
    
    def get_col_height(self, x, tmp_grid):
        # retorna a altura de uma coluna específica

        # como y cresce de cima para baixo a altura deverá ser 30 - o índice do primeiro 1
        # for y in range(get_height()):
        #     if [x, y] in tmp_grid:
        #         return get_height() - y
        # return 0

        ret = get_height() - min({y for y in range(get_height()) if (x, y) in tmp_grid}.union(set([get_height()])))
        return ret

    def get_hole_count(self, pos):
        # buracos que a jogada para pos vai formar
        # para esta contagem só podemos considerar linhas com, pelo menos, um 1 (isto pode ser uma função à parte que só vê se a linha está ocupada)

        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        n_holes = 0
        for x in range(1, get_width() - 1):
            height = self.get_col_height(x, tmp_grid)
            s = ''.join([str(1) if (x, y) in tmp_grid else str(0) for y in range(get_height())])

            n_holes += len(findall('0', s[(get_height() - height):]))

            # block_hit = False
            # for y in range(get_height()):
            #     if (x, y) in tmp_grid:
            #         block_hit = True

            #     if (x, y) not in tmp_grid and block_hit: # algures acima deste espaço livre há um bloco
            #         n_holes += 1
        
        return n_holes

    def get_bumpiness(self, pos):
        # diferença de alturas entre colunas (após a jogada pos)
        # temos de contar onde aparece o primeiro um e a altura será = 30 - <indice do primeiro 1>
        # bumpiness = soma do módulo da diferença entre colunas adjacentes
        
        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        # com list comprehensions iamos ter 2 for's então deixamos assim
        # um para ir buscar as alturas e outro para fazer as diferenças
        # PERGUNTAR AO TEIXEIRA
        
        bumpiness = 0        
        prev_height = self.get_col_height(1, tmp_grid) # não existem alturas negativas, qualquer valor negativo serve
        height = 0
        for x in range(2, get_width() - 1):
            height = self.get_col_height(x, tmp_grid)
            bumpiness += abs(height - prev_height)

            prev_height = height

        return bumpiness

    def get_completed_lines(self, pos):
        # n.º de linhas que ficarão completas com pos

        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        n_completed = sum([1 if self.line_is_full(y, tmp_grid) else 0 for y in range(get_height())])
        # for y in range(get_height()): # para correr linha a linha tem de manter a ordenada e avançar na abcissa
        #     if self.line_is_full(y, tmp_grid):
        #         n_completed += 1

        return n_completed

    def get_rows_with_holes(self, pos):
        # n.º de linhas que terão buracos após pos

        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        # Não estamos a usar, não tentamos melhorar

        rows_with_holes = 0
        for x in range(1, get_width() - 1):
            block_hit = False
            row_has_hole = False

            for y in range(get_height()):
                if self.line_is_full(y, tmp_grid):
                    continue

                if (x, y) in tmp_grid:
                    block_hit = True

                if block_hit and (x, y) not in tmp_grid: # a linha tem blocos e este está vazio, logo conta como buraco
                    row_has_hole = True
                    break
            if row_has_hole:
                rows_with_holes += 1

        return rows_with_holes

    def get_current_height(self, pos):
        # coluna mais alta após pos

        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        max_height = max([self.get_col_height(x,tmp_grid) for x in range(1, get_width() - 1)])

        # for x in range(1, get_width() -1):
        #     tmp_height = self.get_col_height(x,tmp_grid)

        #     if max_height < tmp_height:
        #         max_height = tmp_height

        return max_height

    def aggregate_height(self, pos):
        # soma das alturas de cada coluna
        
        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        height = sum([self.get_col_height(x,tmp_grid) for x in range(1, get_width() - 1)])

        # for x in range(1, get_width() - 1):
        #     height += self.get_col_height(x,tmp_grid)

        return height

    def get_n_valleys(self, pos):
        # função que retorna o número de vales (sítios onde apenas um I cabe)

        # Código 1.0
        # tmp_grid = []
        # for i in range(len(self.grid)):
        #     tmp_grid.append(self.grid[i])

        # for i in range(len(pos)):
        #     tmp_grid.append(pos[i])

        # Código 2.0
        # tmp_grid = deepcopy(self.grid) # self.grid.copy()
        # tmp_grid.extend(pos)

        # Código 3.0
        # tmp_grid = self.add_to_grid_copy(pos)

        # Código 4.0
        # tmp_grid = [[x, y] for x, y in self.grid]
        # tmp_grid = []
        # tmp_grid.extend(self.grid)
        # tmp_grid.extend(pos)

        # Código 5.0
        tmp_grid = set(self.grid).union(set(pos))

        # Não estamos a usar

        valleys = 0
        for x in range(1, get_width() - 1):
            # temos 2 casos especiais, x = 1 que fica no limite esquerdo e x = GAME_WIDTH (se for 10) - 2 
            if x == 1:
                if self.get_col_height(x, tmp_grid) + 3 <= self.get_col_height(x + 1, tmp_grid):
                    valleys += 1

            elif x == get_width() - 2: # x = 8, ou seja, o limite direito
                if self.get_col_height(x, tmp_grid) + 3 <= self.get_col_height(x - 1, tmp_grid):
                    valleys += 1

            else:
                if (self.get_col_height(x, tmp_grid) + 3 <= self.get_col_height(x - 1, tmp_grid)
                    and
                    self.get_col_height(x, tmp_grid) + 3 <= self.get_col_height(x + 1, tmp_grid)):
                    valleys += 1

        return valleys