import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
# Importem TOT el que vam fer al pas anterior
from airport import *

# Variable global per guardar la llista d'aeroports que es mostren a la pantalla
llista_aeroports = []


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


# --- DISSENY DE LA INTERFÍCIE (FINESTRA I BOTONS) ---
finestra = tk.Tk()
finestra.title("Gestió d'Aeroports - V1")
finestra.geometry("650x400")

# Panell per als botons (a l'esquerra)
frame_botons = tk.Frame(finestra)
frame_botons.pack(side=tk.LEFT, padx=15, pady=15, fill=tk.Y)

tk.Button(frame_botons, text="1. Carregar Aeroports", command=carregar_fitxer, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="2. Aplicar Schengen", command=aplicar_schengen, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="3. Afegir Aeroport", command=afegir_aeroport, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="4. Esborrar Aeroport", command=esborrar_aeroport, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="5. Guardar Schengen", command=guardar_schengen, width=20, bg="#e0e0e0").pack(pady=5)
tk.Button(frame_botons, text="6. Mostrar Gràfic", command=mostrar_grafic, width=20, bg="#cce5ff").pack(pady=5)
tk.Button(frame_botons, text="7. Crear Mapa (KML)", command=mostrar_mapa, width=20, bg="#d4edda").pack(pady=5)

# Panell per a la llista (a la dreta)
frame_llista = tk.Frame(finestra)
frame_llista.pack(side=tk.RIGHT, padx=15, pady=15, expand=True, fill=tk.BOTH)

tk.Label(frame_llista, text="Dades dels aeroports:", font=("Arial", 10, "bold")).pack(anchor="w")
scrollbar = tk.Scrollbar(frame_llista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Aquí és on es mostren els aeroports com a text
listbox = tk.Listbox(frame_llista, yscrollcommand=scrollbar.set, width=50, font=("Consolas", 10))
listbox.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=listbox.yview)

# Això fa que la finestra es quedi oberta esperant que facis clic
finestra.mainloop()