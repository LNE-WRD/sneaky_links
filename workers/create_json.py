import pandas as pd
import json
import openpyxl

df = pd.read_excel("friends.xlsx")

nodes = []
links = []

# Créer les noeuds
for i, row in df.iterrows():
    nodes.append({
        "id": i,
        "name": row["Nom Prénom"],
        "milieu": [m.strip() for m in str(row["Milieu"]).split("/")],
        "statut": row["statut"],
        "lieu": row["lieu"]
    })

# Créer un dictionnaire nom -> id pour retrouver les ids
name_to_id = {row["Nom Prénom"]: i for i, row in df.iterrows()}

# Créer les liens
for i, row in df.iterrows():
    if pd.notna(row["edges"]):
        targets = [t.strip() for t in str(row["edges"]).split(",")]
        for target in targets:
            if target in name_to_id:
                links.append({
                    "source": i,
                    "target": name_to_id[target]
                })

new_id = 999
nodes.append({
    "id": new_id,
    "name": "Souad",
    "milieu": [""],
    "statut": "MAIN CHARACTER",
    "lieu": "None"
})

# Lier à tous les autres noeuds
existing_ids = [n["id"] for n in nodes if n["id"] != new_id]
for target_id in existing_ids:
    links.append({"source": new_id, "target": target_id})

graph = {"nodes": nodes, "links": links}

with open("friends.json", "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

print("Done !")