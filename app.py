import streamlit as st
import streamlit.components.v1 as components

from workers import create_base_graph, create_envi_graph, create_map
from workers import db
from workers.db import init_db, lire_tout, ajouter, modifier, supprimer

db.init_db()

st.set_page_config(layout="wide")
st.title("Sneaky links")

st.sidebar.markdown("""
UwU

Cette appli possède 3 visualisations :

- **Graphe des amis** : un graphe de tous les amis, avec les liens que chacun entretient

- **Graphe des milieux** : un graphe qui relie les amis selon le milieu dont ils font partie (ex : Collège, etc)

- **Carte** : une carte qui montre où se trouvent les amis, avec la distance à toi <3

                    Il y a également un onglet Gestion. Celui ci te permet de mettre à jour les infos sur tes amis, d'en ajouter ou d'en supprimer.
                    Tu peux aussi ajouter une nouvelle variable (par exemple la date de rencontre), mais sans mise à jour de l'appli, il n'y aura pas de visuels sur ces infos supplémentaire.

Tu peux cliquer sur les éléments des graphs pour afficher certaines infos
""")

hauteur = st.sidebar.slider("Hauteur des graphes", min_value=400, max_value=1200, value=900, step=50)

tab1, tab2, tab3, tab4 = st.tabs(["Gestion","Graphe des amis", "Graphe des milieux", "Carte"])

with tab1:
    st.subheader("Ajouter une personne")
    with st.form("ajout"):
        name = st.text_input("Nom Prénom")
        milieu = st.text_input("Milieu (séparés par /)")
        statut = st.text_input("Statut")
        lieu = st.text_input("Lieu")
        if st.form_submit_button("Ajouter"):
            db.ajouter(name=name, milieu=milieu, statut=statut, lieu=lieu)
            st.success(f"{name} ajouté !")   

    st.subheader("Modifier les attributs d'une personne")
    rows = db.lire_tout()
    noms = {row[1]: row[0] for row in rows}
    choix_modif = st.selectbox("Personne à modifier", list(noms.keys()))
    
    if choix_modif:
        row = [r for r in rows if r[1] == choix_modif][0]
        with st.form("modif"):
            name = st.text_input("Nom Prénom", value=row[1])
            milieu = st.text_input("Milieu", value=row[2])
            statut = st.text_input("Statut", value=row[3])
            lieu = st.text_input("Lieu", value=row[4])
            if st.form_submit_button("Modifier"):
                db.modifier(noms[choix_modif], name=name, milieu=milieu, statut=statut, lieu=lieu)
                st.success(f"{name} modifié !")

        st.subheader("Supprimer une personne")
    choix_suppr = st.selectbox("Personne à supprimer", list(noms.keys()), key="suppr")
    if st.button("Supprimer"):
        db.supprimer(noms[choix_suppr])
        st.success(f"{choix_suppr} supprimé !")

with tab2:
    components.html(create_base_graph.run(), height=hauteur)

with tab3:
    components.html(create_envi_graph.run(), height=hauteur)

with tab4:
    components.html(create_map.run(), height=hauteur)
