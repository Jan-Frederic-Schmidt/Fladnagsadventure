from gamegrid import *
import random
def level3():
    class Wizard(Actor):
        def __init__(self, score):
            Actor.__init__(self, True, "sprites/mbrobot.gif")
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
            
    class LostScreen(Actor):
        def __init__(self):
            Actor.__init__(self, True, "sprites/you_lost.gif")
            
    class NewGame(Actor):
        def __init__(self):
            Actor.__init__(self, True, "sprites/btn_renew_0.gif")    
    
    def keyCallbackLevelThree(e):
        keyCode = e.getKeyCode()
        if wizard.getX()!= 0 and wizard.getX() != 14:
            if keyCode == 65:
                wizard.setDirection(180)
                wizard.move()
            elif keyCode == 68:
                wizard.setDirection(0)
                wizard.move()
        else:
            wizard.turn(180)
            wizard.move()
            
    def clickOnButton(e):
        location = toLocationInGrid(e.getX(), e.getY())
        button = getOneActorAt(location, NewGame)
        if button != None:
            removeAllActors()
            addActor(wizard, Location(7, 14))
            addActor(Crystal(), Location(random.randint(0, 14),4))
            
    def catchCrystal():
        actor = getOneActorAt(wizard.getLocation(), Crystal)
        if actor != None:
            actor.removeSelf()
            wizard.score += 1
            setStatusText("Dein Score: " + str(wizard.score))
            if wizard.score < 5:
                addActor(Crystal(), Location(random.randint(0, 14),4))
            elif wizard.score < 15:
                addActor(Crystal(), Location(random.randint(0, 14),5))
            else:
                addActor(Crystal(), Location(random.randint(0, 14),6))
            
    def lostGame():
        removeAllActors()
        wizard.score = 0
        setStatusText("Dein Score: " + str(wizard.score))
        addActor(LostScreen(), Location(7,7))
        addActor(NewGame(), Location(7, 8))
    
    makeGameGrid(15, 15, 40, None, "sprites/town.jpg", False, keyPressed = keyCallbackLevelThree, mousePressed = clickOnButton)
    addStatusBar(20)
    wizard = Wizard(0)
    addActor(wizard, Location(7, 14))
    addActor(Crystal(), Location(random.randint(0, 14),4))
    setStatusText("Dein Score: " + str(wizard.score))
    
    show()
    doRun()