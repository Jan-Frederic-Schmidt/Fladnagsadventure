from gamegrid import *
from level3 import level3

class Button(Actor):
    def __init__(self):
        Actor.__init__(self, True, "sprites/btn_renew_0.gif")

def clickOnButton(e):
        location = toLocationInGrid(e.getX(), e.getY())
        button = getOneActorAt(location)
        if button == buttonLevel3:
            level3()
            
makeGameGrid(13, 13, 46, None, "sprites/town.jpg", False, mousePressed = clickOnButton)
buttonLevel1 = Button()
buttonLevel2 = Button()
buttonLevel3 = Button()
buttonLevel4 = Button()
buttonLevel5 = Button()
buttonLevel6 = Button()
buttonLevel7 = Button()
buttonLevel8 = Button()

addActor(buttonLevel1, Location(3, 3))
addActor(buttonLevel2, Location(5, 3))
addActor(buttonLevel3, Location(7, 3))
addActor(buttonLevel4, Location(9, 3))
addActor(buttonLevel5, Location(3, 5))
addActor(buttonLevel6, Location(5, 5))
addActor(buttonLevel7, Location(7, 5))
addActor(buttonLevel8, Location(9, 5))

show()
doRun()