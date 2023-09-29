import requests
import json
import argparse
import time
import os


API_KEYS_FILE = "api_keys.txt"

def load_api_keys():
    try:
        with open(API_KEYS_FILE, 'r') as file:
            return [key.strip() for key in file.readlines()]
    except FileNotFoundError:
        return []

def get_next_api_key(current_api_key):
    with open("api_keys.txt", "r") as file:
        lines = file.readlines()
        for i, key in enumerate(lines):
            if key.strip() == current_api_key:
                if i + 1 < len(lines):
                    return lines[i + 1].strip()  # Retourne la clé API suivante
                else:
                    return None  # Aucune autre clé disponible
    return None

def add_api_key(new_key):
    if new_key not in api_keys:
        api_keys.append(new_key)
        with open(API_KEYS_FILE, 'a') as file:
            file.write(new_key + '\n')
        str_matrix("Clé API ajoutée avec succès.\n")
    else:
        str_matrix("Cette clé API est déjà enregistrée.")

def remove_api_key(old_key):
    if old_key in api_keys:
        api_keys.remove(old_key)
        with open(API_KEYS_FILE, 'w') as file:
            for key in api_keys:
                file.write(key + '\n')
        str_matrix("Clé API supprimée avec succès.\n")
    else:
        str_matrix("Cette clé API n'est pas enregistrée.")

def validate_api_key(api_key):
    return len(api_key) == 32 and all(char in "0123456789ABCDEFabcdef" for char in api_key)

def save_api_keys():
    with open(API_KEYS_FILE, 'w') as file:
        for key in api_keys:
            file.write(key + '\n')

def str_matrix(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.033)

api_keys = load_api_keys()

parser = argparse.ArgumentParser(description="Recherchez des informations dans la base de données Leak Lookup.")
parser.add_argument("-addapi", action="store_true", help="Ajoutez une nouvelle clé API à la liste")
parser.add_argument("-removeapi", action="store_true", help="Supprimez une clé de la liste")
parser.add_argument("-listapi", action="store_true", help="Liste toutes les clés API enregistrées")

args = parser.parse_args()

# Vérifiez si le fichier api_keys.txt est vide ou ne contient pas de clé API valide
if not api_keys or not any(validate_api_key(key) for key in api_keys):
    str_matrix("Votre fichier api_keys.txt est vide ou ne contient pas de clé API valide.")
    new_key = ""
    while not validate_api_key(new_key):
        str_matrix("Veuillez saisir une clé API valide: ")
        new_key = input(": ")
    add_api_key(new_key)
    save_api_keys()

if args.addapi:
    str_matrix("Veuillez saisir la nouvelle clé API à ajouter: ")
    new_key = input(": ")
    if validate_api_key(new_key):
        add_api_key(new_key)
    else:
        str_matrix("Clé API invalide.")
    exit(0)

if args.removeapi:
    str_matrix("Veuillez saisir la clé API à supprimer ")
    old_key = input(": ")
    remove_api_key(old_key)
    exit(0)

if args.listapi:
    if len(api_keys) == 0:
        str_matrix("Aucune clé API enregistrée.\n")
    else:
        str_matrix("Clés API enregistrées:\n")
        for key in api_keys:
            str_matrix(key + "\n")
    exit(0)

api_key_index = 0
api_key = api_keys[api_key_index] if api_keys else "" 

url = "https://leak-lookup.com/api/search"
str_matrix("Entrez la recherche souhaitée ")
query = input(": ")

# Paramètres de la requête


def send_and_print_request(api_key):  

    params = {
    "key": api_key,
    "type": "email_address",
    "query": query,  # Utilisez la valeur saisie par l'utilisateur
    "fields": [
        "userid", "uid", "memberid", "member_id", "email_address", "emailaddress", "email", 
        "email_address2", "emailaddress2", "email2", "membername", "username", "uname", 
        "user_name", "member_name", "ipaddress", "ip_address", "ip", "password", "password2", 
        "password3", "password4", "plaintext", "hash", "salt", "salt2", "salt3", "secret", 
        "key", "firstname", "first_name", "fname", "lastname", "last_name", "lname", "fullname", 
        "full_name", "number", "phone", "mobile", "telephone", "address", "address1", "address2", 
        "address3", "city", "state", "country", "county", "postcode", "zipcode", "postalcode", "zip", 
        "breachname", "fb_id", "facebook_id", "fbid"
    ]
}
    
    while True:  # Boucle pour traiter la réponse
        response = requests.post(url, data=params)
        data = json.loads(response.text)
        
        # Traitement des données obtenues dans la réponse
        if "message" in data and isinstance(data["message"], dict):
            total_results = response.text.count("[")
            cleaned_response = response.text.replace('{"error":"false","message":', '').rstrip('}')
            cleaned_response = cleaned_response.replace("{", "").replace("}", "")
            formatted_output = cleaned_response.replace(",", "\n")
            str_matrix(f"Nombre total de résultats : {total_results}\n")
            str_matrix(formatted_output)
        else:
            str_matrix("Nombre maximum de requêtes atteint.\n")
            next_key = get_next_api_key(api_key)
            if next_key:
                api_key = next_key
                str_matrix(f"Changement de clé API. Nouvelle clé: {api_key}\n")
                send_and_print_request(api_key)
                break  # Continue la boucle avec la nouvelle clé API
            str_matrix("Veuillez saisir une nouvelle clé API valide: ")
            new_key = input(": ")
            while not validate_api_key(new_key):
                str_matrix("Clé API invalide. Veuillez saisir une nouvelle clé API valide: ")
                new_key = input(": ")
            add_api_key(new_key)
            api_key = new_key
            save_api_keys()
            send_and_print_request(api_key)
        break

send_and_print_request(api_key)

print("\n")
