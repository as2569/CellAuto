import cell
import random
import time

class Civilization:
    def __init__(self, civType, modifiers):
        self.population = 0
        self.borders = {}
        self.potentialSeeds = []
        self.type = civType
        self.plainsMod = modifiers[0]
        self.coastMod = modifiers[1]
        self.hillsMod = modifiers[2]
        self.neumannMod = modifiers[3]
        self.mooreMod = modifiers[4]
        self.start_time = time.clock()
        self.step = 0

    def update_borders(self, landLayer, civLayer, pos):
        local_layer = landLayer
        local_civ = civLayer
        newBorders = local_layer.getNeumannNeighbors(pos[0], pos[1])
        for item in newBorders:
            if (local_layer.matrix[item].state == cell.CellType.PLAINS or local_layer.matrix[item].state == cell.CellType.HILL) and local_civ.matrix[item].state != cell.CellType.CIV1:
                self.borders[item] = 0

        self.evaluate_borders(local_layer)
        self.borders.pop(pos)

        if len(self.borders) == 0:
            print("EXPANSION DONE with time " + str(time.clock() - self.start_time) + ' and ' + str(self.step) + ' steps ')

    def checkIfDone(self):
        if len(self.borders) == 0:
            return True
        return False

    def evaluate_borders(self, layer):
        local_layer = layer
        for key in self.borders:
            #print('eval')
            numCoast = local_layer.mooreFast(cell.CellType.COAST, key[0], key[1])
            numPlains = local_layer.mooreFast(cell.CellType.PLAINS, key[0], key[1])
            numHills = local_layer.mooreFast(cell.CellType.HILL, key[0], key[1])
            mooreNeighbors = local_layer.mooreFast(self.type, key[0], key[1])
            #numCoast = local_layer.moore(cell.CellType.COAST, key[0], key[1], 1)
            #numPlains = local_layer.moore(cell.CellType.PLAINS, key[0], key[1], 1)
            #numHills = local_layer.moore(cell.CellType.HILL, key[0], key[1], 1)
            #mooreNeighbors = local_layer.moore(self.type, key[0], key[1], 1)
            neumannNeighbors = local_layer.neumann(self.type, key[0], key[1], 1)
            totalValue = numCoast * self.coastMod\
                         + numPlains * self.plainsMod\
                         + numHills * self.hillsMod \
                         + mooreNeighbors * self.mooreMod \
                         + neumannNeighbors * self.neumannMod
            self.borders[key] = totalValue
        return

    def find_best(self):
        if len(self.borders.values()) > 0:
            max_value = max(self.borders.values())
            max_keys = [k for k, v in self.borders.items() if v == max_value]
            rand = random.randrange(0, len(max_keys))
            return max_keys[rand]
        else:
            return 0

    def expand(self, landLayer, civLayer):
        local_civ = civLayer
        local_land = landLayer

        best_location = self.find_best()
        if best_location == 0:
            return local_civ
        else:
            local_civ.matrix[best_location].set_state(self.type)
            self.update_borders(local_land, local_civ, best_location)
            self.step = self.step + 1
            return local_civ

    def find_initial(self, landLayer, civLayer):
        local_layer = landLayer
        local_civ = civLayer
        self.borders.clear()
        
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == cell.CellType.PLAINS or local_layer.matrix[(x, y)].state == cell.CellType.HILL:
                    self.borders[(x, y)] = 0
                    
        self.evaluate_borders(local_layer)
        best_location = self.find_best()
        local_civ.matrix[best_location].set_state(self.type)
        
        manager.currentStage = GameStage.EXPAND
        return local_civ

    def seed_civ(self, landLayer, civLayer):
        local_layer = landLayer
        local_civ = civLayer
        self.borders.clear()
        self.potentialSeeds.clear()
        
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == cell.CellType.PLAINS:
                    self.potentialSeeds.append((x, y))

        initPos = self.potentialSeeds[random.randrange(0, len(self.potentialSeeds))]
        local_civ.matrix[initPos].set_state(self.type)
        self.borders[initPos] = 0
        
        self.update_borders(local_layer, local_civ, initPos)
        self.evaluate_borders(local_layer)
        
        return local_civ
