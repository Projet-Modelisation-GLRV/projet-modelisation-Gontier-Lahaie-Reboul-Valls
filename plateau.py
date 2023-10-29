import random
from time import sleep
import pygame
import math

pygame.init()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Sommet:

    def __init__(self,id: int,acces: []) -> None:
        self.acces = acces
        self.id = id
        self.color = BLACK

    
    def getId(self):
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
        self.case.color = BLACK
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
            self.sommets = [Sommet(1,[2,3,4,5,6]),Sommet(2,[1,3,4,5,6]),Sommet(3,[2,1,4,5,6]),Sommet(4,[2,3,1,5,6]),Sommet(5,[2,3,4,1,6]),Sommet(6,[2,3,4,5,1])]

    def sommetRandom(self) -> Sommet :
        return random.choice(self.sommets)
    
    def afficher(self, nombreCases: int,screen: any,points: [] ) -> None :
        for i in range(nombreCases):
            pygame.draw.circle(screen, plateau1.sommets[i].color, points[i], 20)
            for l in range(nombreCases):
                pygame.draw.line(screen, BLACK, points[i], points[(l + 1) % nombreCases], 2)
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
    points = []
    angle_increment = (2 * math.pi) / nombreCases
    for i in range(nombreCases):
        angle = i * angle_increment
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        points.append((x, y))


    gendarme = Bot('gendarme')

    plateau1.afficher(nombreCases,screen,points)


    pygame.display.set_caption("Tour du voleur") 

    sleep(3)
    voleur = Bot('voleur')

    plateau1.afficher(nombreCases,screen,points)


    while not gameOver :
        print(gameOver)
        gameOver = gendarme.move(gendarme,voleur)
        pygame.display.set_caption("Tour du gendarme") 
        
        plateau1.afficher(nombreCases,screen,points)

        if gameOver :
            break
        sleep(3)

        gameOver = voleur.move(gendarme,voleur)
        pygame.display.set_caption("Tour du voleur") 
        
        plateau1.afficher(nombreCases,screen,points)

        sleep(3)

    pygame.quit()


partie1()
