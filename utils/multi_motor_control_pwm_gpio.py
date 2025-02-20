import RPi.GPIO as GPIO
import time

### DESCRIPTION ###
# Contrôle plusieurs moteurs simultanément en utilisant un dictionnaire pour gérer plusieurs broches PWM
# deux niveaux de puissance (5% à 6%)

# Liste des broches GPIO compatibles avec PWM (par exemple sur Raspberry Pi 4 : GPIO 12, 13, 18, 19)
PWM_PINS = [12, 13, 18, 19]
FREQUENCY = 50  # Fréquence typique pour un ESC : 50 Hz

# Initialisation des broches GPIO
GPIO.setmode(GPIO.BCM)
for pin in PWM_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Création des instances PWM pour chaque broche
motors = {pin: GPIO.PWM(pin, FREQUENCY) for pin in PWM_PINS}

try:
    # Démarrage des signaux PWM avec un cycle de travail initial de 0%
    for motor in motors.values():
        motor.start(0)

    print("Envoi de signaux PWM sur toutes les broches. Appuyez sur Ctrl+C pour arrêter.")

    # Tester différentes valeurs du cycle de travail
    time.sleep(3)


    print("Cycle de travail : 5% (arrêt)")
    for motor in motors.values():
        motor.ChangeDutyCycle(5)  # Signal 1000 µs
    time.sleep(3)
    while True:
        print("Cycle de travail : 10% (vitesse maximale)")
        for motor in motors.values():
            motor.ChangeDutyCycle(6)  # Signal 2000 µs
        time.sleep(3)

except KeyboardInterrupt:
    print("\nInterruption par l'utilisateur.")

finally:
    # Arrêt de tous les PWM et nettoyage des GPIO
    for motor in motors.values():
        motor.stop()
    GPIO.cleanup()
    print("Moteurs arrêtés et GPIO nettoyé.")
