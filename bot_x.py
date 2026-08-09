import datetime as dt
import tweepy
from dotenv import load_dotenv
from os import getenv
load_dotenv()

MODE_SIMULATION = getenv("MODE_SIMULATION", "true").lower() == "true"


def creer_client_x():
    api_key = getenv("X_API_KEY")
    api_secret = getenv("X_API_SECRET")
    access_token = getenv("X_ACCESS_TOKEN")
    access_token_secret = getenv("X_ACCESS_TOKEN_SECRET")

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret)

mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

def creer_message():
    maintenant = dt.datetime.now()
    mois_fr = mois[maintenant.month - 1]
    date_formatee = f"{maintenant.day} {mois_fr} {maintenant.year}"
    message = f"Nous vous rappelons qu’en ce {date_formatee}, vous pouvez toujours sortir de la Matrice. Ouvrez vos esprits, ouvrez les yeux. Vous pouvez toujours cesser d’être leur produit."
    return message

def verifier_message(texte):
    limite_x = 280
    return len(texte) <= limite_x

def publier_sur_x(client, texte, simulation):
    if simulation:
        print(f"[SIMULATION] {texte}")
    else:
        try:
            reponse = client.create_tweet(text=texte)
            print("Publication réussie")
        except tweepy.TweepyException as erreur:
            print(f"Échec de la publication : {erreur}")

def main():
    client = creer_client_x()
    message = creer_message()
    if verifier_message(message):
        publier_sur_x(client, message, MODE_SIMULATION)
    else:
        print("Message trop long")

if __name__ == "__main__":
    main()
