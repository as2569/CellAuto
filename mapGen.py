import maps
import cell
import math
import random
import time

class MapGen:
    def __init__(self, x_size, y_size, layer):
        self.target_layer = layer
        self.x = x_size
        self.y = y_size
        self.mid_point = (x_size/2, y_size/2)
        self.maximum = self.find_max(x_size, y_size)
        return

    def generateMap(self):
        start_time = time.clock()        
        self.target_layer = self.seed_pass(self.target_layer)
        self.target_layer = self.cluster_pass(self.target_layer, 8)
        self.target_layer = self.coast_pass(self.target_layer, 2)
        self.target_layer = self.hill_seed_pass(self.target_layer)
        self.target_layer = self.hill_pass(self.target_layer, 8)
        
        print("GENERATOR DONE with runtime " + str(time.clock() - start_time))
        return self.target_layer

    def find_max(self, width, height):
        m = math.sqrt(math.pow(0 - width/2, 2) + math.pow(0 - height/2, 2))
        return math.floor(m)

    def find_distance(self, x, y):
        d =  math.sqrt(math.pow(x - self.mid_point[0], 2) + math.pow(y - self.mid_point[1], 2))
        normalized = (d - 0)/(self.maximum - 0)
        return normalized

    def seed_pass(self, layer):
        print('seed pass')
        for x in range(0, layer.mapWidth):
            for y in range(0, layer.mapHeight):
                if x == 0 or x == layer.mapWidth - 1 or y == 0 or y == layer.mapHeight - 1:  # edge cells are always SEA
                    layer.matrix[(x, y)].set_state(cell.CellType.SEA)
                else:
                    rand = random.random() * math.pow(1 - self.find_distance(x, y), 2)
                    if rand <= 0.25:  # chance to spawn SEA cells
                        layer.matrix[(x, y)].set_state(cell.CellType.SEA)
                    else:
                        layer.matrix[(x, y)].set_state(cell.CellType.PLAINS)
        return layer


    def cluster_pass(self, layer, run_times):
        local_layer = layer
        for i in range(0, run_times):
            print('cluster pass')
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.moore(cell.CellType.SEA, x, y, 1) >= 5:
                        layer.matrix[(x, y)].set_state(cell.CellType.SEA)
                    else:
                        layer.matrix[(x, y)].set_state(cell.CellType.PLAINS)
        return local_layer


    def coast_pass(self, layer, run_times):
        local_layer = layer
        for i in range(0, run_times):
            if i == 0:
                print('coast pass')  # initial pass
                for x in range(0, local_layer.mapWidth):
                    for y in range(0, local_layer.mapHeight):
                        if local_layer.matrix[(x, y)].state == cell.CellType.SEA:
                            if local_layer.moore(cell.CellType.PLAINS, x, y, 1) > 0 and local_layer.moore(cell.CellType.SEA, x, y, 1) > 0:
                                layer.matrix[(x, y)].set_state(cell.CellType.COAST)

            print('coast cleanup pass')  # clean up pass
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.matrix[(x, y)].state == cell.CellType.SEA:
                        if local_layer.moore(cell.CellType.COAST, x, y, 1) >= 5 and local_layer.moore(cell.CellType.PLAINS, x, y, 1) == 0:
                            layer.matrix[(x, y)].set_state(cell.CellType.COAST)
        return local_layer

    def hill_seed_pass(self, layer):
        local_layer = layer
        print('hill seed pass')
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == cell.CellType.PLAINS:
                    if local_layer.moore(cell.CellType.COAST, x, y, 2) <= 1:
                        rand = random.random()
                        if(rand > 0.55): # chance to spawn SEA cells --> range 0.5 - 0.55
                            layer.matrix[(x, y)].set_state(cell.CellType.HILL)
        return local_layer

    def hill_pass(self, layer, run_times):
        local_layer = layer
        for i in range(0, run_times):
            print('hill cluster pass')
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.matrix[(x, y)].state == cell.CellType.PLAINS:
                        if local_layer.moore(cell.CellType.HILL, x, y, 1) >= 5:
                            layer.matrix[(x, y)].set_state(cell.CellType.HILL)
                    if local_layer.matrix[(x, y)].state == cell.CellType.HILL:
                        if local_layer.moore(cell.CellType.HILL, x, y, 1) <= 4:
                            layer.matrix[(x, y)].set_state(cell.CellType.PLAINS)
        return local_layer

    def mountain_seed_pass(self, layer, run_times):
        local_layer = layer
        for i in range(0, run_times):
            print('mountain seed pass')
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.matrix[(x, y)].state == cell.CellType.HILL:
                        if local_layer.moore(cell.CellType.PLAINS, x, y, 1) <= 1:
                            rand = random.random()
                            if(rand > 0.50): # range between 0.50 and 0.55
                                layer.matrix[(x, y)].set_state(cell.CellType.MOUNTAIN)
        return local_layer

    def mountain_pass(self, layer, run_times):
        local_layer = layer
        for i in range(0, run_times):
            print('mountain pass')
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.matrix[(x, y)].state == cell.CellType.HILL:
                        if local_layer.moore(cell.CellType.HILL, x, y, 3) + local_layer.moore(cell.CellType.MOUNTAIN, x, y, 3) >= 45:
                            layer.matrix[(x, y)].set_state(cell.CellType.MOUNTAIN)
        return local_layer
