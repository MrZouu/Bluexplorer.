import RPi.GPIO as GPIO
import time

### DESCRIPTION ###
# Controle un seul moteur via une broche GPIO
# trois niveaux de puissance (5%, 7.5%, 20%)

# Configuration de la broche GPIO
MOTOR_PIN = 18
FREQUENCY = 50  # Fréquence typique pour un ESC : 50 Hz

# Initialisation de la broche GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Création de l'instance PWM
motor = GPIO.PWM(MOTOR_PIN, FREQUENCY)

try:
    # Démarrage du signal PWM
    motor.start(0)
    print("Envoi de signaux PWM pour tester l'ESC. Appuyez sur Ctrl+C pour arrêter.")

    # Tester différentes valeurs du cycle de travail
    while True:
        print("Cycle de travail : 5% (arrêt)")
        motor.ChangeDutyCycle(5)  # Signal 1000 µs
        time.sleep(3)

        print("Cycle de travail : 7.5% (neutre)")
        motor.ChangeDutyCycle(7.5)  # Signal 1500 µs
        time.sleep(3)

        print("Cycle de travail : 9% (vitesse maximale)")
        motor.ChangeDutyCycle(20) # Signal 2000 µs
        time.sleep(3)

except KeyboardInterrupt:
    print("\nInterruption par l'utilisateur.")

finally:
    motor.stop()
    GPIO.cleanup()
    print("Moteur arrêté et GPIO nettoyé.")

