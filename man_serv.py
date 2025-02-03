import socket

# Configuration du serveur
HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 12345       # Port d'écoute

def start_server():
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
            print(f"Données reçues : {data}")
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()

