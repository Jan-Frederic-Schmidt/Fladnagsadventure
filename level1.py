from gamegrid import *
import random
import time

def level1():
    startTime = int(time.clock())
    class Bar(Actor):
        def __init__(self, score):
            Actor.__init__(self, "sprites/mbrobot.gif")
            self.score = score
    
    class Obstacle(Actor):
        def __init__(self):
            Actor.__init__(self, "sprites/twentycent.png")
        
        def act(self):
            self.setDirection(90)
            self.move()
            if self.getLocation() == bar.getLocation():
                removeAllActors()
                return
            addObstacles()    
    
    def keyCallbackLevelOne(e):
        keyCode = e.getKeyCode()
        if bar.getX()!= 8 and bar.getX() != 12:
            if keyCode == 65:
                bar.setDirection(180)
                bar.move()
            elif keyCode == 68:
                bar.setDirection(0)
                bar.move()
        else:
            bar.turn(180)
            bar.move()        
            
    def addObstacles():
        newTime = int(time.clock())
        if (startTime - newTime) % 4 == 0:
            addActor(Obstacle(), Location(10,0))
        
    makeGameGrid(21, 21, 29, None, False, keyPressed = keyCallbackLevelOne)
    bar = Bar(0)
    addActor(bar, Location(10, 10))
    addActor(Obstacle(), Location(10, 0))
    
    show()
    doRun()
level1()