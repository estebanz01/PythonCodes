''' =======================================
    Este documento ha sido elaborado con fines educativos.
    Se distribuye bajo licencia Creative Commons 3.0, con obligatoriedad
    de mencionar a su autor (Esteban Zapata Rojas), en caso de usarse en
    cualquier tipo de desarrollo, trabajo o documento.

    Esteban Zapata Rojas.
    @estebanz01 -> Twitter.
    http://plus.google.com/+Estebanzapata -> Google plus.
    http://github.com/estebanz01 -> Github.
    =======================================
'''

# Cargamos las librerías necesarias para capturar la información
# del Streaming de Twitter y almacenarla en MongoDB.
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
from tweepy.utils import import_simplejson

# Nos conectamos al servidor local, selecionamos la BD Tweets y
# Comenzamos a trabajar sobre la colección tuits.
client = MongoClient('localhost', 27017)
db = client.tweets
tweets = db.tuits
# Cargamos el complemento JSON para guardar la información en formato correcto.
json = import_simplejson()

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = COSTUMER_KEY
consumer_secret = COSTUMER_SECRET_KEY

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_SECRET_TOKEN

# Creamos una clase que se encargará de administrar el Streaming de Twitter.
class StdOutListener(StreamListener):
    
    # El método on_data, que recibe dos parámetros, Ingresará la información
    # del Streaming de Twitter a la colección tuits de nuestra BD en MongoDB.
    def on_data(self, data):

        tweet = json.loads(data) # Convertimos el tuit a formato JSON.
        '''
            Acá comienza lo interesante:
                Como vamos a cargar los tuits en el mapa, necesitamos
                validar que la información que nos llegue esté geolocalizado.
                Lastimosamente, hasta éste momento sólo se posee 1 % del total
                de tuits geolocalizado y es por ésto que debemos aplicar los filtros
                necesarios.
        '''
        # Si el tweet que convertimos a JSON posee el campo coordinates, proseguimos.
        if "coordinates" in tweet.keys():
            if tweet["coordinates"] != None: # Si hay información en el campo, procedemos a la inserción.
                tweets.insert({
                    "id" : tweet["id"], # Insertará en una columna el id del tuit, de acuerdo a las políticas de Twitter.
                    "id_str" : tweet["id_str"], # El mismo elemento que el anterior, en formato cadena de texto.
                    "datetime" : tweet["created_at"], # Fecha de creación del tuit.
                    "coordinates" : tweet["coordinates"]["coordinates"], # Latitude y Longitud del tuit.
                    "user" : tweet["user"]["screen_name"], # Nombre de usuario - el arroba en twitter.
                    "name" : tweet["user"]["name"], # Cómo aparece el nombre en Twitter.
                    "text" : tweet["text"], # El tuit que se publicó, que lo utlizaremos más adelante.
                    "source": tweet["source"] # Desde qué tipo de dispositivo o aplicación se publicó.
                    })
                print "After insert" # Debugging purposes
        return True # Devolvemos True para que continúe leyendo la información obtenida.

    # En caso de que haya algún error al leer la data, imprimirá el error y devolverá True, para seguir intentando.
    def on_error(self, status):
        print status
        return True

    # En caso de que se acabe el tiempo de espera, devolverá True y hará que reinicie el proceso.
    def on_timeout(self):
        return True # Don't kill the stream

# Comenzamos la ejecución del programa
if __name__ == '__main__':
    l = StdOutListener() # Instanciamos la clase creada anteriormente.
    auth = OAuthHandler(consumer_key, consumer_secret) # Cargamos las llaves de autenticación
    auth.set_access_token(access_token, access_token_secret) # Establecemos conexión.

    stream = Stream(auth, l) # Comenzamos a escuchar el streaming de Twitter y mandamos la info a la clase instanciada.
    stream.filter(track=['eclipse']) # Filtramos la información del streaming con la palabra clave "Eclipse".