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