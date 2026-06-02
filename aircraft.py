import matplotlib.pyplot as plt
#Importem totes les funcions i classes del fitxer airport.py
from airport import *

#Aquesta classe serveix per guardar la informació d'un avió
class Aircraft:
    def __init__(self, id='-', airline='-', origin='-', time='00:00', destination='-',
                 departuretime='00:00'):
        self.id = id  #Matrícula de l'avió (string)
        self.airline = airline  #Codi ICAO de la companyia (3 caràcters)
        self.origin = origin  #Codi ICAO de l'aeroport d'origen (4 caràcters)
        self.time = time  #Hora d'aterratge en format hh:mm (string)
        self.destination = destination #Quin serà el destí final
        self.departuretime = departuretime #Hora de sortida


def is_valid_time(time_str):
#Comprova si una hora té el format vàlid (hh:mm)
    if not time_str or time_str == '-':
        return False
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return False
        h, m = int(parts[0]), int(parts[1])
        return 0 <= h <= 23 and 0 <= m <= 59
    except:
        return False


def TimeToMinutes(time_str):
    if not time_str or time_str == '-':
        return 0
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


#Carrega els vols d'arribada des d'un fitxer
def LoadArrivals(filename):
    aircrafts = []
    try:
        f = open(filename, 'r')
    except:
        print(f"Error: no s'ha trobat el fitxer '{filename}'")
        return aircrafts
    lines = f.readlines()
    f.close()
#Comencem a la línia 1 perquè la primera sol ser el títol
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        id_avio = parts[0]
        origin = parts[1]
        time_str = parts[2]
        airline = parts[3]
        if not is_valid_time(time_str):
            continue
        ac = Aircraft(id_avio, airline, origin, time_str)
        aircrafts.append(ac)
    return aircrafts

#Carrega els vols de sortida des d'un fitxer# Carrega els vols de sortida des d'un fitxer
def LoadDepartures(filename):
    aircrafts = []
    try:
        f = open(filename, 'r')
    except:
        print(f"Error: no s'ha trobat el fitxer '{filename}'")
        return aircrafts
    lines = f.readlines()
    f.close()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        aircraft_id = parts[0]
        destination = parts[1]
        departuretime = parts[2]
        airline = parts[3]
        if not is_valid_time(departuretime):
            continue
        ac = Aircraft()
        ac.id = aircraft_id
        ac.destination = destination
        ac.departuretime = departuretime
        ac.airline = airline

        aircrafts.append(ac)
    return aircrafts

#Uneix les arribades amb les sortides del mateix avió
def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 and len(departures) == 0:
        return []
    result = []
#Guardarà les sortides que ja hem utilitzat
    used_departures = []
    for arr in arrivals:
        #Comencem amb les dades de l'arribada
        merged = arr
        for dep in departures:
            if dep in used_departures:
                continue
            if arr.id == dep.id:
                if TimeToMinutes(arr.time) < TimeToMinutes(dep.departuretime):
                    #Afegim les dades de la sortida
                    merged.destination = dep.destination
                    merged.departuretime = dep.departuretime
                    used_departures.append(dep)
                    break
        result.append(merged)

    #Afegim avions que només tenen sortida
    for dep in departures:
        if dep not in used_departures:
            result.append(dep)

    return result  # ◄ CORREGIT: Només retorna la llista


#Retorna els avions que han passat la nit a l'aeroport
def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return []
    result = []
    for ac in aircrafts:
        #Si no tenen aeroport d'origen
        if ac.origin == '-' or ac.origin == "":
            result.append(ac)
    return result  # ◄ CORREGIT: Només retorna la llista


#Guarda els vols en un fitxer de text
def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        return -1
    try:
        with open(filename, 'w') as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            for ac in aircrafts:
                #Si algun camp està buit posem un valor per defecte
                id_val = ac.id if ac.id != '' else '-'
                origin_val = ac.origin if ac.origin != '' else '-'
                time_val = ac.time if ac.time != '' else '0'
                airline_val = ac.airline if ac.airline != '' else '-'
                f.write(f"{id_val} {origin_val} {time_val} {airline_val}\n")
        return 0
    except Exception as e:
        print(f"Error guardant el fitxer: {e}")
        return -1


#Fa un gràfic amb el nombre de vols de cada companyia
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: no hi ha dades")
        return

    contador = {}
    #Comptem quants vols té cada companyia
    for ac in aircrafts:
        if ac.airline in contador:
            contador[ac.airline] += 1
        else:
            contador[ac.airline] = 1

    airlines = list(contador.keys())
    values = list(contador.values())
    plt.figure()
    plt.bar(airlines, values)
    plt.title("Vols per aerolínia")
    plt.xlabel("Aerolínia")
    plt.ylabel("Número de vols")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


#Fa un gràfic diferenciant vols Schengen i No Schengen
def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error, no hi ha dades")
        return

    schengen = 0
    no_schengen = 0

    for ac in aircrafts:
        if IsSchengenAirport(ac.origin):
            schengen += 1
        else:
            no_schengen += 1

    plt.figure()
    plt.bar(["Flights"], [schengen], label="Schengen")
    plt.bar(["Flights"], [no_schengen], bottom=[schengen], label="No Schengen")
    plt.title("Flights Type")
    plt.ylabel("Number of Flights")
    plt.legend()
    plt.show()


#Crea un fitxer KML per veure les rutes al Google Earth
def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: no hi ha dades")
        return -1
    #Carreguem els aeroports
    airports_list = LoadAirports("Airports.txt")
    airports_dict = {}
    #Creem un diccionari per buscar aeroports més ràpidament
    for a in airports_list:
        airports_dict[a.code] = a
    #Coordenades aeroport Barcelona
    LEBL_LAT = 41.2974
    LEBL_LON = 2.0833


    #Inici del fitxer KML
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
"""
    for ac in aircrafts:
        if ac.origin in airports_dict:
            origen = airports_dict[ac.origin]
            if IsSchengenAirport(ac.origin):
                color = "ff00ff00"  # verd Schengen
            else:
                color = "ff0000ff"  # vermell No Schengen

            #Dibuixa una línia entre l'origen i Barcelona
            kml += f"""<Placemark>
    <Style>
        <LineStyle>
            <color>{color}</color>
            <width>2</width>
        </LineStyle>
    </Style>
    <LineString>
        <coordinates>
            {origen.lon},{origen.lat},0
            {LEBL_LON},{LEBL_LAT},0
        </coordinates>
    </LineString>
</Placemark>
"""
    kml += "</Document></kml>"
    with open("flights.kml", "w") as f:
        f.write(kml)
    print("KML generat correctament")


#Calcula la distància entre dos punts de la Terra
def HaversineDistance(lat1, lon1, lat2, lon2):
    R = 6371  # Radi de la Terra en km
    a = math.radians(lat1)
    b = math.radians(lon1)
    c = math.radians(lat2)
    d = math.radians(lon2)
    m = 2 * R * math.asin(
        (math.sin((a - c) * 0.5) ** 2 + math.cos(a) * math.cos(c) * (math.sin((b - d) * 0.5) ** 2)) ** 0.5)
    return m


#Torna els avions que venen de més de 2000 km
def LongDistanceArrivals(aircrafts, airports_list):
    llista_llunyans = []
    LEBL_LAT = 41.2974
    LEBL_LON = 2.0833
    airports_dict = {}
    for a in airports_list:
        airports_dict[a.code] = a
    for ac in aircrafts:
        if ac.origin in airports_dict:
            origen = airports_dict[ac.origin]
            distancia = HaversineDistance(origen.lat, origen.lon, LEBL_LAT, LEBL_LON)
            #Si supera els 2000 km l'afegim a la llista
            if distancia > 2000:
                llista_llunyans.append(ac)

    return llista_llunyans


def PlotArrivalsByHour(aircrafts):
    # Inicialitzem un comptador amb 24 posicions (una per a cada hora del dia)
    arribades_per_hora = [0] * 24

    for ac in aircrafts:
        if ac.time and ac.time != '-':
            try:
                # Extraiem l'hora abans dels dos punts (ex: "14:25" -> 14)
                hora = int(ac.time.split(':')[0])
                if 0 <= hora <= 23:
                    arribades_per_hora[hora] += 1
            except:
                continue  # Si hi ha un error de format, passem al següent

    # Creem la visualització amb Matplotlib
    plt.figure(figsize=(10, 5))
    hores = list(range(24))

    # Dibuixem les barres
    plt.bar(hores, arribades_per_hora, color='#1d6fa4', edgecolor='black', alpha=0.8)

    # Configuració de la gràfica
    plt.title("Trànsit de Llegades per Franja Horària", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Hora del dia", fontsize=11)
    plt.ylabel("Número de arribades", fontsize=11)

    # Forcem que mostri totes les hores a l'eix X
    plt.xticks(hores, [f"{h:02d}:00" for h in hores], rotation=45, fontsize=9)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()