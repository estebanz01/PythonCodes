''' =======================================
	Este documento ha sido elaborado con fines educativos.
	Se distribuye bajo licencia Creative Commons 3.0, con obligatoriedad
	de mencionar a su autor (Esteban Zapata Rojas), en caso de usarse en
	cualquier tipo de desarrollo, trabajo o documento.

	Esteban Zapata Rojas.
	@estebanz01 -> Twitter.
	http://plus.google.com/+Estebanzapata -> Google plus.
	http://estebanz01.github.com -> Github.
	=======================================
'''

# Cargamos la libreria Pandas y Matplotlib
from pandas import *
import matplotlib.pyplot as plt

# Cargamos la informacion desde el archivo descargado de http://ourairports.com/data/
dataFrame = read_csv("airports.csv")

# Un contador que servira para mostrar la grafica mas adelante
j = 0

# En la data, encontramos una columna llamada Type, que tiene varios valores:
#		* Closed = Aeropuerto cerrado.
#		* Small_airport = Aeropuerto pequenho.
#		* Medium_airport = Aeropuerto medio.
#		* Large_airport = Aeropuerto grande.
#		* Seaplane_base = Pista para hidroaviones.
#		* heliport = Helipuerto.
#		* Ballonport = Base de recepcion de globos.
#
# Agrupamos por cada uno de las categorias antes mencionadas y comenzamos a recorrer el objeto.

for i, group in dataFrame.groupby(['type']):
	# No mostramos la informacion sobre aeropuertos cerrados.
	if ( i == 'closed'):
		continue
	# La funcion subplot permite dibujar varios graficos en una misma figura. Aca usamos el contador,
	# que indica la ubicacion en la matriz 2 x 3.
	plt.subplot(2,3, j)
	# Damos los valores de X (Longitud) y Y (Latitude), los pintamos de color rojo y en forma de punto
	# y colocamos el type en el label.
	group.plot(x='longitude_deg', y='latitude_deg', style='ro', label=i)
	# Colocamos la leyenda en el mejor lugar dentro del grafico.
	plt.legend(loc='best')
	# Aumentamos el contador.
	j = j+1

# Creamos una nueva figura para el World Map
plt.figure()
# Configuramos el World Map con toda la informacion de la data.
plt.plot(dataFrame['longitude_deg'], dataFrame['latitude_deg'], 'bo', label='World Map')
plt.legend(loc='best')
# Mostramos el resultado.
plt.show()
