import matplotlib.pyplot as plt
#Pas 1


# Codis ICAO dels paisos de l'espai Schengen
SCHENGEN_PREFIXES = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
   'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']


class Airport :
   def __init__(self, code, lat, lon):
       self.code = code
       self.lat = lat
       self.lon = lon
       self.schengen = False


def IsSchengenAirport(code):
   if code[:2] in SCHENGEN_PREFIXES : #el code[:2] selecciona només els 2 primers caracters del codi ICAO
       return True
   return False


def SetSchengen(airport):
   airport.schengen = IsSchengenAirport(airport.code)


def PrintAirport(airport):
   print(f"Codi ICAO : {airport.code}")
   print(f"Latitud : {airport.lat}")
   print(f"Longitud : {airport.lon}")
   print(f"Schengen : {airport.schengen}")




#direcció es refereix a N,S,E o W
def convert_coord(coord):
    direcció = coord[0]
    resta = coord[1:]  # tot sense la lletra inicial
    if len(resta) == 6:   # latitud: GGMMSS (2 dígits de graus)
        graus = int(resta[0:2])
        minuts = int(resta[2:4])
        segons = int(resta[4:6])
    else:                 # longitud: GGGMMSS (3 dígits de graus)
        graus = int(resta[0:3])
        minuts = int(resta[3:5])
        segons = int(resta[5:7])
    decimal = graus + minuts/60 + segons/3600
    if direcció in ['S', 'W']:
        decimal = -decimal
    return decimal
#Amb el if traiem les direccions negatives


def LoadAirports(filename):
   ap = []
   try:
       F = open(filename, 'r')
   except:
       return ap


   lines = F.readlines()
   F.close()


   """
   F = open(filename, 'r')
   lines = F.readlines()
   if filename not found :
       print(f"No s'ha trobat el fitxer {filename}")
       return ap
   """


   for line in lines[1:]:
       line = line.strip()
       parts = line.split()
       code = parts[0]
       """
       S'han de passar a graus decimals. fet
       """
       lat = convert_coord(parts[1])
       lon = convert_coord(parts[2])
       airport = Airport(code, lat, lon)
       ap.append(airport)
   return ap


def SaveSchengenAirports(airports, filename):
   if len(airports) == 0:
       return -1


   file = open(filename, "w")
   file.write("CODI LAT LON\n")


   for airport in airports:
       if airport.schengen:
           file.write(f"{airport.code} {airport.lat} {airport.lon}\n")


   file.close()
   return 0




def AddAirport(airports, airport):
   for a in airports:
       if a.code == airport.code:
           return -1


   airports.append(airport)
   return 0




def RemoveAirport(airports, code):
   for a in airports:
       if a.code == code:
           airports.remove(a)
           return 0


   return -1


def PlotAirports(airports):
    # Contamos cuántos aeropuertos son Schengen y cuántos no
    schengen_count = sum(1 for a in airports if a.schengen)
    non_schengen_count = len(airports) - schengen_count

    # Creamos el gráfico de barras apiladas
    fig, ax = plt.subplots()
    ax.bar(['Aeroports'], [schengen_count], label='Schengen', color='blue')
    ax.bar(['Aeroports'], [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='red')

    ax.set_ylabel('Quantitat')
    ax.set_title('Aeroports Schengen vs No Schengen')
    ax.legend()
    plt.show()


def MapAirports(airports, filename="mapa_aeropuertos.kml"):
    # Estructura básica de un archivo KML para Google Earth
    kml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Style id="schengen_style">
    <IconStyle>
      <Icon><href>http://maps.google.com/mapfiles/ms/icons/blue-dot.png</href></Icon>
    </IconStyle>
  </Style>
  <Style id="no_schengen_style">
    <IconStyle>
      <Icon><href>http://maps.google.com/mapfiles/ms/icons/red-dot.png</href></Icon>
    </IconStyle>
  </Style>
'''
    kml_footer = '''</Document>
</kml>'''

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(kml_header)
            for a in airports:
                # Asignamos color azul si es Schengen, rojo si no lo es
                estil = "#schengen_style" if a.schengen else "#no_schengen_style"
                f.write('  <Placemark>\n')
                f.write(f'    <name>{a.code}</name>\n')
                f.write(f'    <styleUrl>{estil}</styleUrl>\n')
                f.write('    <Point>\n')
                # Google Earth lee primero la longitud y luego la latitud
                f.write(f'      <coordinates>{a.lon},{a.lat},0</coordinates>\n')
                f.write('    </Point>\n')
                f.write('  </Placemark>\n')
            f.write(kml_footer)
        return 0
    except Exception as e:
        print(f"Error generando el mapa KML: {e}")
        return -1