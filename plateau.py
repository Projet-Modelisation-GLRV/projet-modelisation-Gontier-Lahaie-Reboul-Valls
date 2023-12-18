import random

import networkx as nx

import gendarme_voleur as gv


# Création d'un graphe non planaire de n sommets
def createGraph(n, type='random', edges=any):
    graphe = nx.Graph()

    if type == 'square':
        graphe.add_nodes_from(range(1, 17))
        graphe.add_edges_from(
            [(1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (3, 7), (4, 8), (5, 6), (5, 9), (6, 7), (6, 10), (7, 8),
             (7, 11), (8, 12), (9, 10), (9, 13), (10, 11), (10, 14), (11, 12), (11, 15), (12, 16), (13, 14),
             (14, 15), (15, 16)])
        graphe.add_edges_from(
            [(1, 6), (2, 5), (2, 7), (3, 6), (3, 8), (4, 7), (5, 10), (6, 9), (6, 11), (7, 10), (7, 12),
             (8, 11), (9, 14), (10, 13), (10, 15), (11, 14), (11, 16), (12, 15)])
    if type == 'circle':
        graphe = nx.complete_graph(n)
        nx.circular_layout(graphe)
    if type == 'custom':
        # Ajout des arêtes
        graphe.add_edges_from(edges)

    return graphe

def position_plateau(plateau):
    # Renvoie une position aléatoire sur le graphe pour le gendarme et le voleur
    gendarme = random.choice(list(plateau.nodes))
    voleur = random.choice(list(plateau.nodes))

    # le voleur et le gendarme doivent avoir 3 de distance au moins
    while nx.shortest_path_length(plateau, gendarme, voleur) < 3:
        voleur = random.choice(list(plateau.nodes))
    return gendarme, voleur

#plateau = createGraph(0,'square')
#plateau = createGraph(0,'custom', [(0, 1), (0, 5), (1, 2), (1, 3), (1, 6), (2, 7), (2, 8), (3, 8), (4, 5),(4, 8), (5, 0), (5, 4), (6, 1), (6, 7), (7, 2), (7, 6), (7, 9),(8, 2), (8, 3), (8, 4), (8, 9), (9, 8), (9, 7)])
#plateau = createGraph(6,'circle')

#gv.demo_cop_win(plateau)
#gv.demo_cop_win()

#gv.demo_dijkstra()

#gendarme, voleur = position_plateau(plateau)
#gv.play(plateau, gendarme, voleur)
#gv.play(plateau, 0, 1)
#gv.play()
