#!/usr/bin/python3
#coding: utf-8

"""
@author : tiansemi@outlook.com

Télécharger le fichier http://challenge01.root-me.org/steganographie/ch1/ch1.png et placer le
dans le même dossier que ce script python
"""
import subprocess

result=''
cmd = 'exiftool ch1.png|grep "GPS Position"|cut -d: -f2'
result = subprocess.check_output(cmd, shell=True)
result = result.decode('utf-8').strip().split(',')
if result=='':
	print('Vous devez Install exiftool. \nSinon vérifier si le fichier ch1.png se trouve dans le même dossier que ce script.')
	exit()
# Définir les coordonnées GPS
latitude = result[0]
longitude = result[1]
# Supprimer les caractères non numériques
latitude = latitude.replace("deg", "").replace("'", "").replace("\"", "").replace("N", "").replace("S", "").split()
longitude = longitude.replace("deg", "").replace("'", "").replace("\"", "").replace("E", "").replace("W", "").split()

# Convertir en format décimal
decimal_latitude = sum(float(x) / 60 ** n for n, x in enumerate(latitude))
decimal_longitude = sum(float(x) / 60 ** n for n, x in enumerate(longitude))
print("Latitude en format décimal :", decimal_latitude)
print("Longitude en format décimal :", decimal_longitude)

from geopy.geocoders import Nominatim

# Créer un géocodeur
geolocator = Nominatim(user_agent="ch1RootMeStego")
# Obtenir l'emplacement
location = geolocator.reverse([decimal_latitude, decimal_longitude])

# Afficher l'emplacement
# print(location.address)

# Afficher la ville
city = location.raw['address']['city']
print("Ville :", city)
