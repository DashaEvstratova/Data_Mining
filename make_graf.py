import matplotlib.pyplot as plt
import networkx as nx


def make_data():
    data = []
    with open("/home/daria/PycharmProjects/Data_Maining/data.txt") as f:
        while f.readline():
            n = f.readline().strip().split(", ")
            data.append([n[0], n[1]])
    return data


def make_graph():
    data = make_data()
    graph = nx.DiGraph()
    graph.add_edges_from(data)
    fig, ax = plt.subplots(figsize=(30, 30))
    nx.draw(graph, with_labels=True, ax=ax)
    plt.show()


make_graph()
