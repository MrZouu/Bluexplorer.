import pygame
import socket
import json
import time

# Initialisation de Pygame
pygame.init()

# Configuration du client
SERVER_IP = "192.168.2.2"  # Remplacez par l'adresse IP de votre serveur
SERVER_PORT = 12345        # Port du serveur

# Vérifier si une manette est connectée
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Aucune manette connectée.")
    pygame.quit()
    exit()

# Initialiser la manette
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Manette connectée : {joystick.get_name()}")

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connecté au serveur {SERVER_IP}:{SERVER_PORT}")

# Boucle principale
try:
    while True:
        # Mettre à jour les événements Pygame
        pygame.event.pump()

        # Récupérer les données de la manette
        data = {
            "axes": [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())],
            "buttons": [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        }

        # Envoyer les données au serveur
        client_socket.send(json.dumps(data).encode())

        # Ajouter un délai pour limiter la fréquence d'envoi
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Arrêt du client.")
finally:
    client_socket.close()
    pygame.quit()
