import cv2
import time
import math
import cv2
import ms5837
import board
import busio
from adafruit_lsm9ds1 import LSM9DS1_I2C
import subprocess

# Ce code initialise et gère plusieurs capteurs :
# (MS5837) pour mesurer la profondeur et la température
# (LSM9DS1) pour récupérer les données de mouvement (accélération et rotation).
# apture flux vidéo depuis la caméra du drone  
# valeurs des capteurs en temps réel pour l'affichage.


# Initialisation du capteur de pression
pressure_sensor = ms5837.MS5837_30BA()
if not pressure_sensor.init():
    print("Erreur lors de l'initialisation du capteur de pression.")
    exit(1)

i2c = busio.I2C(board.SCL, board.SDA)
gyro_sensor = LSM9DS1_I2C(i2c)

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Impossible d'ouvrir la caméra")
    exit(1)


while True:
    ret, frame = cap.read()  # Lire une image de la caméra
    if not ret:
        print("Erreur lors de la lecture du flux vidéo")
        break

    if pressure_sensor.read():
        pressure = f"P: {pressure_sensor.pressure():.1f} mbar"
        temperature = f"T: {pressure_sensor.temperature():.2f} C"
    else:
        pressure = "P: Erreur"
        temperature = "T: Erreur"

    # Simuler les valeurs du capteur de pression
    #fake_pressure += 0.1 * math.sin(angle)  # Variation périodique
    #fake_temp += 0.01 * math.cos(angle)  # Variation plus lente
    #angle += 0.1

    # Simuler les valeurs du gyroscope
    #gyro_x = 10.0 * math.sin(angle)
    #gyro_y = 10.0 * math.cos(angle)
    #gyro_z = 5.0 * math.sin(angle / 2)

    gyro_x, gyro_y, gyro_z = gyro_sensor.gyro
    gyro_data = f"Gyro - X: {gyro_x:.2f}, Y: {gyro_y:.2f}, Z: {gyro_z:.2f}"

    # Ajouter les textes sur l'image
    cv2.putText(frame, pressure, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, temperature, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, gyro_data, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Afficher le flux vidéo avec les annotations
    cv2.imshow('Flux Video', frame)

    # Quitter si 'q' est pressé
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
