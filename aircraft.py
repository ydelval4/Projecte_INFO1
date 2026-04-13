class Aircraft:
    def __init__(self, id='-', airline='-', origin='-', time='00:00'):
        self.id = id  # Matrícula de l'avió (string)
        self.airline = airline  # Codi ICAO de la companyia (3 caràcters)
        self.origin = origin  # Codi ICAO de l'aeroport d'origen (4 caràcters)
        self.time = time  # Hora d'aterratge en format hh:mm (string)

def is_valid_time(time_str):
    """Comprova que un string té format hh:mm vàlid."""
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return False
        h, m = int(parts[0]), int(parts[1])
        return 0 <= h <= 23 and 0 <= m <= 59
    except:
        return False


def LoadArrivals(filename):
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
        id_avio = parts[0]
        origin = parts[1]
        time_str = parts[2]
        airline = parts[3]

        if not is_valid_time(time_str):
            continue

        ac = Aircraft(id_avio, airline, origin, time_str)
        aircrafts.append(ac)

    return aircrafts


def SaveFlights(aircrafts, filename):

    if len(aircrafts) == 0:
        return -1

    try:
        with open(filename, 'w') as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            for ac in aircrafts:
                id_val = ac.id if ac.id != '' else '-'
                origin_val = ac.origin if ac.origin != '' else '-'
                time_val = ac.time if ac.time != '' else '0'
                airline_val = ac.airline if ac.airline != '' else '-'
                f.write(f"{id_val} {origin_val} {time_val} {airline_val}\n")
        return 0
    except Exception as e:
        print(f"Error guardant el fitxer: {e}")
        return -1

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: no hi ha dades")
        return

    contador = {}
#Començo sense res i vaig guardant coses. Dins de contador.
    for ac in aircrafts:
        if ac.airline in contador:
            contador[ac.airline] += 1
        else:
            contador[ac.airline] = 1
#Per a cada avió:Si ja l'he vit en l'aerolínia cumo 1, si és la primera vegada començo a 1.

    airlines = list(contador.keys())
    values = list(contador.values())
#Noms que ja venen donats per Pyton. Pel contador que fa com un  diccionari.
    plt.figure()
    plt.bar(airlines, values)
    plt.title("Vols per aerolínia")
    plt.xlabel("Aerolínia")
    plt.ylabel("Número de vols")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error, no hi ha dades")
        return

    schengen = 0
    no_schengen = 00

    for ac in aircrafts:
        if ac.origin in airports_data:
            country = airports_data[ac.origin][0]

            if country in schengen_countries:
                schengen += 1
            else:
                no_schengen += 1
#Es recorre la llista de vols, s'obté el país de l'aeroport d'origen i es classifica com a Schengen o no Schengen, mentre s'acumula el número de vols.
    plt.figure()
    plt.bar(["Flights"], [schengen], label="Schengen")
    plt.bar(["Flights"], [no_schengen], bottom=[schengen], label="No Schenegen")
    plt.title("Flights Type")
    plt.ylabel("Number of Flights")
    plt.legend()
    plt.show()

def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: no hi ha dades")
        return

    LEBL_LAT = 41.2974
    LEBL_LON = 2.0833
#Tots els vols al mteix aeroport, el de Barcelona.
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
"""

    for ac in aircrafts:
        if ac.origin not in airports_data:
            continue

        country, lat, lon = airports_data[ac.origin]

        if country in schengen_countries:
            color = "ff00ff00"  # verde
        else:
            color = "ff0000ff"  # rojo

        kml += f""" #Es un texto multilínea con variables dentro, PREGUNTAR PROFE
<Placemark>
    <Style>
        <LineStyle>
            <color>{color}</color>
            <width>2</width>
        </LineStyle>
    </Style>
    <LineString>
        <coordinates>
            {lon},{lat},0
            {LEBL_LON},{LEBL_LAT},0
        </coordinates>
    </LineString>
</Placemark>
"""
#Dibuixar al mapa amb el colo que toqui i el estil denfinit.
    kml += "</Document></kml>"
    with open("flights.kml", "w") as f:
        f.write(kml)
#Crear el fitxer que obrirem a Google Earth.
    print("KML generat correctament")


import math

def HaversineDistance(lat1, lon1, lat2, lon2):

    R = 6371  #Radi de la Terra en km

    a = math.radians(lat1)
    b = math.radians(lon1)
    c = math.radians(lat2)
    d = math.radians(lon2)

    m = 2 * R * math.asin(
        (math.sin((a - c) * 0.5) ** 2 + math.cos(a) * math.cos(c) * (math.sin((b - d) * 0.5) ** 2)) ** 0.5)

    return m


def LongDistanceArrivals(aircrafts):
    llista_llunyans = []

    # Coordenades de l'aeroport de Barcelona
    LEBL_LAT = 41.2974
    LEBL_LON = 2.0833

    for ac in aircrafts:
        # Comprovem si tenim les dades de l'aeroport d'origen
        if ac.origin in airports_data:

            pais, lat_origen, lon_origen = airports_data[ac.origin]

            # Calculem la distància fins a Barcelona
            distancia = HaversineDistance(lat_origen, lon_origen, LEBL_LAT, LEBL_LON)

            # Si és superior a 2000 km, l'afegim a la llista
            if distancia > 2000:
                llista_llunyans.append(ac)

    return llista_llunyans