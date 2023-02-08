import threading
from Wallet_miner_BTC import miner
from time import sleep
threads = []

for _ in range(300): #définir le nombre de thread sur lesquelles le programmes va tourner
    sleep(0.3)
    t = threading.Thread(target=miner)
    t.start()
    threads.append(t)

for thread in threads: #lancer le programme
    thread.join()