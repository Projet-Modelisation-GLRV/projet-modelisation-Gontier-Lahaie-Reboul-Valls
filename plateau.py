import random
from time import sleep
import pygame
import math

pygame.init()

# Couleurs
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Sommet:
    x = 0
    y = 0

    def __init__(self,id: int,acces: []) -> None:
        self.acces = acces
        self.id = id
        self.color = GREY

    def setX(self,coordinate) -> None:
        self.x = coordinate
    
    def setY(self,coordinate) -> None:
        self.y = coordinate
    
    def getId(self) -> int:
        return self.id
    
    def getAcces(self) -> str:
        retour = str(self.id) + ' a accés à '
        for sommet in self.acces :
            retour += str(sommet) + ', '
        return retour

class Bot:

    def __init__(self,team: str,plateau,positionsDepart) -> None:
        self.plateau = plateau
        self.team = team
        self.case = plateau.sommetRandom()
        while self.case in positionsDepart :
            self.case = plateau.sommetRandom()
        positionsDepart.append(self.case)
    
    def move(self,gendarme,voleur):
        gameOver = False
        self.case.color = GREY
        sommetsAccessibles = []
        for case in self.plateau.sommets:
            if case.id in self.case.acces :
                sommetsAccessibles.append(case)
        self.case = random.choice(sommetsAccessibles)
        newColor = RED
        ennemy = gendarme
        if self.team == 'gendarme' :
            newColor = BLUE
            ennemy = voleur

        if ennemy.case.id == self.case.id :
            newColor = BLUE
            gameOver = True
        self.case.color = newColor
        return gameOver

class Plateau:
    sommets = []

    def __init__(self,type: int) -> None:
        # Paramètres de la fenêtre
        self.width, self.height = 400, 400

        # Configuration de l'écran Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        if (type == 1) :
            self.generateType1()
            
    def generateType1(self) -> None:
        nombreCases = 6
        for x in range(nombreCases):
            x1 = x + 1
            subArray = []
            for y in range(nombreCases):
                y1 = y + 1
                if not (y1 == x1) :
                    subArray.append(y1)
            self.sommets.append(Sommet(x1, subArray))             

        center = (self.width // 2, self.height // 2)
        radius = 150
        points = self.sommets
        angle_increment = (2 * math.pi) / nombreCases
        cpt = 0
        for point in points:
            angle = cpt * angle_increment
            point.x = int(center[0] + radius * math.cos(angle))
            point.y = int(center[1] + radius * math.sin(angle))
            cpt += 1


    def sommetRandom(self) -> Sommet :
        return random.choice(self.sommets)
    
    def getSommetById(self, id) -> Sommet :
        for sommet in self.sommets:
            if sommet.id == id :
                return sommet
    
    def afficher(self) -> None :
        for point in self.sommets:
            pygame.draw.circle(self.screen, point.color, (point.x,point.y), 20)
            for accessedPointId in point.acces:
                accessedPoint = self.getSommetById(accessedPointId)
                pygame.draw.line(self.screen, BLACK, (point.x,point.y), (accessedPoint.x,accessedPoint.y), 2)
        pygame.display.flip()
        


def partie(plateauType):
    positionsDepart = []
    plateau = Plateau(plateauType)
    gendarme = Bot
    voleur = Bot
    gameOver = bool
    gameOver = False

    pygame.display.set_caption("Tour du gendarme")
    plateau.screen.fill(WHITE)

    clock = pygame.time.Clock()

    gendarme = Bot('gendarme',plateau,positionsDepart)

    plateau.afficher()


    pygame.display.set_caption("Tour du voleur") 

    #sleep(1)
    voleur = Bot('voleur',plateau,positionsDepart)

    plateau.afficher()


    while not gameOver :
        gameOver = gendarme.move(gendarme,voleur)
        pygame.display.set_caption("Tour du gendarme") 
        
        plateau.afficher()

        if gameOver :
            break
        sleep(1)

        gameOver = voleur.move(gendarme,voleur)
        pygame.display.set_caption("Tour du voleur") 
        
        plateau.afficher()

        sleep(1)

    pygame.quit()


partie(1)
