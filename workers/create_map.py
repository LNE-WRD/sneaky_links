import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

def run():

    df = pd.read_excel("friends.xlsx")

    geolocator = Nominatim(user_agent="friends_map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    ville_data = {}

    souad_location = geocode("Cologne, Germany")

    for _, row in df.iterrows():
        ville = str(row["lieu"]).strip()
        if not ville or ville == "nan":
            continue
        if ville not in ville_data:
            ville_data[ville] = []
        ville_data[ville].append(row["Nom Prénom"])

    carte = folium.Map(location=[46.5, 2.5], zoom_start=6)

    for ville, personnes in ville_data.items():
        location = geocode(ville)
        if location is None:
            continue
        distance = geodesic(
            (souad_location.latitude, souad_location.longitude),
            (location.latitude, location.longitude)
        ).km

        text = (
            f"<b>{ville}</b><br>"
            f"Distance à Souad : {distance:.1f} km<br>"
            f"Personnes : {', '.join(personnes)}"
        )

        folium.CircleMarker(
            location=[location.latitude, location.longitude],
            radius=5 + len(personnes) * 1.5,
            color="#3498db",
            fill=True,
            popup=folium.Popup(text, max_width=200)
            ).add_to(carte)

    carte.save("friends_map.html")
    
    return carte._repr_html_()
