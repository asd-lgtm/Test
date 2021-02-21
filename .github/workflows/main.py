#!/usr/bin/env python3

refresh_time = 1 # апдейт хешрейта каждые n секунд
autorestart_time = 600 # Перезапуск каждые n секунд. 0 = никогда.

import multiprocessing, threading, socket, hashlib, os, urllib.request, statistics, random, sys, time


if sys.platform == "win32":
    try:
        from colorama import init, Fore, Back, Style
        init()
    except:
        print("У вас не установлен colorama, установить сейчас?")
        choice = input("(y/n): ")
        if choice == "y":
            os.system("pip install colorama")
        else:
            os._exit(1)
    colorama_choice = True
else:
    colorama_choice = False

class bcolors:
    blue = '\033[36m'
    yellow = '\033[93m'
    endc = '\033[0m'
    back_cyan = '\033[46m'
    red = '\033[31m'
    back_yellow = '\033[43m'
    black = '\033[30m'
    back_red = '\033[41m'

last_hash_count = 0
khash_count = 0
hash_count = 0
hash_mean = []

def hashrateCalculator():
    global last_hash_count, hash_count, khash_count, hash_mean
  
    last_hash_count = hash_count
    khash_count = last_hash_count / 1000
    if khash_count == 0:
        khash_count = random.uniform(0, 1)
    
    hash_mean.append(khash_count)
    khash_count = statistics.mean(hash_mean)
    khash_count = round(khash_count, 2)
  
    hash_count = 0
  
    threading.Timer(1.0, hashrateCalculator).start()

    
def start_thread(arr, i, username, accepted_shares, bad_shares, thread_number):
    global hash_count, khash_count
    soc = socket.socket()

    serverip = "https://mhcoin.s3.filebase.com/Pool.txt"
    with urllib.request.urlopen(serverip) as content:
        content = content.read().decode().splitlines()
    pool_address = content[0]
    pool_port = content[1]

    soc.connect((str(pool_address), int(pool_port)))
    soc.recv(3).decode()

    hashrateCalculator()
    while True:
        try:
            soc.send(bytes("JOB,"+str(username), encoding="utf8"))
            job = soc.recv(1024).decode()
            job = job.split(",")
            try:
                difficulty = job[2]
            except:
                for p in multiprocessing.active_children():
                    p.terminate()
                time.sleep(1)
                sys.argv.append(str(thread_number))
                os.execl(sys.executable, sys.executable, *sys.argv)

            for result in range(100 * int(difficulty) + 1):
                hash_count = hash_count + 1
                ducos1 = hashlib.sha1(str(job[0] + str(result)).encode("utf-8")).hexdigest()
                if job[1] == ducos1:
                    soc.send(bytes(str(result) + "," + str(last_hash_count) + ",Repl.it Multithreaded Miner", encoding="utf8"))
                    feedback = soc.recv(1024).decode()
                    arr[i] = khash_count
                    if feedback == "GOOD" or feedback == "BLOCK":
                        accepted_shares[i] += 1
                        break
                    elif feedback == "BAD":
                        bad_shares[i] += 1
                        break
                    elif feedback == "INVU":
                        print("Пользователь не существует!")
        except (KeyboardInterrupt, SystemExit):
            print("Поток #{}: завершен...".format(i))
            os._exit(0)


def autorestarter():
    time.sleep(autorestart_time)
    
    for p in multiprocessing.active_children():
        p.terminate()
    time.sleep(1)
    sys.argv.append(str(thread_number))
    os.execl(sys.executable, sys.executable, *sys.argv)

def showOutput():
    clear()

    d = {}
    for thread in range(thread_number):
        d[f"#{thread + 1}"] = [f"{hashrate_array[thread]} kH/s", accepted_shares[thread], bad_shares[thread]]

    if colorama_choice:
        print(Fore.YELLOW + Back.CYAN + "{:<9} {:<13} {:<10} {:<10}".format('Thread','Hashrate','Accepted','Rejected') + Style.RESET_ALL)
    else:
        print(bcolors.yellow + bcolors.back_cyan + "{:<9} {:<13} {:<10} {:<10}".format('Thread','Hashrate','Accepted','Rejected') + bcolors.endc)
    for k, v in d.items():
        hashrate, good, bad = v
        if colorama_choice:
            print(Fore.CYAN + "{:<9} {:<13} {:<10} {:<10}".format(k, hashrate, good, bad) + Style.RESET_ALL)
        else:
            print(bcolors.blue + "{:<9} {:<13} {:<10} {:<10}".format(k, hashrate, good, bad) + bcolors.endc)
    
    if colorama_choice:
        print(Back.RED + "{:<9} {:<13} {:<10} {:<10}".format("TOTAL", totalHashrate(sum(hashrate_array)), sum(accepted_shares), sum(bad_shares)) + Style.RESET_ALL)
    else:
        print(bcolors.back_red + "{:<9} {:<13} {:<10} {:<10}".format("TOTAL", totalHashrate(sum(hashrate_array)), sum(accepted_shares), sum(bad_shares)) + bcolors.endc)

    threading.Timer(float(refresh_time), showOutput).start()
        

def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def totalHashrate(khash):
    if khash / 1000 >= 1:
        return str(round(khash / 1000, 2)) + " MH/s"
    else:
        return str(round(khash, 2)) + " kH/s"


if __name__ == '__main__':
    global thread_number, curr_bal
 
    if (autorestart_time) > 0:
        threading.Thread(target=autorestarter).start()

    with urllib.request.urlopen("https://mhcoin.s3.filebase.com/Server.txt") as content:
        content = content.read().decode().splitlines()
    pool_address = content[0]
    pool_port = content[1]
    
    arguments = len(sys.argv)
    if arguments <= 2:
        if colorama_choice:
            print(Fore.RED + "Введи username и количество потоков!" + Style.RESET_ALL)
            print(Fore.YELLOW + "Пример: python3 Multithreaded_PC_Miner.py username 8" + Style.RESET_ALL)
            print(Fore.RED + "Выход через 15 секунд." + Style.RESET_ALL)
        #else:
        #    print(bcolors.red + "Введи username и количество потоков!" + bcolors.endc)
        #    print(bcolors.yellow + "Пример: python3 Multithreaded_PC_Miner.py username 8" + bcolors.endc)
        #    print(bcolors.red + "Выход через 15 секунд." + bcolors.endc)
        #time.sleep(15)
        #os._exit(0)

    username = 'sheeplover'   #str(sys.argv[1])
    thread_number = 5 #int(sys.argv[2])
    print(f"Майнер для пользователя {username} запущен с {thread_number} потоком(и).")

    hashrate_array = multiprocessing.Array("d", thread_number)
    accepted_shares = multiprocessing.Array("i", thread_number)
    bad_shares = multiprocessing.Array("i", thread_number)

    showOutput()

    for i in range(thread_number):
        p = multiprocessing.Process(target=start_thread, args=(hashrate_array, i, username, accepted_shares, bad_shares, thread_number))
        p.start()
        time.sleep(0.5)
    time.sleep(1)
    
