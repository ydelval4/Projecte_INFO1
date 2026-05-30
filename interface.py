import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk

from LEBL import LoadAirportStructure, AssignGate, GateOccupancy
# Importem TOT el que vam fer al pas anterior
from airport import *
from aircraft import *

# Variables globals
llista_aeroports = []
llista_vols = []
bcn = None
estat_var = None

def actualitzar_estat(text):
    if estat_var:
        estat_var.set(text)


def carregar_fitxer():
    global llista_aeroports
    # Obre una finestra per buscar l'arxiu .txt
    filename = filedialog.askopenfilename(title="Selecciona l'arxiu d'aeroports", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_aeroports = LoadAirports(filename)
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_aeroports)} aeroports.")


def actualitzar_llista():

    listbox_ap.delete(0, tk.END)

    for a in llista_aeroports:

        schengen_txt = "Sí" if a.schengen else "No"

        listbox_ap.insert(
            tk.END,
            f"{a.code} | Lat:{a.lat:.2f} | Lon:{a.lon:.2f} | Schengen:{schengen_txt}")


def aplicar_schengen():
    for a in llista_aeroports:
        SetSchengen(a)
    actualitzar_llista()
    messagebox.showinfo("Èxit", "S'ha comprovat l'espai Schengen per a tots els aeroports.")


def afegir_aeroport():

    finestra_add = tk.Toplevel(finestra)
    finestra_add.title("Afegir Aeroport")
    finestra_add.geometry("350x250")
    finestra_add.resizable(False, False)

    tk.Label(
        finestra_add,
        text="Nou Aeroport",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=10)

    tk.Label(finestra_add, text="Codi ICAO").pack()
    entry_code = tk.Entry(finestra_add)
    entry_code.pack(fill="x", padx=20)

    tk.Label(finestra_add, text="Latitud").pack(pady=(10,0))
    entry_lat = tk.Entry(finestra_add)
    entry_lat.pack(fill="x", padx=20)

    tk.Label(finestra_add, text="Longitud").pack(pady=(10,0))
    entry_lon = tk.Entry(finestra_add)
    entry_lon.pack(fill="x", padx=20)

    def guardar():

        try:
            code = entry_code.get().upper()
            lat = float(entry_lat.get())
            lon = float(entry_lon.get())

            nou = Airport(code, lat, lon)

            SetSchengen(nou)

            res = AddAirport(llista_aeroports, nou)

            if res == 0:

                actualitzar_llista()
                actualitzar_llista_aeroports()

                actualitzar_estat(
                    f"Aeroport {code} afegit correctament")
                messagebox.showinfo(
                    "Èxit",
                    f"Aeroport {code} afegit correctament")
                finestra_add.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Aquest aeroport ja existeix")
        except:
            messagebox.showerror(
                "Error",
                "Valors incorrectes")
    tk.Button(
        finestra_add,
        text="Guardar Aeroport",
        bg="#2E7D32",
        fg="white",
        command=guardar
    ).pack(pady=20)


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

        text = (
            f"✈ {v.id} | "
            f"{v.origin} → BCN | "
            f"{v.time} | "
            f"{v.airline}"
        )

        listbox_vols.insert(tk.END, text)


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
    try:
        result = LoadAirportStructure("Terminals.txt")
        if result == -1 or result is None:

            messagebox.showerror(
                "Error",
                "No s'ha pogut carregar l'aeroport")
            return

        bcn = result
        actualitzar_estat(
            "Estructura LEBL carregada")

        messagebox.showinfo(
            "Èxit",
            "Aeroport carregat correctament")

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e))

def assignar_gate_ui():
    global bcn, llista_vols

    if bcn is None or not hasattr(bcn, "terminals"):
        print("Primer carrega l'aeroport")
        return

    #Assignem gates a tots els vols carregats
    if not llista_vols:
        print("Primer carrega els vols (Arrivals)")
        return

    assignats = 0
    errors = 0
    for v in llista_vols:
        res = AssignGate(bcn, v)
        if res == -1:
            errors += 1
        else:
            assignats += 1

    print(f"Gates assignats: {assignats} | No assignats: {errors}")
    messagebox.showinfo("Assignació completada",
                        f"Assignats: {assignats}\nNo assignats: {errors}")

def mostrar_gates():

    global bcn

    if bcn is None:

        messagebox.showwarning(
            "Atenció",
            "Primer carrega LEBL")

        return

    dades = GateOccupancy(bcn)

    listbox_vols.delete(0, tk.END)

    for g in dades:

        estat = "Ocupat" if g["occupied"] else "Lliure"

        aircraft = (
            g["aircraft_id"]
            if g["aircraft_id"] != ""
            else "-")

        text = (
            f"{g['name']} | "
            f"{estat} | "
            f"{aircraft}")

        listbox_vols.insert(tk.END, text)

    actualitzar_estat(
        "Gates mostrats")

# =========================
# VENTANA PRINCIPAL
# =========================

COLOR_FONDO = "#F5F7FA"
COLOR_PANEL = "#FFFFFF"
COLOR_PRINCIPAL = "#1F4E79"
COLOR_TEXTO = "#2C3E50"
COLOR_LISTA = "#FAFBFC"

finestra = tk.Tk()
finestra.title("Airport Management System")
finestra.geometry("1450x850")
finestra.configure(bg=COLOR_FONDO)

# =========================
# ESTILO BOTONES
# =========================

BTN_FONT = ("Segoe UI", 10, "bold")

def crear_boto(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=28,
        height=1,
        bg=COLOR_PRINCIPAL,
        fg="white",
        activebackground="#163A5C",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        font=BTN_FONT
    )

import tkinter as tk

# =========================
# VENTANA PRINCIPAL
# =========================

COLOR_FONDO = "#F5F7FA"
COLOR_PANEL = "#FFFFFF"
COLOR_PRINCIPAL = "#1F4E79"
COLOR_TEXTO = "#2C3E50"
COLOR_LISTA = "#FAFBFC"

finestra = tk.Tk()
finestra.title("Airport Management System")
finestra.geometry("1450x850")
finestra.configure(bg=COLOR_FONDO)

# =========================
# BOTÓN UNIFICADO
# =========================

BTN_FONT = ("Segoe UI", 10, "bold")

def crear_boto(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=28,
        bg=COLOR_PRINCIPAL,
        fg="white",
        activebackground="#163A5C",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        font=BTN_FONT
    )

# =========================
# TITULO
# =========================

tk.Label(
    finestra,
    text="AIRPORT MANAGEMENT SYSTEM",
    font=("Segoe UI", 22, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_PRINCIPAL
).pack(pady=15)

# =========================
# CONTENEDOR PRINCIPAL
# =========================

contenidor = tk.Frame(finestra, bg=COLOR_FONDO)
contenidor.pack(fill="both", expand=True, padx=15, pady=10)

# =========================
# PANEL BOTONES (SCROLLABLE)
# =========================

frame_botons_container = tk.Frame(contenidor, bg=COLOR_PANEL)
frame_botons_container.pack(side="left", fill="y", padx=(0,10))

canvas_botons = tk.Canvas(frame_botons_container, bg=COLOR_PANEL, highlightthickness=0, width=320)
scroll_botons = tk.Scrollbar(frame_botons_container, orient="vertical", command=canvas_botons.yview)

frame_botons = tk.Frame(canvas_botons, bg=COLOR_PANEL)

frame_botons.bind(
    "<Configure>",
    lambda e: canvas_botons.configure(scrollregion=canvas_botons.bbox("all"))
)

canvas_botons.create_window((0, 0), window=frame_botons, anchor="nw")
canvas_botons.configure(yscrollcommand=scroll_botons.set)

canvas_botons.pack(side="left", fill="both", expand=True)
scroll_botons.pack(side="right", fill="y")

# =========================
# PANEL AEROPUERTOS
# =========================

frame_aeroports = tk.Frame(contenidor, bg=COLOR_PANEL, bd=1, relief="solid")
frame_aeroports.pack(side="left", fill="both", expand=True, padx=(0,10))

# =========================
# PANEL VUELOS
# =========================

frame_vols = tk.Frame(contenidor, bg=COLOR_PANEL, bd=1, relief="solid")
frame_vols.pack(side="left", fill="both", expand=True)

# =========================
# AEROPORTS BOTONES
# =========================

tk.Label(frame_botons, text="AEROPORTS", font=("Segoe UI",12,"bold"), bg=COLOR_PANEL).pack(pady=10)

crear_boto(frame_botons,"Carregar Aeroports",carregar_fitxer).pack(pady=3)
crear_boto(frame_botons,"Aplicar Schengen",aplicar_schengen).pack(pady=3)
crear_boto(frame_botons,"Afegir Aeroport",afegir_aeroport).pack(pady=3)
crear_boto(frame_botons,"Esborrar Aeroport",esborrar_aeroport).pack(pady=3)
crear_boto(frame_botons,"Guardar Schengen",guardar_schengen).pack(pady=3)
crear_boto(frame_botons,"Mostrar Gràfic",mostrar_grafic).pack(pady=3)
crear_boto(frame_botons,"Crear Mapa KML",mostrar_mapa).pack(pady=3)

# =========================
# VOLS BOTONES
# =========================

tk.Label(frame_botons, text="VOLS", font=("Segoe UI",12,"bold"), bg=COLOR_PANEL).pack(pady=(20,10))

crear_boto(frame_botons,"Carregar Arrivals",carregar_fitxer_vols).pack(pady=3)
crear_boto(frame_botons,"Gràfic Aerolínies",mostrar_grafic_vols).pack(pady=3)
crear_boto(frame_botons,"Gràfic Tipus Vol",mostrar_grafic_tipus_vols).pack(pady=3)
crear_boto(frame_botons,"Mapa Trajectòries",generar_mapa_trajectories).pack(pady=3)
crear_boto(frame_botons,"Vols > 2000 km",guardar_vols_llunyans).pack(pady=3)

# =========================
# GATES BOTONES
# =========================

tk.Label(frame_botons, text="GATES BCN", font=("Segoe UI",12,"bold"), bg=COLOR_PANEL).pack(pady=(20,10))

crear_boto(frame_botons,"Carregar LEBL",carregar_aeroport).pack(pady=3)
crear_boto(frame_botons,"Assignar Gates",assignar_gate_ui).pack(pady=3)
crear_boto(frame_botons,"Mostrar Gates",mostrar_gates).pack(pady=3)

# =========================
# AEROPORTS LISTA
# =========================

tk.Label(frame_aeroports, text="AEROPORTS", font=("Segoe UI",13,"bold"), bg=COLOR_PANEL).pack(pady=10)

listbox_ap = tk.Listbox(frame_aeroports, font=("Consolas",10), bg=COLOR_LISTA, bd=0)
listbox_ap.pack(fill="both", expand=True, padx=10, pady=10)

# =========================
# VOLS LISTA
# =========================

tk.Label(frame_vols, text="VOLS I GATES", font=("Segoe UI",13,"bold"), bg=COLOR_PANEL).pack(pady=10)

listbox_vols = tk.Listbox(frame_vols, font=("Consolas",10), bg=COLOR_LISTA, bd=0)
listbox_vols.pack(fill="both", expand=True, padx=10, pady=10)

# =========================
# ESTADO
# =========================

estat_var = tk.StringVar(value="Sistema preparat")

tk.Label(
    finestra,
    textvariable=estat_var,
    bg=COLOR_PANEL,
    anchor="w",
    padx=10
).pack(side="bottom", fill="x")

finestra.mainloop()