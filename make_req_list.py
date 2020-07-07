import requests
import json
import time
import timeit
import asyncio
from random import randint
from bs4 import BeautifulSoup
import multiprocessing.dummy as mp 


def read_html(html_doc):
    return BeautifulSoup(html_doc, 'html.parser')

def get_requirements(plist):
    if not plist:
        return {}
    req_list = {}
    for line in plist:
        if(len(str(line.string).replace(' ', '').replace('\n', '')) > 0):
            req_list[str(line.string.split(':')[0]).strip()] = str(line.string.split(':')[1]).strip()
    return req_list

def generate_game_dict(document):
    game_title = document.title.string.split('system requirements')[0].strip()
    min_req = document.find('h2', id='requirement-specs').find_next_sibling('ul')
    max_req = min_req.find_next_sibling('ul')

    return  {
        'name': game_title,
        'min_requirements': get_requirements(min_req),
        'max_requirements': get_requirements(max_req)
    }

def get_game_list(session):
    response = session.get('https://www.systemrequirementslab.com/cyri')
    document = read_html(response.content)
    # count = 0
    link_list = []
    for li in document.find('ul', class_='ul-most-popular'):
        a = li.find('a')

        if a != -1:
            link_list.append(a['href'])

        # count += 1

        # if count > 2:
        #     break

    return link_list

def get_game_page(link, session):
     response = session.get(link)

     document = read_html(response.content)

     return document




def main():
    session = requests.Session()

    session.timeout = 10000

    game_list = get_game_list(session)

    file_data = { 'list': []}

    start_time = timeit.default_timer()

    def make_game(game):
        try:
            game_page = get_game_page(game, session)
            print("Acessando: " + game_page.title.string)
            file_data['list'].append(generate_game_dict(game_page))
            # time.sleep(randint(3, 12))
        except:
            print("ERRO: " + game)

    print('Started')

    p=mp.Pool(100)
    p.map(make_game, game_list)
    p.close()
    p.join()

    with open('games.json', 'w+') as file:
        json.dump(file_data, file, indent=4, sort_keys=True)
    end_time = timeit.default_timer()

    print('End: ' + str(end_time-start_time))

if __name__ == "__main__":
    main()