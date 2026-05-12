from gamegrid import *
import random

def level1():
    class Bar(Actor):
        def __init__(self, score):
            Actor.__init__(self, "H:\Informatik\Python/fladnagsAdventure/sprites/fladnagFliegend@2x.png", 2)
            self.score = score
    
    class Obstacle(Actor):
        def __init__(self):
            Actor.__init__(self, "sprites/twentycent.png")
        
        def act(self):
            self.setDirection(90)
            self.move()
            if self.getY() == 4:
                addObstacles()
            if self.getLocation() == bar.getLocation():
                removeAllActors()
                bar.score = 0
                setStatusText("Dein Score: " + str(bar.score))
                addActor(LostScreen(), Location(10, 9))
                addActor(NewGame(), Location(10, 11))
                return
            if self.getY() == bar.getY() + 1: 
                bar.score += 1
                setStatusText("Dein Score: " + str(bar.score)) 
              
    class LostScreen(Actor):
        def __init__(self):
            Actor.__init__(self, True, "sprites/you_lost.gif")
            
    class NewGame(Actor):
        def __init__(self):
            Actor.__init__(self, True, "sprites/btn_renew_0.gif")
    
    def keyCallbackLevelOne(e):
        keyCode = e.getKeyCode()
        if bar.getX()!= 8 and bar.getX() != 12:
            if keyCode == 65:
                bar.setDirection(180)
                bar.showNextSprite()
                bar.move()
            elif keyCode == 68:
                bar.setDirection(0)
                bar.showNextSprite()
                bar.move()
        else:
            bar.turn(180)
            bar.move()  
            
    def clickOnButton(e):
        location = toLocationInGrid(e.getX(), e.getY())
        button = getOneActorAt(location, NewGame)
        if button != None:
            removeAllActors()
            addActor(bar, Location(10, 10))
            addActor(Obstacle(), Location(random.randint(8, 12), 0))  
            
    def addObstacles():
            locations = []
            length = 1

            while len(locations) < length:
                integer = random.randint(8, 12)

                if integer not in locations:
                    locations.append(integer)
            print(len(locations))

            for x in locations:
                addActor(Obstacle(), Location(x, 0))
        
    makeGameGrid(21, 21, 29, None, "H:\Informatik\Python/fladnagsAdventure/sprites/level1Background.png", False, keyPressed = keyCallbackLevelOne, mousePressed = clickOnButton)
    bar = Bar(0)
    addStatusBar(20)
    setStatusText("Dein Score: " + str(bar.score))
    addActor(bar, Location(10, 10))
    addActor(Obstacle(), Location(random.randint(8,12), 0))
    
    show()
    doRun()