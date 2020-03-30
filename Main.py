#Importar consumer API de Twitter https://github.com/tweepy/tweepy
import tweepy
#importar las credenciales de Twitter de un script
import twkeys
# import libraries to handle data
import pandas as pd
from time import sleep
from datetime import datetime

#Credenciales del Twitter API que están el el script twkeys.py
consumer_key = twkeys.consumer_key()
consumer_secret = twkeys.consumer_secret()
access_key = twkeys.access_key()
access_secret = twkeys.access_secret()


def get_all_tweets(screen_name):
    #Este método solo tiene permitido descargar máximo los ultimos 3240 tweets del usuario
    #Especificar aquí durante las pruebas un número entre 200 y 3240
    limit_number =  100

    #autorizar twitter, inicializar tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #inicializar una list to para almacenar los Tweets descargados por tweepy
    alltweets = []

    #Hacer una petición inicial por los 200 tweets más recientes (200 es el número máximo permitido)
    new_tweets = api.user_timeline(tweet_mode = 'extended', screen_name = screen_name,count=50)

    #guardar los tweets más recientes
    alltweets.extend(new_tweets)

    #guardar el ID del tweet más antiguo menos 1
    oldest = alltweets[-1].id - 1

    #recorrer todos los tweets en la cola hasta que no queden más
    while len(new_tweets) > 0 and len(alltweets) <= limit_number:
        print ("getting tweets before" + str(oldest))

        #en todas las peticiones siguientes usar el parámetro max_id para evitar duplicados
        new_tweets = api.user_timeline(screen_name = screen_name,count=50,max_id=oldest, tweet_mode = 'extended')

        #guardar los tweets descargados
        alltweets.extend(new_tweets)

        #actualizar el ID del tweet más antiguo menos 1
        oldest = alltweets[-1].id - 1

        #informar en la consola como vamos
        print (str(len(alltweets)) + " tweets descargados hasta el momento")

    return alltweets

# filters
def ignore_retweets(tweet):
    if not tweet.text.startswith("RT"):
        return tweet


def word_of_the_day(tweet):
    if tweet.text.startswith("Word of the day"):
        return tweet

def filter_tweets(allteewts):
    filteredteets= []
    # Pass custom filters here
    filters = [
        ignore_retweets,
        word_of_the_day,
    ]
    for tweet in allteewts:
        if not (tweet.full_text.startswith("Word of the day") or tweet.full_text.startswith("RT")):
            filteredteets.append(tweet)
        #else:
            #print(tweet.text)
    return filteredteets

# Function to filter the tweets
def filter_tweet(tweet, filters):
    for f in filters:
        tweet = f(tweet)
        if tweet is None:
            return
    return tweet


if __name__ == '__main__':
    #especificar el nombre de usuario de la cuenta a la cual se descargarán los tweets
    tweets = get_all_tweets("UdeA")
    tweets  = filter_tweets(tweets)
    # Mostrarlista
    print(len(tweets))

    # transform the tweepy tweets into a 2D array that will
    # populate the csv
    outtweets = [[tweet.id_str,
                  tweet.created_at,
                  tweet.full_text,
                  tweet.favorite_count,
                  tweet.retweet_count] for tweet in tweets]

    df = pd.DataFrame.from_records(outtweets, columns =['id', 'created_at', 'text', 'fovourited', 'retweeted'])
    print(df )