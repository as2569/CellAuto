import cell

class Maps:
    def __init__(self, x, y, size):
        self.mapWidth = x
        self.mapHeight = y
        self.cellSize = size
        self.matrix = {(0, 0): cell.Cell(x, y, size)}
        return

    def make_empty(self):
        for x in range(0, self.mapWidth):
            for y in range(0, self.mapHeight):
                self.matrix[(x, y)] = cell.Cell(x, y, self.cellSize)
        self.set_neighbors()
        return

    def get_state(self, x, y):
        if x > self.mapWidth - 1 or x < 0 or y > self.mapHeight - 1 or y < 0:
            return cell.CellType.SEA
        else:
            return self.matrix[(x, y)].state

    def set_neighbors(self):
        for x in range(0, self.mapWidth):
            for y in range(0, self.mapHeight):
                self.set_neighbor(x,y)

    def set_neighbor(self, x, y):
        vals = [(x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y), (x,y), (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
        for val in vals:
            if (val[0] > self.mapWidth - 1 or val[0] < 0 or val[1] > self.mapHeight - 1 or val[1] < 0) == False:
                self.matrix[(x, y)].neighbors.append(self.matrix[(val[0], val[1])])

    def neumann(self, target_type, x, y, r):
        count = 0
        if self.get_state(x - 1, y) == target_type:
            count += 1
        if self.get_state(x, y - 1) == target_type:
            count += 1
        if self.get_state(x + 1, y) == target_type:
            count += 1
        if self.get_state(x, y + 1) == target_type:
            count += 1
        return count

    def getNeumannNeighbors(self, x, y):
        n = []
        if self.get_state(x - 1, y) != cell.CellType.SEA:
            n.append((x - 1, y))
        if self.get_state(x, y - 1) != cell.CellType.SEA:
            n.append((x, y - 1))
        if self.get_state(x + 1, y) != cell.CellType.SEA:
            n.append((x + 1, y))
        if self.get_state(x, y + 1) != cell.CellType.SEA:
            n.append((x, y + 1))
        return n

    def moore(self, in_type, x, y):
        count = 0
        if self.get_state(x, y) == in_type: # self
            count += 1
        if self.get_state(x - 1, y) == in_type: # left center
            count += 1
        if self.get_state(x - 1, y - 1) == in_type: # left bottom
            count += 1
        if self.get_state(x, y - 1) == in_type: # middle bottom
            count += 1
        if self.get_state(x + 1, y - 1) == in_type: # right bottom
            count += 1
        if self.get_state(x + 1, y) == in_type: # right center
            count += 1
        if self.get_state(x + 1, y + 1) == in_type: # right top
            count += 1
        if self.get_state(x, y + 1) == in_type: # middle top
            count += 1
        if self.get_state(x - 1, y + 1) == in_type: # left top
            count += 1
        return count

    def moore(self, in_type, xPos, yPos, r): #counts self
        count = 0
        for x in range(xPos - r, xPos + r + 1):
            for y in range(yPos - r, yPos + r + 1):
                if self.get_state(x, y) == in_type:
                    if abs(xPos - x) <= r and abs(yPos - y) <= r:
                        count += 1
        return count

    def mooreFast(self, in_type, x, y):
        count = 0
        for n in self.matrix[(x,y)].neighbors:
            if n.get_state == in_type:
                count = count + 1
        return count

    def update_map(self):
        for key, value in self.matrix.items():
            self.matrix[key].update()

    def draw_map(self, screen):
        for key, cell in self.matrix.items():
            screen.blit(cell.image, cell.rect)
        return

#    def remove_sea(self):
#        keysToDelete = []
#        for key, value in self.matrix.items():
#            if self.matrix[key].state == cell.CellType.SEA:
#                keysToDelete.append(key)

#        for i in keysToDelete:
#            self.matrix.items().pop(key, None)

        return self.matrix

    def position_valid(self, x, y):
        if x > self.mapWidth or x < 0 or y > self.mapHeight or y < 0:
            return False
        else:
            return True
