import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

from LEBL import LoadAirportStructure, AssignGate, GateOccupancy
# Importem TOT el que vam fer al pas anterior
from airport import *
from aircraft import *
from LEBL import *


# Variables globals
llista_aeroports = []
llista_vols = []
bcn = None


def carregar_fitxer():
    global llista_aeroports
    # Obre una finestra per buscar l'arxiu .txt
    filename = filedialog.askopenfilename(title="Selecciona l'arxiu d'aeroports", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_aeroports = LoadAirports(filename)
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_aeroports)} aeroports.")


def actualitzar_llista():
    # Esborra la llista visual i la torna a omplir
    listbox.delete(0, tk.END)
    for a in llista_aeroports:
        schengen_txt = "Sí" if a.schengen else "No"
        listbox.insert(tk.END, f"{a.code} | Lat: {a.lat:.2f} | Lon: {a.lon:.2f} | Schengen: {schengen_txt}")


def aplicar_schengen():
    for a in llista_aeroports:
        SetSchengen(a)
    actualitzar_llista()
    messagebox.showinfo("Èxit", "S'ha comprovat l'espai Schengen per a tots els aeroports.")


def afegir_aeroport():
    code = simpledialog.askstring("Codi", "Introdueix el codi ICAO (ex: LEBL):")
    if not code: return
    lat = simpledialog.askfloat("Latitud", "Introdueix la latitud (en graus decimals, ex: 41.29):")
    if lat is None: return
    lon = simpledialog.askfloat("Longitud", "Introdueix la longitud (en graus decimals, ex: 2.08):")
    if lon is None: return

    nou = Airport(code.upper(), lat, lon)
    SetSchengen(nou)  # Comprovem si és Schengen abans d'afegir-lo
    res = AddAirport(llista_aeroports, nou)

    if res == 0:
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"Aeroport {code.upper()} afegit correctament.")
    else:
        messagebox.showerror("Error", "Aquest aeroport ja existeix a la llista.")


def esborrar_aeroport():
    code = simpledialog.askstring("Codi", "Introdueix el codi de l'aeroport a esborrar:")
    if not code: return

    res = RemoveAirport(llista_aeroports, code.upper())
    if res == 0:
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"Aeroport {code.upper()} esborrat.")
    else:
        messagebox.showwarning("Atenció", "No s'ha trobat cap aeroport amb aquest codi.")


def guardar_schengen():
    res = SaveSchengenAirports(llista_aeroports, "schengen_interficie.txt")
    if res == 0:
        messagebox.showinfo("Èxit", "Aeroports Schengen guardats a l'arxiu 'schengen_interficie.txt'.")
    else:
        messagebox.showwarning("Atenció", "La llista està buida o hi ha hagut un error.")


def mostrar_grafic():
    if not llista_aeroports:
        messagebox.showwarning("Atenció", "Primer has de carregar els aeroports.")
        return
    PlotAirports(llista_aeroports)


def mostrar_mapa():
    if not llista_aeroports:
        messagebox.showwarning("Atenció", "Primer has de carregar els aeroports.")
        return
    res = MapAirports(llista_aeroports, "mapa_interficie.kml")
    if res == 0:
        messagebox.showinfo("Èxit", "Fitxer 'mapa_interficie.kml' creat! Obre'l amb Google Earth.")
    else:
        messagebox.showerror("Error", "No s'ha pogut crear el mapa.")

# --- FUNCIONS EXISTENTS (V1) ---
def carregar_fitxer_aeroports():
    global llista_aeroports
    filename = filedialog.askopenfilename(title="Selecciona Airports.txt", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_aeroports = LoadAirports(filename)
        for a in llista_aeroports: SetSchengen(a)  # Activem Schengen per defecte
        actualitzar_llista_aeroports()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_aeroports)} aeroports.")


def actualitzar_llista_aeroports():
    listbox_ap.delete(0, tk.END)
    for a in llista_aeroports:
        schengen_txt = "Sí" if a.schengen else "No"
        listbox_ap.insert(tk.END, f"{a.code} | Lat: {a.lat:.2f} | Lon: {a.lon:.2f} | Sch: {schengen_txt}")


# --- NOVES FUNCIONS (V2) ---

def carregar_fitxer_vols():
    global llista_vols
    filename = filedialog.askopenfilename(title="Selecciona Arrivals.txt", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_vols = LoadArrivals(filename)
        actualitzar_llista_vols()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_vols)} vols.")


def actualitzar_llista_vols():
    listbox_vols.delete(0, tk.END)
    for v in llista_vols:
        listbox_vols.insert(tk.END, f"{v.id} | {v.origin} -> BCN | {v.time} | {v.airline}")


def mostrar_grafic_vols():
    if not llista_vols:
        messagebox.showwarning("Atenció", "Primer carrega els vols.")
        return
    # Pots triar quin gràfic mostrar o fer dos botons
    PlotAirlines(llista_vols)


def mostrar_grafic_tipus_vols():
    if not llista_vols:
        messagebox.showwarning("Atenció", "Primer carrega els vols.")
        return
    PlotFlightsType(llista_vols)


def generar_mapa_trajectories():
    if not llista_vols:
        messagebox.showwarning("Atenció", "No hi ha vols per mapejar.")
        return
    # MapFlights ja crea el fitxer "flights.kml" segons el teu codi
    MapFlights(llista_vols)
    messagebox.showinfo("Èxit", "Fitxer 'flights.kml' creat amb les trajectòries.")


def guardar_vols_llunyans():
    # Important: Recorda arreglar el 'return' de la teva funció LongDistanceArrivals!
    vols_llunyans = LongDistanceArrivals(llista_vols)
    if not vols_llunyans:
        messagebox.showinfo("Info", "No hi ha vols de més de 2000km.")
        return

    res = SaveFlights(vols_llunyans, "long_distance_flights.txt")
    if res == 0:
        messagebox.showinfo("Èxit", f"S'han guardat {len(vols_llunyans)} vols llunyans.")

# --- NOVES FUNCIONS (V3) ---
def carregar_aeroport():
    global bcn

    result = LoadAirportStructure("LEBL.txt")

    if result == -1 or result is None:
        print("Error carregant aeroport")
        bcn = None
        return

    bcn = result

    print("Aeroport carregat correctament")

def assignar_gate_ui():
    global bcn

    if bcn is None or not hasattr(bcn, "terminals"):
        print("Primer carrega l'aeroport")
        return

    aircraft = Aircraft("TEST123", "AEE", True)

    try:
        res = AssignGate(bcn, aircraft)
    except Exception as e:
        print("Error assignant gate:", e)
        return

    if res == -1:
        print("No s'ha pogut assignar gate")
    else:
        print("Gate assignat correctament")


def mostrar_gates():
    global bcn

    if bcn is None or not hasattr(bcn, "terminals"):
        print("No hi ha aeroport carregat")
        return

    try:
        dades = GateOccupancy(bcn)
    except Exception as e:
        print("Error llegint gates:", e)
        return

    listbox_vols.delete(0, tk.END)

    for g in dades:
        estat = "Ocupat" if g["occupied"] else "Lliure"
        aircraft = g["aircraft_id"] if g["aircraft_id"] != "" else "-"
        text = f"{g['name']} - {estat} - {aircraft}"
        listbox_vols.insert(tk.END, text)

# --- DISSENY DE LA INTERFÍCIE (ÚNICA FINESTRA) ---
finestra = tk.Tk()
finestra.title("Gestió completa aeroports - V1 + V2 + V3")
finestra.geometry("900x600")


# V1

frame_llista = tk.Frame(finestra)
frame_llista.pack(side=tk.RIGHT, padx=15, pady=15, expand=True, fill=tk.BOTH)

frame_botons = tk.Frame(finestra)
frame_botons.pack(side=tk.LEFT, padx=15, pady=15, fill=tk.Y)


tk.Button(frame_botons, text="1. Carregar Aeroports", command=carregar_fitxer, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="2. Aplicar Schengen", command=aplicar_schengen, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="3. Afegir Aeroport", command=afegir_aeroport, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="4. Esborrar Aeroport", command=esborrar_aeroport, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="5. Guardar Schengen", command=guardar_schengen, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="6. Mostrar Gràfic", command=mostrar_grafic, width=20, bg="#cce5ff").pack(pady=5)
tk.Button(frame_botons, text="7. Crear Mapa (KML)", command=mostrar_mapa, width=20, bg="#d4edda").pack(pady=5)


tk.Label(frame_llista, text="Dades dels aeroports:", font=("Arial", 10, "bold")).pack(anchor="w")

scrollbar = tk.Scrollbar(frame_llista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_llista, yscrollcommand=scrollbar.set, width=50, font=("Consolas", 10))
listbox.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=listbox.yview)

# V2

tk.Label(frame_botons, text="\nVOLS (ARRIVALS)", font=("Arial", 10, "bold")).pack()

tk.Button(frame_botons, text="Carregar Arrivals.txt", command=carregar_fitxer_vols, width=20, bg="#cce5ff").pack(pady=2)
tk.Button(frame_botons, text="Gràfic Aerolínies", command=mostrar_grafic_vols, width=20).pack(pady=2)
tk.Button(frame_botons, text="Gràfic Tipus Vol", command=mostrar_grafic_tipus_vols, width=20).pack(pady=2)
tk.Button(frame_botons, text="Crear Mapa Trajectòries", command=generar_mapa_trajectories, width=20, bg="#d4edda").pack(pady=2)
tk.Button(frame_botons, text="Vols > 2000km", command=guardar_vols_llunyans, width=20).pack(pady=2)


tk.Label(frame_llista, text="\nLlista d'Aeroports:").pack(anchor="w")
listbox_ap = tk.Listbox(frame_llista, height=10, font=("Consolas", 9))
listbox_ap.pack(fill=tk.X, pady=5)

tk.Label(frame_llista, text="Llista de Vols:").pack(anchor="w")
listbox_vols = tk.Listbox(frame_llista, height=15, font=("Consolas", 9), bg="#f0f8ff")
listbox_vols.pack(fill=tk.BOTH, expand=True)


# V3

tk.Label(frame_botons, text="\n Gates BCN", font=("Arial", 10, "bold")).pack()

tk.Button(frame_botons, text="Carregar LEBL", command=carregar_aeroport, width=20).pack(pady=2)
tk.Button(frame_botons, text="Assignar Gate", command=assignar_gate_ui, width=20).pack(pady=2)
tk.Button(frame_botons, text="Mostrar Gates", command=mostrar_gates, width=20).pack(pady=2)

tk.Button(frame_botons, text="Plot Gates", command=lambda: print(GateOccupancy(bcn)), width=20).pack(pady=2)
# SOLO UNA MAINLOOP
finestra.mainloop()