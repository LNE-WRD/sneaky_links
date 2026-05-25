import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

ordre = ["ex", "ami d'ami", "connaissance", "ami éloigné", "bestie d'enfance","ami", "poto sûr", "bestie", "soeur", "crush"]

cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom", ["#B72818", "#FFEBE8", "#E6AF00", "#EAF797", "#1D3ECF"]
)

def color_status(status):
    if status not in ordre:
        return "#ff9ffa"
    position = ordre.index(status) / (len(ordre) - 1)
    r, g, b, _ = cmap(position)
    return mcolors.to_hex((r, g, b))
