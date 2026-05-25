import json
import networkx as nx
import importlib
import consts.gradient
importlib.reload(consts.gradient)
from pyvis.network import Network

from consts.gradient import color_status

def run(hauteur=900):
    with open("friends.json", encoding="utf-8") as f:
        dta = json.load(f)

    G = nx.node_link_graph(dta)

    for node_id, attrs in G.nodes(data=True):
        G.nodes[node_id]["color"] = color_status(attrs.get("statut", ""))

    for node_id, attrs in G.nodes(data=True):
        degree = G.degree(node_id)
        G.nodes[node_id]["label"] = attrs.get("name", str(node_id))
        G.nodes[node_id]["size"] = 10 + degree * 1.01

    net = Network(height=f"{hauteur}px", width="100%", notebook=False)
    net.from_nx(G)

    net.html = net.generate_html()
    net.html = net.html.replace("<head>", '<head><meta charset="utf-8">')
    with open("friends.html", "w", encoding="utf-8") as f:
        f.write(net.html)

    return net.html
