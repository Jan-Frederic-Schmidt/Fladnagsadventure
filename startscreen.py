from gamegrid import *
from level1 import level1
from level3 import level3

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
            
makeGameGrid(13, 13, 46, None, "sprites/town.jpg", False, mousePressed = clickOnButton)
buttonLevel1 = Button()
buttonLevel2 = Button()
buttonLevel3 = Button()
buttonLevel4 = Button()
buttonLevel5 = Button()
buttonLevel6 = Button()

addActor(buttonLevel1, Location(4, 5))
addActor(buttonLevel2, Location(6, 5))
addActor(buttonLevel3, Location(8, 5))
addActor(buttonLevel4, Location(4, 7))
addActor(buttonLevel5, Location(6, 7))
addActor(buttonLevel6, Location(8, 7))

show()
doRun()