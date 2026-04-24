from gamegrid import *

_M_HV = [(0,-1),(0,1),(-1,0),(1,0)]
_M_DI = [(-1,-1),(1,-1),(-1,1),(1,1)]

_MOVES = {
    'r': [7] + _M_HV,
    'b': [7] + _M_DI,
    'k': [1] + _M_HV + _M_DI,
    'q': [7] + _M_HV + _M_DI,
    'n': [1, (-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(-1,2),(1,2)],
    'p': [2, (0,1)],
    'P': [2, (0,-1)],
    'pc': [1, (-1,1),(1,1)],
    'Pc': [1, (-1,-1),(1,-1)]  
}

_MOVES_ROCH = {
'K': [((5,7),(6,7)), ((7,7),(5,7))],
'k': [((5,0),(6,0)), ((7,0),(5,0))],
'Q': [((3,7),(2,7)), ((0,7),(3,7))],
'q': [((3,0),(2,0)), ((0,0),(3,0))]
}

_GRUNDLINIE = [1,6]

brett = {(s, z): (s + z) % 2 == 0 for s in range(8) for z in range(8)} 

_FIG_WERTE = dict(P=1, K=99999,Q=9, R=5, B=3 , N=3,
                  p=-1, k=-99999,q=-9, r=-5, b=-3 , n=-3)

MAX_TIEFE = 4

def zugGenerator(weiss, position, rochaderecht):
    zuege = []
    pseudo, koenigsposition = _pseudoZugGenerator(weiss, position)
    for zug in pseudo:
        zug_ausfuehren(zug, position, koenigsposition)
        if not imSchach(weiss, position, koenigsposition[weiss]):
            zuege.append(zug)
        zug_zuruecknehmen(zug, position, koenigsposition)
    if rochaderecht[weiss] and not imSchach(weiss, position, koenigsposition[weiss]):
        _zuegeRochade(weiss, zuege, position, koenigsposition[weiss], rochaderecht[weiss])
    return zuege, koenigsposition

def _zuegeRochade(weiss, zuege, position, von, rochade):
    for roch in rochade:
        turmzug =  _MOVES_ROCH[roch][1]
        if turmzug not in {(z[1], z[2]) for z in zuege if not z[3]}:
            continue
        if all([not imSchach(weiss, position, zu) for zu in _MOVES_ROCH[roch][0]]):
            zuege.append(('K' if weiss else 'k', von, _MOVES_ROCH[roch][0][1], False, False, roch))

def imSchach(weiss,position, von):
    if von is None:
        return False
    for figs, moves in _MOVES.items():
        if figs in 'pP': continue
        for ds, dz in moves[1:]:
            for m in range(1,moves[0]+1):
                zu = (von[0] + ds * m, von[1]+dz*m)
                if zu not in brett: break
                if zu in position:
                    if position[zu].isupper() == weiss:
                        break
                    else:
                        if position[zu].lower() == figs:
                            return True
                        break
    return False
    



def zug_ausfuehren(zug, position, koenigsposition):
    fig, von, zu, capture, umwandlung, rochade = zug
    position[zu] = position.pop(von)
    if umwandlung:
        position[zu] = 'Q' if fig.isupper() else 'q'
    if fig in 'kK':
        koenigsposition[fig.isupper()] = zu
    if rochade:
        tv, tz = _MOVES_ROCH[rochade][1]
        position[tz] = position.pop(tv)
        
        
def zug_zuruecknehmen(zug, position, koenigsposition):
    fig, von, zu, capture, umwandlung, rochade = zug
    position[von] = position.pop(zu)
    if capture:
        position[zu] = capture
    if umwandlung:
        position[von] = 'P' if fig.isupper() else 'p'
    if fig in 'kK':
        koenigsposition[fig.isupper()] = von
    if rochade:
        tv, tz = _MOVES_ROCH[rochade][1]
        position[tv] = position.pop(tz)
        
            
            
def _pseudoZugGenerator(weiss, position):  
    pseudo = []
    koenigsposition = [None, None]
    for von, fig in position.items():
        if fig in 'kK':
            koenigsposition[fig.isupper()] = von
        if fig.isupper() != weiss: 
            continue
        if fig in 'pP':
            _zuegeBauern(weiss, fig, von, position, pseudo)
            continue
        f = fig.lower()
        if fig == 'K': 
            koenigsposition[True] = von
        elif fig == 'k':
            koenigsposition[False] = von
        richtungen = _MOVES[f][1:]
        multiplikator = _MOVES[f][0]
        for ds, dz in richtungen:
            for m in range(1, multiplikator + 1):
                zu = (von[0] + ds * m, von[1] + dz * m)  
                if zu not in brett:
                    break
                if zu in position and position[zu].isupper() == weiss:
                    break
                if zu in position and position[zu].isupper() != weiss:  
                    pseudo.append((fig, von, zu, position[zu], False, False))
                    break
                else:
                    pseudo.append((fig, von, zu, False, False, False))                
    return pseudo, koenigsposition

def _zuegeBauern(weiss, fig, von, position, pseudo):
    #(Angelo) Stiller Zug (HILFE ICH KANN NICHT MEHR!!!!!!)
    for ds, dz in _MOVES[fig][1:]:
        for m in range(1, _MOVES[fig][0] + 1):
            zu = (von[0], von[1] + dz * m)  
            if zu not in brett or zu in position: break
            if m==2 and von[1] != _GRUNDLINIE[weiss]: break
            if zu[1] in (0,7): 
                pseudo.append((fig, von, zu, False, True, False))
            else:   
                pseudo.append((fig, von, zu, False, False, False))
    #(Xaver) Schalg(er)zug (Die Stimmen werden Lauterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr...Sie kommen...)
    for ds, dz in _MOVES[fig+'c'][1:]:
        zu = (von[0]+ ds, von[1] + dz)  
        if zu not in position: continue
        if position[zu].isupper()== weiss: continue
        if zu[1] in (0,7): 
            pseudo.append((fig, von, zu, position[zu], True, False))
        else:   
            pseudo.append((fig, von, zu, position[zu], False, False))         

def bewerte_position(position):
    return sum(_FIG_WERTE[fig] for fig in position.values())           
                                 
def minimax(tiefe, alpha, beta, weiss, position, rochaderecht):
    if tiefe == MAX_TIEFE:
        return (bewerte_position(position), None)
    zugliste, koenigsposition = zugGenerator(weiss, position, rochaderecht)
    if not zugliste:
        if not imSchach(weiss, position, koenigsposition[weiss]):
            return (0, None)
        else:
            return (-99999+tiefe if weiss else 99999-tiefe, None)
    beste_bewertung = -99999 if weiss else 99999
    bester_zug = None
    for zug in zugliste:
        safe_roch = rochaderecht[:]
        zug_ausfuehren(zug, position, koenigsposition)
        wert, _ = minimax(tiefe+1, alpha, beta, not weiss, position, rochaderecht)
        zug_zuruecknehmen(zug, position, koenigsposition)
        rochaderecht = safe_roch
        if weiss:
            if wert > beste_bewertung:
                beste_bewertung = wert
                bester_zug = zug
            alpha = max(alpha, wert)
        else:
            if wert < beste_bewertung:
                beste_bewertung = wert
                bester_zug = zug
            beta = min(beta, wert)
        if alpha >= beta:
            break
    return beste_bewertung, bester_zug