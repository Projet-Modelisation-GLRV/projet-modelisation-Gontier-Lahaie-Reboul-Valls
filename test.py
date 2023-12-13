import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq


# Création d'un graphe non planaire de n sommets
def createGame(n, distanceBetweenPlayers=3):
    graphe = nx.gnm_random_graph(n, n * 2)
    # Placer un gendarme et un voleur aléatoirement sur le graphe
    gendarme = np.random.randint(0, n)
    voleur = np.random.randint(0, n)
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
    # Vérifier quel voisin du voleur est le plus éloigné du gendarme avec le chemin le plus court
    voleurPath = []
    for neighbor in voleurNeighbors:
        voleurPath.append(nx.shortest_path(graphe, source=neighbor, target=gendarme))
    voleurPath.sort(key=len)
    voleurNextMove = voleurPath[-1][0]
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

    pos = nx.spring_layout(graphe)
    nx.draw(graphe, pos, node_color=colors, with_labels=True)
    plt.show()


def dijkstra_shortest_path(graph, start, end):
    # Implémentation de l'algorithme de Dijkstra pour trouver le plus court chemin
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            distance = current_distance + 1  # Poids des arêtes égal à 1 dans ce cas
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruction du chemin
    path = [end]
    while path[-1] != start:
        for neighbor in graph.neighbors(path[-1]):
            if distances[neighbor] == distances[path[-1]] - 1:
                path.append(neighbor)
                break

    return path[::-1]


def getNextMoveWithAlgo(graphe, gendarme, voleur):
    # Récupération du chemin le plus court pour le gendarme afin de rattraper le voleur
    gendarmePath = dijkstra_shortest_path(graphe, gendarme, voleur)

    voleurNextMove = None
    # Récupération des voisins du voleur
    voleurNeighbors = list(graphe.neighbors(voleur))
    # Recherche du voisin du voleur le plus éloigné du gendarme avec le chemin le plus court
    max_distance = -1
    for neighbor in voleurNeighbors:
        distance = len(dijkstra_shortest_path(graphe, neighbor, gendarme))
        if distance > max_distance:
            max_distance = distance
            voleurNextMove = neighbor

    return gendarmePath[1], voleurNextMove


# Création d'un jeu aléatoire de n sommets
graphe, gendarme, voleur = createGame(10)
nextGendarmeMove, nextVoleurMove = getNextMoveWithNetworkx(graphe, gendarme, voleur)
showGraph(graphe, gendarme, voleur, nextGendarmeMove, nextVoleurMove)

nextGendarmeMove, nextVoleurMove = getNextMoveWithAlgo(graphe, gendarme, voleur)
showGraph(graphe, gendarme, voleur, nextGendarmeMove, nextVoleurMove)
