import json
import re
from bs4 import BeautifulSoup
import requests

def gpus():
    session = requests.Session()

    session.timeout = 10000

    response = session.get('https://www.videocardbenchmark.net/gpu_list.php')
    document = BeautifulSoup(response.content, 'html.parser')

    gputable = document.select_one('#cputable').find('tbody')

    count = 0
    gpu_list = {}
    for gpu in gputable:
        count += 1
        # if count > 10:
        #     break

        if gpu.find('a') != -1 and gpu.find('a') != None:
            gpu_name = gpu.find('a').string.lower()
            gpu_list[gpu_name] = float(gpu.findAll('td')[1].string)

    with open('video_cards.json', 'w+') as file:
        json.dump(gpu_list, file,indent=4, sort_keys=True)

    print(gpu_list)

def cpus():
    session = requests.Session()

    session.timeout = 10000

    response = session.get('https://www.cpubenchmark.net/cpu_list.php')
    document = BeautifulSoup(response.content, 'html.parser')

    cputable = document.select_one('#cputable').find('tbody')

    count = 0
    cpu_list = {}
    for cpu in cputable:
        count += 1
        # if count > 10:
        #     break

        if cpu.find('a') != -1 and cpu.find('a') != None:
            cpu_name = cpu.find('a').string.lower()
            cpu_list[cpu_name] = float(cpu.findAll('td')[1].string.replace(',', ''))

    with open('cpus.json', 'w+') as file:
        json.dump(cpu_list, file,indent=4, sort_keys=True)

    print(cpu_list)

if __name__ == "__main__":
    gpus()
    cpus()