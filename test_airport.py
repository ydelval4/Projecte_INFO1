from airport import *
#Creem un aeroport amb el codi de Barcelona i les seves coordenades
airport = Airport ("LEBL", 41.297445, 2.0832941 )
#Mirem si aquest aeroport forma part de l'espai Schengen
SetSchengen(airport)
#Mostrem per pantalla la informació de l'aeroport
PrintAirport (airport)

""" Test Pas 3
airports = LoadAirports("Airports.txt")
print(f"Aeroports carregats: {len(airports)}")
# Mostrem els 3 primers
for a in airports[:3]:
   SetSchengen(a)
   PrintAirport(a)
"""
#Aeroports desde l'arxiu Airports.txt
airports = LoadAirports("Airports.txt")
#Mostrem quants aeroports s'han carregat
print("Aeroports carregats:", len(airports))

#Posar el Schengen, recorrem tota la llista.
for a in airports:
   SetSchengen(a)

#Guardar Schengen en un arxiu
resultat = SaveSchengenAirports(airports, "schengen.txt")
if resultat == 0:
   print("Arxiu schengen.txt creat be.")
else:
   print("No es pot crear l'arxiu (llista buida).")

#Afegir aeroport
nou = Airport("KJFK", 40.6413, -73.7781)
res_add = AddAirport(airports, nou)
if res_add == 0:
   print(f"Aeroport {nou.code} ben afegit.")
else:
   print(f"Aeroport {nou.code} ja existeix.")

#Eliminar aeroport
res_remove = RemoveAirport(airports, "KJFK")
if res_remove == 0:
   print("Aeroport KJFK ben eliminat.")
else:
   print("Aeroport KJFK no trobat per eliminar.")

#Mostrar alguns resultats
for a in airports[:3]:  # els 3 primers
   PrintAirport(a)
print("\nProbar pas 5")

#Probar el gràfic
print("S'esta generant el gràfic de barres")
PlotAirports(airports)

#Probem el mapa
print("Generant l'arxiu KML per Google Earth")
res_map = MapAirports(airports, "mapa_aeroports.kml")
if res_map == 0:
    print("Arxiu mapa aeroports  ben creat, busca'l a la carpeta.")
else:
    print("Error al crear el mapa.")