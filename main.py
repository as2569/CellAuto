import pygame
import sys
import random
import time
import json
import math
import cell
import maps
import mapGen
import civilization


class GameStage(enumerate):
    INITIAL = 0
    SEED = 1
    CLUSTER = 2
    COASTPASS = 3
    HILLPASS = 4
    MOUNTAINPASS = 5
    SEEDCIV = 6
    EXPAND = 7
    DONE = 8


class Manager:
    def __init__(self):
        self.currentStage = GameStage.INITIAL

x_max = 200
y_max = 200

pygame.init()
manager = Manager()

land_layer = maps.Maps(x_max, y_max, 5)
civ_layer = maps.Maps(x_max, y_max, 5)

windowSize = [800, 800]

land_layer.make_empty()
civ_layer.make_empty()

# Plains, Coast, Hills, Neumann, Moore
civ1Mods = [2, 1, 3, 30, 30]
civ2Mods = [1, 1, 1, 1, 1]

civ_1 = civilization.Civilization(cell.CellType.CIV1, civ2Mods)

screen = pygame.display.set_mode(windowSize)
start_time = time.clock()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0, 0))  # draw blank screen

    if manager.currentStage == GameStage.INITIAL:
        mapGenerator = mapGen.MapGen(x_max, y_max, land_layer)
        land_layer = mapGenerator.generateMap()
        manager.currentStage = GameStage.SEEDCIV
    elif manager.currentStage == GameStage.SEEDCIV:
        civ_layer = civ_1.seed_civ(land_layer, civ_layer)
        manager.currentStage = GameStage.EXPAND
        #land_layer = land_layer.remove_sea()
    elif manager.currentStage == GameStage.EXPAND:
        civ_layer = civ_1.expand(land_layer, civ_layer)
        if(civ_1.checkIfDone()):
            sys.exit()

##    pressed = pygame.key.get_pressed()

#   land_layer.update_map()
#    civ_layer.update_map()

#    land_layer.draw_map(screen)    
#    civ_layer.draw_map(screen)

    pygame.display.flip()  # next frame

























