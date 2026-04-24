from gamegrid import *
import schachregelnV4

# Disclaimer:
# Ich habe das natürlich nicht ohne Hilfe programmieren können.
# Ich habe große Teile aus Tutorial Videos entnommen (https://youtu.be/STHZzsW7ODs?si=6VQf4vlOpH8pi0Hi, und weitere des Kanals)
# und damit das ganze für gamegrid funktioniert, habe ich die gamegrid-Befehl-Datenbank (https://jython.ch/index.php?inhalt_links=navigation.inc.php&inhalt_mitte=gamegrid/gamegriddoc.html),
# sowie, falls ich nicht weiter gekommen bin, AI (ChatGPT und/oder Gemini). Das aber nur für einzelne Teile/Befehle die ich nicht gefunden habe und nicht den ganzen Code.


actor = None
startLoc = None
selected_from = None     
zielfelder = set()  
spielende = False      

def pressCallback(e):
    global actor, startLoc, selected_from, zielfelder
    if spielende: return
    startLoc = toLocationInGrid(e.getX(), e.getY())
    actor = getOneActorAt(startLoc)
    if actor is None:
        return
    von = (startLoc.x, startLoc.y)  
    if von not in {z[1] for z in zuege}:
        actor = None
        return
    selected_from = von  
    zielfelder = {z[2] for z in zuege if z[1] == von}
    zeichneZielfelder(zielfelder)
    
def dragCallback(e):
    global actor
    if actor is None:
        return
    actor.setLocationOffset(e.getX() - 100 * startLoc.x - 50,
                            e.getY() - 100 * startLoc.y - 50)

def releaseCallback(e):
    global actor, weiss, zuege, position, koenigsposition, spielende
    if actor is None or spielende:
        return
    destLoc = toLocationInGrid(e.getX(), e.getY())
    zu = (destLoc.x, destLoc.y)  
    actor.setLocationOffset(0, 0)

  

    if zu in zielfelder:
        zug = [z for z in zuege if z[1] == selected_from and z[2] == zu][0]
        schachregelnV4.zug_ausfuehren(zug, position, koenigsposition)
        removeAllActors()
        zeichneFiguren(position)
        weiss = not weiss
        zuege, koenigsposition = schachregelnV4.zugGenerator(weiss, position, rochaderecht)
        if not zuege:
            print(("Weiss" if weiss else "Schwarz") + " ist ", end='')
            if schachregelnV4.imSchach(weiss, position, koenigsposition[weiss]):
                print('Matt')
            else:
                print('Patt')
            spielende = True
        elif spieler[weiss]:
            beste_bewertung, bester_zug = schachregelnV4.minimax(0, -9999999, 9999999, weiss, position, rochaderecht)
            if bester_zug is not None:
                schachregelnV4.zug_ausfuehren(bester_zug, position, koenigsposition)
                weiss = not weiss
                zuege, koenigsposition = schachregelnV4.zugGenerator(weiss, position, rochaderecht)
                if not zuege:
                    print(("Weiss" if weiss else "Schwarz") + " ist ", end='')
                    if schachregelnV4.imSchach(weiss, position, koenigsposition[weiss]):
                        print('Matt')
                    else:
                        print('Patt')
                    spielende = True
        showBrett(schachregelnV4.brett)
        removeAllActors()
        zeichneFiguren(position)
    else:
        actor.setLocation(startLoc)
    actor = None
        
    
def showBrett(brett):
    for (s, z), feld in brett.items():
        if (s + z) % 2 == 0:
            farbe = makeColor('#bb7f65')  
        else:
            farbe = makeColor('#e4bba7')  
        getBg().fillCell(Location(s, z), farbe)
    refresh()
    
def fen2position(fen):
    position, s ,z, rochaderecht = {}, 0,0, ['','']
    figurenstellung, zugrecht, rochaderechte, enpassant, zug50, zugnr = fen.split()
    for char in figurenstellung:
        if char.isalpha():
            position[(s,z)] = char
            s += 1
        elif char.isdigit():
            s+= int(char)
        else:
            s,z = 0, z+1
    for char in rochaderechte:
        if char == '-': 
            break
        rochaderecht[char.isupper()] += char  
    return position, zugrecht, rochaderecht

def ladeFiguren():
    fig2datei = dict(
        r='chessblack_2.png', n='chessblack_3.png', b='chessblack_4.png',
        q='chessblack_1.png', k='chessblack_0.png', p='chessblack_5.png',
        R='chesswhite_2.png', N='chesswhite_3.png', B='chesswhite_4.png',
        Q='chesswhite_1.png', K='chesswhite_0.png', P='chesswhite_5.png'
    )
    return fig2datei

def zeichneFiguren(p):
    for (s, z), fig in p.items():
        sprite = "sprites/" + figuren[fig]
        a = Actor(sprite)
        addActor(a, Location(s, z))
    refresh()
        
def zeichneZielfelder(felder):
    bg = getBg() 
    zielfeld_farbe = makeColor('#ecdfe0')
    bg.setPaintColor(zielfeld_farbe)
    for (s, z) in felder:
        bg.fillCircle(toPoint(Location(s, z)), 15)
    refresh()


#fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#fen = 'k1N2r2/8/B7/8/6q1/8/8/3QK3 w - - 0 1'
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

position, zugrecht, rochaderecht = fen2position(fen)
figuren = ladeFiguren()
weiss = (zugrecht == 'w')
print(("Weiss" if weiss else "Schwarz") + " ist am Zug")
zuege, koenigsposition = schachregelnV4.zugGenerator(weiss, position, rochaderecht)
spieler = [True, False]


        
makeGameGrid(8, 8, 100, None, False,
             mousePressed = pressCallback,
             mouseDragged = dragCallback,
             mouseReleased = releaseCallback)
setTitle("NOAHS ULTIMATE SCHACH")

showBrett(schachregelnV4.brett)
zeichneFiguren(position)
setSimulationPeriod(30)
if spielende:
    stop()
show()
doRun()
