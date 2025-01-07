import subprocess

def execute_command(command):
    """
    Execute une commande Linux et affiche la sortie.

    :param command: La commande Linux à exécuter (str).
    """
    try:
        # Exécute la commande et capture la sortie
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Affiche la sortie standard et les erreurs
        print("Sortie de la commande :")
        print(result.stdout)
        if result.stderr:
            print("Erreurs :")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")
        print(f"Code de retour : {e.returncode}")
        print(f"Message d'erreur : {e.stderr}")

if __name__ == "__main__":
    # Remplace "ls -l" par la commande Linux que tu veux exécuter
    command = "sudo libcamera-vid -t 0 --inline --framerate 30 -o - | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264"
    execute_command(command)
