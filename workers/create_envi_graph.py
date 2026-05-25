import pandas as pd
import json
import networkx as nx
from pyvis.network import Network

def run(hauteur=900):

    df = pd.read_excel("friends.xlsx")

    nodes = []
    links = []

    milieu_ids = {}

    next_id = len(df) + 1

    for i, row in df.iterrows():
        nodes.append({
            "id": i + 1,
            "name": row["Nom Prénom"],
            "type": "person"
        })

    for i, row in df.iterrows():
        for m in str(row["Milieu"]).split("/"):
            m = m.strip()
            if not m or m == "nan":
                continue
            if m not in milieu_ids:
                milieu_ids[m] = next_id
                nodes.append({
                    "id": next_id,
                    "name": m,
                    "type": "milieu"
                })
                next_id += 1
            links.append({"source": i + 1, "target": milieu_ids[m]})

    G = nx.Graph()
    for node in nodes:
        G.add_node(node["id"], **node)
    for link in links:
        G.add_edge(link["source"], link["target"])

    for node_id, attrs in G.nodes(data=True):
        if attrs.get("type") == "milieu":
            G.nodes[node_id]["label"] = attrs["name"]
            G.nodes[node_id]["color"] = "#f39c12"
            G.nodes[node_id]["shape"] = "square"
            G.nodes[node_id]["size"] = 30 + G.degree(node_id) * 1.05
        else:
            G.nodes[node_id]["label"] = attrs["name"]
            G.nodes[node_id]["color"] = "#3498db"
            G.nodes[node_id]["shape"] = "dot"
            G.nodes[node_id]["size"] = 10 + G.degree(node_id) * 1.05

    net = Network(height=f"{hauteur}px", width="100%", notebook=False)
    net.from_nx(G)

    html = net.generate_html()
    html = html.replace("<head>", '<head><meta charset="utf-8">')

    with open("friends_milieu.html", "w", encoding="utf-8") as f:
        f.write(html)

    return html