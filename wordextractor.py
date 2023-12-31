import click
import requests
import re
from bs4 import BeautifulSoup

# Fonction pour obtenir le contenu HTML d'une URL
def get_html_of(url):
    resp = requests.get(url)

    # Vérifie si le code d'état HTTP est différent de 200 (OK)
    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.content.decode()

# Fonction pour compter les occurrences des mots dans une liste, en ignorant ceux de longueur inférieure à min_length
def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        # Ignore les mots de longueur inférieure à min_length
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count

# Fonction pour extraire tous les mots d'une page web
def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)

# Fonction pour obtenir les mots les plus fréquents avec une longueur minimale spécifiée
def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

# Définition de la commande CLI avec click
@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=9, help='Minimum word length (default: 9, no limit).')
def main(url, length):
    # Appelle les fonctions définies précédemment avec les arguments spécifiés par l'utilisateur
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)

    # Affiche les 10 premiers mots les plus fréquents
    for i in range(10):
        print(top_words[i][0])

# Point d'entrée du script
if __name__ == '__main__':
    main()
