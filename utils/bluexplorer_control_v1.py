import cv2
import time
import math
import json
import socket
import threading
import ms5837
import board
import busio
from adafruit_lsm9ds1 import LSM9DS1_I2C
import RPi.GPIO as GPIO

### DESCRIPTION ###
# Ce code permet de piloter bluexplorer 
# en utilisant une manette et plusieurs capteurs
# Pas de gestion d'erreurs si un composant n'est pas fonctionnel

# Nous avons :
# Communication avec la manette pour recevoir les commandes de l'utilisateur
# La lecture des capteurs (pression, gyroscope)
# Intégration d'une caméra pour le flux video

# Initialisation des capteurs
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

# Configuration GPIO pour les moteurs
MOTOR_PIN = [12, 13, 18, 19]
FREQUENCY = 50
GPIO.setmode(GPIO.BCM)
for pin in MOTOR_PIN:
    GPIO.setup(pin, GPIO.OUT)

motor0 = GPIO.PWM(MOTOR_PIN[0], FREQUENCY)
motor1 = GPIO.PWM(MOTOR_PIN[1], FREQUENCY)
motor2 = GPIO.PWM(MOTOR_PIN[2], FREQUENCY)
motor3 = GPIO.PWM(MOTOR_PIN[3], FREQUENCY)

motor0.start(0)
motor1.start(0)
motor2.start(0)
motor3.start(0)

print("Démarage des moteurs")
print("Cycle de travail : 5% (arrêt)")
motor0.ChangeDutyCycle(5)  # Signal 1000 µs
motor1.ChangeDutyCycle(5)
motor2.ChangeDutyCycle(5)
motor3.ChangeDutyCycle(5)
time.sleep(2.5)

# Configuration du serveur
HOST = "0.0.0.0"
PORT = 12345
current_axes = [0, 0, 0, 0]
current_buttons = [0, 0, 0, 0]
dt_value = [5, 5, 5, 5]
freinage = 0.2
acceleration = 0.2

def start_server():
    global current_axes, current_buttons
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Serveur en écoute sur {HOST}:{PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"Connexion établie avec {client_address}")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            try:
                parsed_data = json.loads(data)
                current_axes = parsed_data.get("axes", [])
                current_buttons = parsed_data.get("buttons", [])
            except json.JSONDecodeError:
                print("Erreur : les données reçues ne sont pas un JSON valide.")
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
    finally:
        motor0.stop()
        motor1.stop()
        motor2.stop()
        motor3.stop()
        GPIO.cleanup()
        client_socket.close()
        server_socket.close()

def display_current_data():
    while True:
        print(f"moteur0 : {dt_value[0]}")
        if dt_value[0] >= 9.5:
            print("valeur max atteint")
        elif current_axes[1] < -0.5:
            dt_value[0] += acceleration

        if dt_value[0] <= 5:
            print("valeur min atteint")
        elif current_axes[1] > 0.5:
            dt_value[0] -= freinage

        motor0.ChangeDutyCycle(dt_value[0])  # Signal 1500 µs

        print(f"moteur1: {dt_value[1]}")
        if dt_value[1] >= 9.5:
            print("valeur max atteint")
        elif current_axes[1] < -0.5:
            dt_value[1] += acceleration

        if dt_value[1] <= 5:
            print("valeur min atteint")
        elif current_axes[1] > 0.5:
            dt_value[1] -= freinage

        motor1.ChangeDutyCycle(dt_value[1])  # Signal 1500 µs

        print(f"moteur2 {dt_value[2]}")
        if dt_value[2] >= 9.5:
            print("valeur max atteint")
        elif current_axes[3] < -0.5:
            dt_value[2] += acceleration

        if dt_value[2] <= 5:
            print("valeur min atteint")
        elif current_axes[3] > 0.5:
            dt_value[2] -= freinage

        motor2.ChangeDutyCycle(dt_value[2])  # Signal 1500 µs

        print(f"moteur3 {dt_value[3]}")
        if dt_value[3] >= 9.5:
            print("valeur max atteint")
        elif current_axes[3] < -0.5:
            dt_value[3] += acceleration

        if dt_value[3] <= 5:
            print("valeur min atteint")
        elif current_axes[3] > 0.5:
            dt_value[3] -= freinage

        motor3.ChangeDutyCycle(dt_value[3])  # Signal 1500 µs

        time.sleep(0.2)

def display_video_and_sensors():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la lecture du flux vidéo")
            break

        if pressure_sensor.read():
            pressure = f"P: {pressure_sensor.pressure():.1f} mbar"
            temperature = f"T: {pressure_sensor.temperature():.2f} C"
        else:
            pressure = "P: Erreur"
            temperature = "T: Erreur"

        gyro_x, gyro_y, gyro_z = gyro_sensor.gyro
        gyro_data = f"Gyro - X: {gyro_x:.2f}, Y: {gyro_y:.2f}, Z: {gyro_z:.2f}"

        cv2.putText(frame, pressure, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, temperature, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, gyro_data, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Flux Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    display_thread = threading.Thread(target=display_current_data, daemon=True)
    display_thread.start()

    display_video_and_sensors()
