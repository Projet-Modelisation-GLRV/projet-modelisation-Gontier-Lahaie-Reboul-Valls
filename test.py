import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import spicy as sp


# Création d'un graphe non planaire de n sommets
def createGame(n, distanceBetweenPlayers=3):
    graphe = nx.gnm_random_graph(n, n * 2)
    # Placer un gendarme et un voleur aléatoirement sur le graphe
    gendarme = np.random.randint(0, n)
    voleur = np.random.randint(0, n)
    while (gendarme == voleur) or (nx.shortest_path_length(graphe, source=gendarme, target=voleur) < distanceBetweenPlayers):
        voleur = np.random.randint(0, n)

    return graphe, gendarme, voleur


def getNextMove(graphe, gendarme, voleur):
    # Récuperation du chemin le plus court pour le gendarmer afin de rattraper le voleur
    gendarmePath = nx.shortest_path(graphe, source=gendarme, target=voleur)

    voleurNextMove = None
    # Récuperation des voisins du voleur
    voleurNeighbors = list(graphe.neighbors(voleur))
    # Vérifier quel voisin du voleur est le plus éloigné du gendarme avec le chemin le plus court
    voleurPath = []
    for neighbor in voleurNeighbors:
        voleurPath.append(nx.shortest_path(graphe, source=neighbor, target=gendarme))
    voleurPath.sort(key=len)
    voleurNextMove = voleurPath[-1][1]
    return gendarmePath[1], voleurNextMove


def showGraph(graphe, gendarme, voleur, nextGendarmeMove=None, nextVoleurMove=None):
    # Afficher le graphe avec le prochain déplacement du gendarme et du voleur
    colors = []
    for i in range(graphe.number_of_nodes()):
        if i == gendarme:
            colors.append('blue')
        elif i == voleur:
            colors.append('red')
        elif i == nextGendarmeMove:
            colors.append('green')
        elif i == nextVoleurMove:
            colors.append('orange')
        else:
            colors.append('grey')

    # Afficher le graphe en utilisant un layout adapté au nombre de sommets du graphe
    if graphe.number_of_nodes() <= 10:
        pos = nx.circular_layout(graphe)
    elif graphe.number_of_nodes() <= 20:
        pos = nx.spring_layout(graphe)
    else:
        pos = nx.random_layout(graphe)

    nx.draw(graphe, pos, node_color=colors, with_labels=True)
    plt.show()

# Création d'un jeu aléatoire de n sommets
graphe, gendarme, voleur = createGame(21)
nextGendarmeMove, nextVoleurMove = getNextMove(graphe, gendarme, voleur)
showGraph(graphe, gendarme, voleur, nextGendarmeMove, nextVoleurMove)
