import random

class Sommet:
    id
    acces = []

    def __init__(self,id,access) -> None:
        self.access = access
        self.id = id
    
    def getId(self):
        return self.id

class Plateau:
    sommets = []

    def __init__(self,type) -> None:
        if (type == 1) :
            self.sommets = [Sommet(1,[2,3,4,5,6]),Sommet(2,[1,3,4,5,6]),Sommet(3,[2,1,4,5,6]),Sommet(4,[2,3,1,5,6]),Sommet(5,[2,3,4,1,6]),Sommet(6,[2,3,4,5,1])]

    def sommetRandom(self) -> Sommet :
        return random.choice(self.sommets)
    
    def getSommets(self) -> str :
        retour = ''
        for sommet in self.sommets :
            retour += sommet.getAcces()
        return retour
        

class Bot:
    case = Sommet
    team

    def __init__(self) -> None:
        self.case = Plateau.sommetRandom()
        while self.case in positionsDepart :
            self.case = Plateau.sommetRandom()
        positionsDepart.append(self.case)
    
    def move(self):
        sommetsAccessibles = []
        for case in Plateau.sommets:
            if case.id in self.case.acces :
                sommetsAccessibles.append(case)
        self.case = random.choice(sommetsAccessibles)

        

gameOver = False

positionsDepart = []

plateau = Plateau(1)

print(plateau.sommetRandom().id)



