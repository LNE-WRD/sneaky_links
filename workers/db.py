import sqlite3
import json
import os


DB_PATH = "friends.db"

def init_db():
    if os.path.exists(DB_PATH):
        return
    
    with open("friends.json", encoding="utf-8") as f:
        dta = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE personnes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                milieu TEXT,
                statut TEXT,
                lieu TEXT
        )
    """)

    for node in dta["nodes"]:
        if node.get("name") == "Souad":
            continue
        cur.execute(
            "INSERT INTO personnes VALUES (?, ?, ?, ?, ?)",
            (node["id"], node["name"], "/".join(node["milieu"]), node["statut"], node["lieu"])
        )

    conn.commit()
    conn.close()

def lire_tout():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM personnes")
    rows = cur.fetchall()
    conn.close()
    return rows

def ajouter(**kwargs):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    colonnes = ", ".join(kwargs.keys())
    placeholders = ",".join("?" for _ in kwargs)
    cur.execute(
        f"INSERT INTO personnes ({colonnes}) VALUES ({placeholders})",
        tuple(kwargs.values())
    )
    conn.commit()
    conn.close()

def modifier(id, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    colonnes = ", ".join(f"{k}=?" for k in kwargs)
    valeurs = list(kwargs.values()) + [id]
    cur.execute(f"UPDATE personnes SET {colonnes} WHERE id=?", valeurs)
    conn.commit()
    conn.close()

def supprimer(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM personnes WHERE id=?", (id,))
    conn.commit()
    conn.close()