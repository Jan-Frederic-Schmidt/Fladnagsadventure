from gamegrid import *
import random

class LostScreen(Actor):
    def __init__(self):
        Actor.__init__(self, True, "sprites/you_lost.gif")
            
class WinScreen(Actor):
    def __init__(self):
         Actor.__init__(self, True, "sprites/you_win.gif")
            
class NewGame(Actor):
    def __init__(self):
        Actor.__init__(self, True, "H:\Informatik\Python/fladnagsAdventure/sprites/restart.png")

def startscreen():
    class Button(Actor):
        def __init__(self):
            Actor.__init__(self, False, "sprites/btn_renew_0.gif")

    def clickOnButton(e):
        location = toLocationInGrid(e.getX(), e.getY())
        button = getOneActorAt(location)
        if button == buttonLevel1:
            level1()
        if button == buttonLevel3:
            level3()
            
    makeGameGrid(16, 9, 45, None, "H:\Informatik\Python/fladnagsAdventure/sprites/Hintergrund_Start@169.png", False, mousePressed = clickOnButton)
    buttonLevel1 = Button()
    buttonLevel2 = Button()
    buttonLevel3 = Button()
    buttonLevel4 = Button()
    buttonLevel5 = Button()
    buttonLevel6 = Button()

    addActor(buttonLevel1, Location(5, 3))
    addActor(buttonLevel2, Location(7, 3))
    addActor(buttonLevel3, Location(9, 3))
    addActor(buttonLevel4, Location(5, 5))
    addActor(buttonLevel5, Location(7, 5))
    addActor(buttonLevel6, Location(9, 5))

    show()
    doRun()
    
def level1():
    class Bar(Actor):
        def __init__(self, score):
            Actor.__init__(self, "H:\Informatik\Python/fladnagsAdventure/sprites/fladnagFliegend@2x.png", 2)
            self.score = score
    
    class Obstacle(Actor):
        def __init__(self):
            Actor.__init__(self, "H:\Informatik\Python/fladnagsAdventure/sprites/vogelBlau@3x.png")
        
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
                if bar.score >= 20:
                    addActor(WinScreen(), Location(10, 9))
                    delay(1000)
                    startscreen() 
    
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
    
def level3():
    class Wizard(Actor):
        def __init__(self, score):
            Actor.__init__(self, "H:\Informatik\Python/fladnagsAdventure/sprites/fladnagLaufend@2x.png", 2)
            self.score = score    
    
    class Crystal(Actor):
        def __init__(self):
            Actor.__init__(self, "sprites/twentycent.png")
        
        def act(self):
            self.setDirection(90)
            self.move()
            if self.getY() == 15:
                lostGame()
            catchCrystal() 
    
    def keyCallbackLevelThree(e):
        keyCode = e.getKeyCode()
        if wizard.getX()!= 0 and wizard.getX() != 14:
            if keyCode == 65:
                wizard.setDirection(180)
                wizard.showNextSprite()
                wizard.move()
            elif keyCode == 68:
                wizard.setDirection(0)
                wizard.showNextSprite()
                wizard.move()
        else:
            wizard.turn(180)
            wizard.move()
            
    def clickOnButton(e):
        location = toLocationInGrid(e.getX(), e.getY())
        button = getOneActorAt(location, NewGame)
        if button != None:
            removeAllActors()
            addActor(wizard, Location(7, 13))
            addActor(Crystal(), Location(random.randint(0, 14),4))
            
    def catchCrystal():
        actor = getOneActorAt(wizard.getLocation(), Crystal)
        if actor != None:
            actor.removeSelf()
            wizard.score += 1
            setStatusText("Dein Score: " + str(wizard.score))
            if wizard.score >= 15:
                addActor(WinScreen(), Location(7,7))
                delay(1000)
                startscreen()
            if wizard.score < 5:
                addActor(Crystal(), Location(random.randint(0, 14),4))
            elif wizard.score < 10:
                addActor(Crystal(), Location(random.randint(0, 14),5))
            else:
                addActor(Crystal(), Location(random.randint(0, 14),6))
            
    def lostGame():
        removeAllActors()
        wizard.score = 0
        setStatusText("Dein Score: " + str(wizard.score))
        addActor(LostScreen(), Location(7,7))
        addActor(NewGame(), Location(7, 9))
    
    makeGameGrid(15, 15, 40, None, "sprites/town.jpg", False, keyPressed = keyCallbackLevelThree, mousePressed = clickOnButton)
    addStatusBar(20)
    wizard = Wizard(0)
    addActor(wizard, Location(7, 13))
    addActor(Crystal(), Location(random.randint(0, 14),4))
    setStatusText("Dein Score: " + str(wizard.score))
    
    show()
    doRun()
    
startscreen()