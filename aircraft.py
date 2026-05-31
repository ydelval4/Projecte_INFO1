import matplotlib.pyplot as plt
from airport import *

class Aircraft:
    def __init__(self, id='-', airline='-', origin='-', time='00:00', destination='-',
                 departuretime='00:00'):
        self.id = id  # Matrícula de l'avió (string)
        self.airline = airline  # Codi ICAO de la companyia (3 caràcters)
        self.origin = origin  # Codi ICAO de l'aeroport d'origen (4 caràcters)
        self.time = time  # Hora d'aterratge en format hh:mm (string)
        self.destination = destination #Quin serà el destí final
        self.departuretime = departuretime #Hora de sortida

def is_valid_time(time_str):
    """Comprova que un string té format hh:mm vàlid."""
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

    return aircrafts  # ◄ CORREGIT: Només retorna la llista


def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 and len(departures) == 0:
        return []

    result = []
    used_departures = []

    for arr in arrivals:
        merged = arr  # Empecemos con el avión de llegada
        for dep in departures:
            if dep in used_departures:
                continue
            if arr.id == dep.id:
                if TimeToMinutes(arr.time) < TimeToMinutes(dep.departuretime):
                    merged.destination = dep.destination
                    merged.departuretime = dep.departuretime
                    used_departures.append(dep)
                    break
        result.append(merged)

    # Añadir vuelos que solo tienen salida (aviones nocturnos)
    for dep in departures:
        if dep not in used_departures:
            result.append(dep)

    return result  # ◄ CORREGIT: Només retorna la llista


def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return []
    result = []
    for ac in aircrafts:
        if ac.origin == '-' or ac.origin == "":
            result.append(ac)
    return result  # ◄ CORREGIT: Només retorna la llista


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

def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: no hi ha dades")
        return -1

    airports_list = LoadAirports("Airports.txt")
    airports_dict = {}
    for a in airports_list:
        airports_dict[a.code] = a

    LEBL_LAT = 41.2974
    LEBL_LON = 2.0833
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
"""
    for ac in aircrafts:
        if ac.origin in airports_dict:
            origen = airports_dict[ac.origin]
            if IsSchengenAirport(ac.origin):
                color = "ff00ff00"  # verd
            else:
                color = "ff0000ff"  # vermell

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


def HaversineDistance(lat1, lon1, lat2, lon2):
    R = 6371  # Radi de la Terra en km
    a = math.radians(lat1)
    b = math.radians(lon1)
    c = math.radians(lat2)
    d = math.radians(lon2)
    m = 2 * R * math.asin(
        (math.sin((a - c) * 0.5) ** 2 + math.cos(a) * math.cos(c) * (math.sin((b - d) * 0.5) ** 2)) ** 0.5)
    return m


def LongDistanceArrivals(aircrafts, airports_list):
    # ◄ MODIFICAT: Ara rep els aeroports com a paràmetre obligatori per a la v4
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
            if distancia > 2000:
                llista_llunyans.append(ac)

    return llista_llunyans