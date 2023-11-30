import random
from time import sleep
import pygame
import math
import pprint

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
        print(self.acces)
        for sommet in self.acces :
            retour += str(sommet) + ', '
        return retour

class Bot:

    def __init__(self,team: str) -> None:
        
        self.team = team
        self.case = plateau1.sommetRandom()
        while self.case in positionsDepart :
            self.case = plateau1.sommetRandom()
        positionsDepart.append(self.case)
    
    def move(self,gendarme,voleur):
        gameOver = False
        self.case.color = GREY
        sommetsAccessibles = []
        for case in plateau1.sommets:
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
        if (type == 1) :
            nbRange = 6
            for x in range(nbRange):
                x1 = x + 1
                subArray = []
                for y in range(nbRange):
                    y1 = y + 1
                    if not (y1 == x1) :
                        subArray.append(y1)
                self.sommets.append(Sommet(x1, subArray))   
         

    def sommetRandom(self) -> Sommet :
        return random.choice(self.sommets)
    
    def getSommetById(self, id) -> Sommet :
        for sommet in self.sommets:
            if sommet.id == id :
                return sommet
    
    def afficher(self, nombreCases: int,screen: any,points: [] ) -> None :
        for point in points:
            pygame.draw.circle(screen, point.color, (point.x,point.y), 20)
            for accessedPointId in point.acces:
                accessedPoint = self.getSommetById(accessedPointId)
                pygame.draw.line(screen, BLACK, (point.x,point.y), (accessedPoint.x,accessedPoint.y), 2)
        pygame.display.flip()
        

positionsDepart = []
plateau1 = Plateau(1)
gendarme = Bot
voleur = Bot
gameOver = bool


def partie1():
    gameOver = False
    # Paramètres de la fenêtre
    width, height = 400, 400

    center = (width // 2, height // 2)
    radius = 150

    # Configuration de l'écran Pygame
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tour du gendarme")
    screen.fill(WHITE)

    clock = pygame.time.Clock()

    nombreCases = len(plateau1.sommets)
    points = plateau1.sommets
    angle_increment = (2 * math.pi) / nombreCases
    cpt = 0

    print(points)
    for point in points:
        print(point)
        angle = cpt * angle_increment
        point.x = int(center[0] + radius * math.cos(angle))
        point.y = int(center[1] + radius * math.sin(angle))
        cpt += 1


    gendarme = Bot('gendarme')

    plateau1.afficher(nombreCases,screen,points)


    pygame.display.set_caption("Tour du voleur") 

    #sleep(1)
    voleur = Bot('voleur')

    plateau1.afficher(nombreCases,screen,points)


    while not gameOver :
        print(gameOver)
        gameOver = gendarme.move(gendarme,voleur)
        pygame.display.set_caption("Tour du gendarme") 
        
        plateau1.afficher(nombreCases,screen,points)

        if gameOver :
            break
        sleep(1)

        gameOver = voleur.move(gendarme,voleur)
        pygame.display.set_caption("Tour du voleur") 
        
        plateau1.afficher(nombreCases,screen,points)

        sleep(1)

    pygame.quit()


partie1()
