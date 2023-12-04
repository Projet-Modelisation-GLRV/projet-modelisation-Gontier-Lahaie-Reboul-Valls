import random
from time import sleep
import pygame
import math


# Couleurs
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Sommet:
    rayon = 20

    def __init__(self,id: int,acces: [], x: int, y: int) -> None:
        self.acces = acces
        self.id = id
        self.color = GREY
        self.x = x
        self.y = y
    
    def getId(self) -> int:
        return self.id
    
    def getAcces(self) -> str:
        retour = str(self.id) + ' a accès à '
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

    def __init__(self,type: int) -> None:
        # Paramètres de la fenêtre
        self.width, self.height = 500, 500
        self.sommets = []

        # Configuration de l'écran Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        if (type == 1) :
            self.generateType1()
        if (type == 2) :
            self.generateType2()

    def generateType1(self) -> None:
        nombreCases = 16
        sqrt = math.sqrt(nombreCases)
        largeurUtilisable = self.width*0.9
        hauteurUtilisable = self.height*0.9
        
        rayon = Sommet.rayon
        largeurUtilisable -= rayon*2
        hauteurUtilisable -= rayon*2

        coordonneeXInitiale = self.width - largeurUtilisable
        coordonneeX =  coordonneeXInitiale
        coordonneeY =  self.height - hauteurUtilisable

        for x in range(nombreCases):
            caseActuel = x + 1
            subArray = []
            colX = (int) (caseActuel % sqrt)
            if not colX == 1 :
                coordonneeX += largeurUtilisable/sqrt
            for y in range(nombreCases):
                y1 = y + 1
                colY = (int) (y1 % sqrt)
                if not (y1 == caseActuel) :
                    if (not ((colX == 1 or colX == 0) and (colY == 1 or colY == 0)) or colX == colY) :
                        suivCol = colX+1
                        if suivCol == sqrt :
                            suivCol = 0
                        prevCol = colX-1
                        if prevCol < 0 :
                            prevCol = sqrt-1
                        colProches = [prevCol,suivCol]
                        if (colY == colX or colY in colProches) and abs(caseActuel-y1) <= sqrt+1 : 
                            subArray.append(y1)
            self.sommets.append(Sommet(caseActuel, subArray, coordonneeX, coordonneeY))
            if colX == 0 :
                coordonneeX = coordonneeXInitiale 
                coordonneeY += hauteurUtilisable/sqrt
            
    def generateType2(self) -> None:
        nombreCases = 6
        cpt = 0            

        center = (self.width // 2, self.height // 2)
        rayon = 150
        angle_increment = (2 * math.pi) / nombreCases
        
        for x in range(nombreCases):
            caseActuel = x + 1
            subArray = []
            for y in range(nombreCases):
                y1 = y + 1
                if not (y1 == caseActuel) :
                    subArray.append(y1)
            angle = cpt * angle_increment
            coordonneeX = int(center[0] + rayon * math.cos(angle))
            coordonneeY = int(center[1] + rayon * math.sin(angle))
            cpt += 1
            self.sommets.append(Sommet(caseActuel, subArray, coordonneeX, coordonneeY))

    def sommetRandom(self) -> Sommet :
        return random.choice(self.sommets)
    
    def getSommetById(self, id) -> Sommet :
        for sommet in self.sommets:
            if sommet.id == id :
                return sommet
    
    def afficher(self) -> None :
        for point in self.sommets:
            pygame.draw.circle(self.screen, point.color, (point.x,point.y), Sommet.rayon)
            for accessedPointId in point.acces:
                accessedPoint = self.getSommetById(accessedPointId)
                pygame.draw.line(self.screen, BLACK, (point.x,point.y), (accessedPoint.x,accessedPoint.y), 2)
        pygame.display.flip()
        
pygame.init()


def partie(plateauType):

    positionsDepart = []
    plateau = Plateau
    gendarme = Bot
    voleur = Bot
    gameOver = bool
    gameOver = False

    plateau = Plateau(plateauType)

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

    pygame.display.flip()
    pygame.quit()




partie(1)
partie(2)