import json
import re
from bs4 import BeautifulSoup
import requests
import textdistance


GOOGLE_SEARCH_API_KEY = 'AIzaSyDfZblS2LrVkjWtHmBHpbCtKsc-aNHWtzk'

def cross_list():
    pass

def main():
    with open('games.json', 'r') as reqs_file, open('cpus.json', 'r') as cpus_file, open('video_cards.json', 'r') as video_cards_file:
        reqs = json.load(reqs_file)
        cpus = json.load(cpus_file)
        video_cards = json.load(video_cards_file)

        for game in reqs['list']:
            if('VIDEO CARD' in game['min_requirements'] and
               'RAM' in game['min_requirements'] and
               'CPU' in game['min_requirements'] and
               'VIDEO CARD' in game['max_requirements'] and
               'RAM' in game['max_requirements'] and
               'CPU' in game['max_requirements']
               ):
                min_req = game['min_requirements']

                min_ram = min_req['RAM'].replace(' ', '').lower()
                min_video = min_req['VIDEO CARD'].lower().split('|')[0].split('/')[0].split(' or ')[0].split(',')[0].replace('®', '')
                min_video = re.sub("[\(\[].*?[\)\]]", "", min_video).strip()
                min_cpu = min_req['CPU'].lower().split('|')[0].split('/')[0].split(' or ')[0].split(',')[0]
                min_cpu = re.sub("[\(\[].*?[\)\]]", "", min_cpu).strip()

                if ('radeon' not in min_video and
                'geforce' not in min_video and
                'gtx' not in min_video and
                'nvidia' not in min_video and
                'gf' not in min_video and
                'amd' not in min_video and
                'quadro' not in min_video and
                'hd' not in min_video and
                'gts' not in min_video and
                'intel' not in min_video):
                    continue

                max_card = ''
                max_card_distance = 0
                for video_card in video_cards.keys():
                    text_distance_level = textdistance.jaro_winkler(min_video, video_card)
                    if max_card_distance < text_distance_level:
                        max_card = video_card
                        max_card_distance= text_distance_level
                # print(f'------------\nMelhor resultado: \n\tESCOLHIDO: {max_card} \n\tORIGINAL: {min_video}')

                max_cpu = ''
                max_cpu_distance = 0
                for cpu in cpus.keys():
                    text_distance_level = textdistance.jaro_winkler(min_cpu, cpu)
                    if max_cpu_distance < text_distance_level:
                        max_cpu = cpu
                        max_cpu_distance= text_distance_level

                # print(f'------------\nMelhor resultado: \n\tESCOLHIDO: {max_cpu} \n\tORIGINAL: {min_cpu}')
    
                try:
                    if('MB'.lower() in min_ram):
                        min_ram = 1.0
                    elif('GB'.lower() in min_ram):
                        min_ram = float(min_ram.lower().split('gb')[0])
                    # print('---------------------------')
                    # print(game['name'])
                    # print('RAM LEVEL: ' + str(min_ram))
                    # print('VIDEO LEVEL: ' + str(video_cards[max_card]))
                    # print('CPU LEVEL: ' + str(cpus[max_cpu]))
                    # print('---------------------------')

                except:
                    pass


if __name__ == "__main__":
    main()