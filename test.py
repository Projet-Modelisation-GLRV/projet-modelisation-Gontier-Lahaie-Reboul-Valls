import heapq
import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def createGame(n, distanceBetweenPlayers=3):
    # Génération d'un graphe aléatoire de taille n
    graphe = nx.gnm_random_graph(n, n * 2)
    # Placer un gendarme et un voleur aléatoirement sur le graphe
    gendarme = np.random.randint(0, n)
    voleur = np.random.randint(0, n)

    # Tant que le gendarme et le voleur n'ont pas "distanceBetweenPlayers" cases de distance, changer la position du voleur
    while (gendarme == voleur) or (
            nx.shortest_path_length(graphe, source=gendarme, target=voleur) < distanceBetweenPlayers):
        voleur = np.random.randint(0, n)

    return graphe, gendarme, voleur


def getNextMoveWithNetworkx(graphe, gendarme, voleur):
    # Récuperation du chemin le plus court pour le gendarmer afin de rattraper le voleur
    gendarmePath = nx.shortest_path(graphe, source=gendarme, target=voleur)

    voleurNextMove = None
    # Récuperation des voisins du voleur
    voleurNeighbors = list(graphe.neighbors(voleur))
    voleurPath = []
    # Stocker dans une liste les meilleurs chemins entre les voisins du voleur et le gendarme
    for neighbor in voleurNeighbors:
        voleurPath.append(nx.shortest_path(graphe, source=neighbor, target=gendarme))

    # Trier les résultats en fonction de la longueur
    voleurPath.sort(key=len)

    # Le prochain meilleur coup du voleur est donc le dernier chemin
    voleurNextMove = voleurPath[-1][0]
    return gendarmePath[1], voleurNextMove


def showGraph(graphe, gendarme=None, voleur=None, nextGendarmeMove=None, nextVoleurMove=None):
    # Vérifier si un gendarme et un voleur doivent être affichés
    if not (gendarme is None and voleur is None):
        colors = []
        # Pour chaque noeud du graphe, ajouter la couleur associé si c'est un gendarme, voleur ou prochain coup
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

        pos = nx.spring_layout(graphe)
        nx.draw(graphe, pos, node_color=colors, with_labels=True)

    # Sinon (lorsque aucun joueur ne doit être affiché)
    else:
        pos = nx.spring_layout(graphe)
        nx.draw(graphe, pos, with_labels=True)

    plt.show()


def dijkstra(graph, start, end):
    # Définition a la valeur Infini de chacun des noeuds du graphe
    distances = {node: float('infinity') for node in graph.nodes}

    # Définition du nœud de départ a 0
    distances[start] = 0

    # Initialisation d'une file de priorité avec la distance du départ
    priority_queue = [(0, start)]

    # Tant que la file de priorité n'est pas vide
    while priority_queue:
        # Récupération du nœud avec la plus petite distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Si le noeuf courrant est le noeuf final, sortir de la boucle tant que
        if current_node == end:
            break

        # Pour chacun des voisins du noeud courant
        for neighbor in graph.neighbors(current_node):
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruction du chemin le plus court en partant de la fin
    path = [end]
    # Tant que le nœud courant n'est pas celui de départ
    while path[-1] != start:
        for neighbor in graph.neighbors(path[-1]):
            if distances[neighbor] == distances[path[-1]] - 1:
                path.append(neighbor)
                break

    # Retourner le chemin inversé
    return path[::-1]


def getNextMoveWithDijkstraAlgo(graphe, gendarme, voleur):
    # Récupération du chemin le plus court pour le gendarme afin de rattraper le voleur
    gendarmePath = dijkstra(graphe, gendarme, voleur)

    voleurNextMove = None
    # Récupération des voisins du voleur
    voleurNeighbors = list(graphe.neighbors(voleur))
    # Recherche du voisin du voleur le plus éloigné du gendarme avec le chemin le plus court
    max_distance = -1
    for neighbor in voleurNeighbors:
        distance = len(dijkstra(graphe, neighbor, gendarme))
        if distance > max_distance:
            max_distance = distance
            voleurNextMove = neighbor

    return gendarmePath[1], voleurNextMove


def demo_dijkstra():
    # Création d'un jeu aléatoire de n sommets
    graphe, gendarme, voleur = createGame(10, 2)

    # Récupération du prochain déplacement du gendarme et du voleur avec Networkx
    nextGendarmeMove, nextVoleurMove = getNextMoveWithNetworkx(graphe, gendarme, voleur)
    showGraph(graphe, gendarme, voleur, nextGendarmeMove, nextVoleurMove)

    # Récupération du prochain déplacement du gendarme et du voleur avec l'algorithme de Dijkstra
    nextGendarmeMove, nextVoleurMove = getNextMoveWithDijkstraAlgo(graphe, gendarme, voleur)
    showGraph(graphe, gendarme, voleur, nextGendarmeMove, nextVoleurMove)


def isDominated(graphe, node):
    # Un nœud est dominé si un autre nœud peut atteindre tous ses voisins en un coup
    # Récupération des voisins du nœud
    neighbors = set(graphe.neighbors(node))

    for currentNode in graphe.nodes:
        if currentNode != node:
            # Récupération des voisins du nœud courant
            currentNeighbors = set(graphe.neighbors(currentNode))
            currentNeighbors.add(currentNode)

            # Vérifier si les voisins du nœud en question sont inclus dans les voisins du nœud courant
            if neighbors <= currentNeighbors:
                print(f"Le nœud {node} est dominé par le nœud {currentNode}")
                return True

    return False


def dismantle(graphe, tentative):
    # Retirer un sommet afin de démanteler le graphe (tester si il est cop-win)

    # Choisir un sommet aléatoirement parmi les sommets du graphe
    nodes = list(graphe.nodes)
    node = random.choice(nodes)

    tentative += 1

    # Suppression du sommet si il est dominé par un autre sommet
    if isDominated(graphe, node):
        graphe.remove_node(node)
        tentative = 0
        time.sleep(1)
        showGraph(graphe)

    return graphe, tentative


def isCyclic(graphe):
    # tester si le graphe est composé uniquement d'un cycle
    for node in graphe.nodes:
        if len(list(graphe.neighbors(node))) != 2:
            return False
    return True


def isPrism(graphe):
    if graphe.number_of_nodes() == 6 and graphe.number_of_edges() == 9:
        for node in graphe.nodes:
            if len(list(graphe.neighbors(node))) != 3:
                return False
        return True


def demo_cop_win(plateau = createGame(10, 2)[0]):
    # Création d'un jeu aléatoire de n sommets
    graphe = plateau
    showGraph(graphe)

    tentative = 0
    # Tant que le graphe n'est pas cop-win et qu'il n'est pas composé d'un cycle
    while not ((isCyclic(graphe) and graphe.number_of_nodes() > 4) or graphe.number_of_nodes() == 1 or tentative > 40):
        graphe, tentative = dismantle(graphe, tentative)

    if (isCyclic(graphe) and graphe.number_of_nodes() > 4) or isPrism(graphe or tentative > 40):
        print("Le graphe est robber-win")

    else:
        print("Le graphe est cop-win")
