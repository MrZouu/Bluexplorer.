import spidev
import time
import RPi.GPIO as GPIO

### DESCRIPTION ###
# lit la valeur brute d'un canal ADC sur un MCP3008
# convertit cette valeur brute en une tension comprise entre 0 et 3.3V
# Permet de lire la valeur du capteur TDS (qualité de l'eau)

# Initialisation de la communication SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, périphérique 0 (CE0)
spi.max_speed_hz = 1350000

# Configuration de GPIO pour CS (GPIO 5)
CS_PIN = 5
GPIO.setmode(GPIO.BCM)  # Utiliser le mode BCM pour le GPIO
GPIO.setup(CS_PIN, GPIO.OUT)  # Configurer GPIO 5 en sortie

def read_adc(channel):
    """Lire la valeur du canal ADC"""
    if channel < 0 or channel > 7:
        raise ValueError("Canal doit être entre 0 et 7")
    
    # Activer le CS
    GPIO.output(CS_PIN, GPIO.LOW)
    
    # Envoi de la commande SPI pour lire le canal
    command = [1, (8 + channel) << 4, 0]
    response = spi.xfer2(command)
    value = ((response[1] & 3) << 8) | response[2]
    
    # Désactiver le CS
    GPIO.output(CS_PIN, GPIO.HIGH)
    
    return value

# Test de lecture de la valeur brute sur CH0
try:
    print("Lecture du canal CH0 :")
    while True:
        raw_value = read_adc(0)  # Lire le canal CH0
        voltage = (raw_value * 3.3) / 1023.0  # Conversion en tension (3.3V réf)
        
        # Exemple de conversion (à adapter selon le capteur)
        print(f"Valeur brute : {raw_value} | Tension : {voltage:.3f} V")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")
finally:
    spi.close()
    GPIO.cleanup()  # Nettoyer les configurations GPIO
