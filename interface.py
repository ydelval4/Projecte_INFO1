import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk

from LEBL import LoadAirportStructure, AssignGate, GateOccupancy
#Importem TOT el que vam fer als pasos anteriors

#Importemles funcions dels fitxers airport.py i aircraft.py
from aircraft import *
from airport import *

# Variables globals
llista_aeroports = []
llista_vols = []
bcn = None
#Variable per mostrar missatges de com està tot a la part inferior
estat_var = None

#Noves variables globals (V4)
llista_arrivals = []
llista_departures = []


#Actualitza el text de la barra d'estat inferior
def actualitzar_estat(text):
    if estat_var:
        estat_var.set(text)


#Deixa seleccionar un fitxer d'aeroports i carregar-lo
def carregar_fitxer():
    global llista_aeroports
    #Obre una finestra per buscar l'arxiu .txt
    filename = filedialog.askopenfilename(title="Selecciona l'arxiu d'aeroports", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_aeroports = LoadAirports(filename)
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_aeroports)} aeroports.")


#Actualitza la llista visual dels aeroports
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


#Obre una finestra per afegir un aeroport nou
def afegir_aeroport():
    #Creem una finestra nova
    finestra_add = tk.Toplevel(finestra)
    finestra_add.title("Afegir Aeroport")
    finestra_add.geometry("350x250")
    finestra_add.resizable(False, False)

    tk.Label(finestra_add, text="Nou Aeroport", font=("Segoe UI", 14, "bold")).pack(pady=10)
    tk.Label(finestra_add, text="Codi ICAO").pack()
    entry_code = tk.Entry(finestra_add)
    entry_code.pack(fill="x", padx=20)

    tk.Label(finestra_add, text="Latitud").pack(pady=(10,0))
    entry_lat = tk.Entry(finestra_add)
    entry_lat.pack(fill="x", padx=20)

    tk.Label(finestra_add, text="Longitud").pack(pady=(10,0))
    entry_lon = tk.Entry(finestra_add)
    entry_lon.pack(fill="x", padx=20)

    #Funció que es crida quan premem "Guardar"
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
                actualitzar_estat(f"Aeroport {code} afegit correctament")
                messagebox.showinfo("Èxit",f"Aeroport {code} afegit correctament")
                #Tanquem la finestra
                finestra_add.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Aquest aeroport ja existeix")
        except:
            messagebox.showerror(
                "Error",
                "Valors incorrectes")
    tk.Button(finestra_add,text="Guardar Aeroport",bg="#2E7D32",fg="white",command=guardar).pack(pady=20)


#Eminiar un aeroport posant el codi ICAO
def esborrar_aeroport():
    code = simpledialog.askstring("Codi", "Introdueix el codi de l'aeroport a esborrar:")
    if not code: return

    res = RemoveAirport(llista_aeroports, code.upper())
    if res == 0:
        actualitzar_llista()
        messagebox.showinfo("Èxit", f"Aeroport {code.upper()} esborrat.")
    else:
        messagebox.showwarning("Atenció", "No s'ha trobat cap aeroport amb aquest codi.")


#Guarda en un fitxer només els aeroports que són Schengen
def guardar_schengen():
    res = SaveSchengenAirports(llista_aeroports, "schengen_interficie.txt")
    if res == 0:
        messagebox.showinfo("Èxit", "Aeroports Schengen guardats a l'arxiu 'schengen_interficie.txt'.")
    else:
        messagebox.showwarning("Atenció", "La llista està buida o hi ha hagut un error.")


#Mostra un gràfic amb les dades dels aeroports
def mostrar_grafic():
    if not llista_aeroports:
        messagebox.showwarning("Atenció", "Primer has de carregar els aeroports.")
        return
    PlotAirports(llista_aeroports)


#Crea un mapa KML per obrir-lo amb Google Earth
def mostrar_mapa():
    if not llista_aeroports:
        messagebox.showwarning("Atenció", "Primer has de carregar els aeroports.")
        return
    res = MapAirports(llista_aeroports, "mapa_interficie.kml")
    if res == 0:
        messagebox.showinfo("Èxit", "Fitxer 'mapa_interficie.kml' creat! Obre'l amb Google Earth.")
    else:
        messagebox.showerror("Error", "No s'ha pogut crear el mapa.")

#Carrega el fitxer Airports.txt
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


#Noves funcions (V2)

def carregar_fitxer_vols():
    global llista_vols, llista_arrivals
    filename = filedialog.askopenfilename(title="Selecciona Arrivals.txt", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_vols = LoadArrivals(filename)
        llista_arrivals = llista_vols #Guardem a arrivals per a la v4
        actualitzar_llista_vols()
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_vols)} vols.")


def actualitzar_llista_vols():
    listbox_vols.delete(0, tk.END)
    for v in llista_vols:
        text = (f"{v.origin} → BCN | "f"{v.time} | "f"{v.airline}")
        listbox_vols.insert(tk.END, text)


def mostrar_grafic_vols():
    if not llista_vols:
        messagebox.showwarning("Atenció", "Primer carrega els vols.")
        return
    #Pots triar quin gràfic mostrar o fer dos botons
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
    #MapFlights ya crea el fitxer "flights.kml" segons el nostre codi
    MapFlights(llista_vols)
    messagebox.showinfo("Èxit", "Fitxer 'flights.kml' creat amb les trajectòries.")


def guardar_vols_llunyans():
    #Recordar arreglar el 'return' de la funció LongDistanceArrivals
    vols_llunyans = LongDistanceArrivals(llista_vols)
    if not vols_llunyans:
        messagebox.showinfo("Info", "No hi ha vols de més de 2000km.")
        return

    res = SaveFlights(vols_llunyans, "long_distance_flights.txt")
    if res == 0:
        messagebox.showinfo("Èxit", f"S'han guardat {len(vols_llunyans)} vols llunyans.")


#Noves funcions V3
def carregar_aeroport():
    global bcn
    try:
        result = LoadAirportStructure("Terminals.txt")
        if result == -1 or result is None:
            messagebox.showerror("Error","No s'ha pogut carregar l'aeroport")
            return
        #Guardem l'estructura carregada
        bcn = result
        actualitzar_estat(
            "Estructura LEBL carregada")
        messagebox.showinfo("Èxit","Aeroport carregat correctament")
    except Exception as e:
        messagebox.showerror("Error",str(e))


#Assigna portes als vols carregats
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
    messagebox.showinfo("Assignació completada",f"Assignats: {assignats}\nNo assignats: {errors}")


#Mostra totes les portes i el seu estat
def mostrar_gates():
    global bcn
    if bcn is None:
        messagebox.showwarning("Atenció","Primer carrega LEBL")
        return
    dades = GateOccupancy(bcn)
    listbox_vols.delete(0, tk.END)
    for g in dades:
        estat = "Ocupat" if g["occupied"] else "Lliure"
        aircraft = (g["aircraft_id"]
            if g["aircraft_id"] != ""
            else "-")
        text = (f"{g['name']} | "f"{estat} | "f"{aircraft}")
        listbox_vols.insert(tk.END, text)
    actualitzar_estat("Gates mostrats")


def carregar_fitxer_sortides():
    global llista_departures
    filename = filedialog.askopenfilename(title="Selecciona Departures.txt", filetypes=[("Text files", "*.txt")])
    if filename:
        llista_departures = LoadDepartures(filename)
        actualitzar_estat(f"Carregats {len(llista_departures)} vols de sortida")
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_departures)} vols de sortida.")

def fusionar_moviments_ui():
    global llista_vols, llista_arrivals, llista_departures
    if not llista_arrivals or not llista_departures:
        messagebox.showwarning("Atenció", "Cal carregar tant Arrivals com Departures primer.")
        return
    llista_vols = MergeMovements(llista_arrivals, llista_departures)
    actualitzar_llista_vols()
    actualitzar_estat("Moviments fusionats")
    messagebox.showinfo("Èxit", f"Moviments del dia fusionats. Total vols: {len(llista_vols)}")

def mostrar_grafic_ocupacio_diaria():
    from LEBL import PlotDayOccupancy
    global bcn, llista_vols
    if bcn is None or not llista_vols:
        messagebox.showwarning("Atenció", "Cal carregar l'aeroport i haver fusionat els vols del dia.")
        return
    PlotDayOccupancy(bcn, llista_vols)

from tkinter import ttk, messagebox, filedialog

COLORS = {
    "bg_main":          "#f0f4f8",
    "bg_secondary":     "#ffffff",
    "bg_card":          "#e8edf2",
    "accent_primary":   "#1d6fa4",
    "accent_secondary": "#6d28d9",
    "accent_gradient":  "#0891b2",
    "success":          "#059669",
    "warning":          "#d97706",
    "danger":           "#dc2626",
    "text_primary":     "#1e293b",
    "text_secondary":   "#475569",
    "text_muted":       "#94a3b8",
    "border":           "#cbd5e1",
    "hover":            "#1e40af",
}

def carregar_fitxer(): pass
def aplicar_schengen(): pass
def afegir_aeroport(): pass
def esborrar_aeroport(): pass
def guardar_schengen(): pass
def mostrar_grafic(): pass
def mostrar_mapa(): pass
def carregar_fitxer_vols(): pass
def carregar_fitxer_sortides(): pass
def fusionar_moviments_ui(): pass
def mostrar_grafic_vols(): pass
def mostrar_grafic_tipus_vols(): pass
def generar_mapa_trajectories(): pass
def guardar_vols_llunyans(): pass
def carregar_aeroport(): pass
def assignar_gate_ui(): pass
def mostrar_gates(): pass
def mostrar_grafic_ocupacio_diaria(): pass


class AirportManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airport Management System")
        self.root.geometry("1600x950")
        self.root.configure(bg=COLORS["bg_main"])
        self.root.minsize(1400, 800)

        self.estado_var = tk.StringVar(value="Sistema inicialitzat correctament")

        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Custom.Vertical.TScrollbar",background=COLORS["bg_card"],troughcolor=COLORS["bg_main"],arrowcolor=COLORS["accent_primary"])

    def create_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg_main"], height=100)
        header.pack(fill="x", padx=20, pady=(15, 10))
        header.pack_propagate(False)

        left_container = tk.Frame(header, bg=COLORS["bg_main"])
        left_container.pack(side="left", fill="y")

        tk.Label(left_container,text="AMS",font=("Segoe UI", 26, "bold"),bg=COLORS["bg_main"],fg=COLORS["accent_primary"]).pack(side="left", padx=(0, 15))

        title_frame = tk.Frame(left_container, bg=COLORS["bg_main"])
        title_frame.pack(side="left")

        tk.Label(title_frame,text="AIRPORT MANAGEMENT",font=("Segoe UI", 28, "bold"),bg=COLORS["bg_main"],fg=COLORS["text_primary"]).pack(anchor="w")

        tk.Label(title_frame,text="Sistema de Gestio Aeroportuaria",font=("Segoe UI", 11),bg=COLORS["bg_main"],fg=COLORS["text_secondary"]).pack(anchor="w")

    def create_main_content(self):
        main_container = tk.Frame(self.root, bg=COLORS["bg_main"])
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_sidebar(main_container)
        self.create_content_area(main_container)

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=COLORS["bg_secondary"], width=320)
        sidebar.pack(side="left", fill="y", padx=(0, 15))
        sidebar.pack_propagate(False)

        canvas = tk.Canvas(sidebar, bg=COLORS["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar, orient="vertical", command=canvas.yview)

        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_secondary"])

        window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", update_scrollregion)

        def resize_frame(event):
            canvas.itemconfig(window, width=event.width)

        canvas.bind("<Configure>", resize_frame)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_section(scroll_frame, "AEROPORTS", COLORS["accent_primary"], [
            ("Carregar Aeroports", carregar_fitxer, "Importar fitxer"),
            ("Aplicar Schengen", aplicar_schengen, "Filtrar Schengen"),
            ("Afegir Aeroport", afegir_aeroport, "Crear aeroport"),
            ("Esborrar Aeroport", esborrar_aeroport, "Eliminar aeroport"),
            ("Guardar Schengen", guardar_schengen, "Exportar"),
            ("Mostrar Grafic", mostrar_grafic, "Estadistiques"),
            ("Crear Mapa", mostrar_mapa, "Mapa KML"),])

        self.create_section(scroll_frame, "VOLS", COLORS["success"], [
            ("Carregar Arrivals", carregar_fitxer_vols, "Importar arribades"),
            ("Carregar Departures", carregar_fitxer_sortides, "Sortides"),
            ("Fusionar Moviments", fusionar_moviments_ui, "Combinar"),
            ("Grafic Aerolinies", mostrar_grafic_vols, "Stats"),
            ("Grafic Tipus Vol", mostrar_grafic_tipus_vols, "Tipus"),
            ("Mapa Trajectories", generar_mapa_trajectories, "Rutes"),
            ("Vols Llargs", guardar_vols_llunyans, "2000km+"),])

        self.create_section(scroll_frame, "GATES BCN", COLORS["warning"], [
            ("Carregar LEBL", carregar_aeroport, "Barcelona"),
            ("Assignar Gates", assignar_gate_ui, "Auto gates"),
            ("Mostrar Gates", mostrar_gates, "Estat"),
            ("Ocupacio 24h", mostrar_grafic_ocupacio_diaria, "Grafic"),])


    def create_section(self, parent, title, color, buttons):
        tk.Label(parent,text=title,font=("Segoe UI", 13, "bold"),bg=COLORS["bg_secondary"],fg=color).pack(anchor="w", padx=15, pady=(15, 5))

        for text, cmd, tip in buttons:
            self.create_button(parent, text, cmd, tip, color)

    def create_button(self, parent, text, command, tooltip, color):
        btn = tk.Label(parent,text=text,font=("Segoe UI", 10),bg=COLORS["bg_card"],fg=COLORS["text_primary"],padx=15,pady=12,anchor="w",cursor="hand2")
        btn.pack(fill="x", padx=15, pady=3)

        def on_enter(e):
            btn.configure(bg=color, fg="white")

        def on_leave(e):
            btn.configure(bg=COLORS["bg_card"], fg=COLORS["text_primary"])

        def on_click(e):
            self.update_status(f"Executant: {text}")
            self.root.after(100, command)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)

    def create_content_area(self, parent):
        content = tk.Frame(parent, bg=COLORS["bg_main"])
        content.pack(side="left", fill="both", expand=True)

        self.listbox_ap = self.create_list("AEROPORTS", content, COLORS["accent_primary"])
        self.listbox_vols = self.create_list("VOLS I GATES", content, COLORS["success"])

    def create_list(self, title, parent, color):
        frame = tk.Frame(parent, bg=COLORS["bg_secondary"])
        frame.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(frame,text=title,font=("Segoe UI", 14, "bold"),bg=COLORS["bg_secondary"],fg=color).pack(anchor="w", padx=10, pady=10)

        listbox = tk.Listbox(frame)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        listbox.insert(tk.END, "Carrega dades per començar...")
        return listbox

    def create_status_bar(self):
        bar = tk.Frame(self.root, bg=COLORS["bg_card"], height=40)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        tk.Label(bar,textvariable=self.estado_var,bg=COLORS["bg_card"],fg=COLORS["text_secondary"]).pack(side="left", padx=15)

    def update_status(self, msg):
        self.estado_var.set(msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = AirportManagementApp(root)
    root.mainloop()