from airport import *
airport = Airport ("LEBL", 41.297445, 2.0832941 )
SetSchengen(airport)
PrintAirport (airport)
""" Test Pas 3
airports = LoadAirports("Airports.txt")
print(f"Aeroports carregats: {len(airports)}")
# Mostrem els 3 primers
for a in airports[:3]:
   SetSchengen(a)
   PrintAirport(a)
"""
# Aeroports desde l'arxiu
airports = LoadAirports("Airports.txt")
print("Aeroports carregats:", len(airports))


# Posar el Schengen
for a in airports:
   SetSchengen(a)


# Guardar Schengen en un arxiu
resultat = SaveSchengenAirports(airports, "schengen.txt")
if resultat == 0:
   print("Arxiu schengen.txt creat be.")
else:
   print("No es pot crear l'arxiu (llista buida).")


# Afegir aeroport
nou = Airport("KJFK", 40.6413, -73.7781)
res_add = AddAirport(airports, nou)
if res_add == 0:
   print(f"Aeroport {nou.code} ben afegit.")
else:
   print(f"Aeroport {nou.code} ja existeix.")


# Eliminar aeroport
res_remove = RemoveAirport(airports, "KJFK")
if res_remove == 0:
   print("Aeroport KJFK ben eliminat.")
else:
   print("Aeroport KJFK no trobat per eliminar.")


# Mostrar alguns resultats
for a in airports[:3]:  # els 3 primers
   PrintAirport(a)

print("\n--- PROBANDO EL PASO 5 ---")

# 1. Probamos el gráfico
print("Generando gráfico de barras...")
PlotAirports(airports)

# 2. Probamos el mapa
print("Generando archivo KML para Google Earth...")
res_map = MapAirports(airports, "mapa_aeropuertos.kml")
if res_map == 0:
    print("¡El archivo 'mapa_aeropuertos.kml' se ha creado bien! Búscalo en tu carpeta.")
else:
    print("Hubo un error creando el mapa.")