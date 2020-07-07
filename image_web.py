from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json, timeit

IMAGE_TRY_COUNT = 5

driver = webdriver.Chrome('../chromedriver.exe')

games_with_images = {}
for i in range(0, 100):
    with open('games.json', 'r') as games, open('new_images.json', 'r+') as images:
        image_json = json.load(images)
        count = 0
        for game in json.load(games)['list']:
            if count > 10:
                break

            if game['name'] in image_json.keys():
                games_with_images[game['name']] = image_json[game['name']]
                continue

            count += 1
            driver.get("https://images.google.com/?gws_rd=ssl")
            elem = driver.find_element_by_name("q")
            elem.clear()
            elem.send_keys(f"{game['name']} wallpaper")
            elem.send_keys(Keys.RETURN)

            time.sleep(3)

            elem = driver.find_elements_by_css_selector('a img')[3]
            elem.click()
            start_loading = timeit.default_timer()
            # for i in range(0, IMAGE_TRY_COUNT):
            while True:
                imgs = driver.find_elements_by_css_selector('a[role=link][target="_blank"][rel="noopener"] img[jsaction][jsname][data-noaft][alt]')
                image_src = 'data:image'
                if len(imgs) > 0:
                    image_src = imgs[0].get_attribute('src')
                    for img in imgs:
                        if 'data:image' not in img.get_attribute('src') :
                            image_src = img.get_attribute('src')
                            games_with_images[game['name']] = image_src
                            print(f'Imagem carregada: {game["name"]}')
                            break

                if 'data:image' not in image_src:
                    break

                loop_loading = (timeit.default_timer()-start_loading) > 30

                if loop_loading:
                    print(f'Imagem não carregada: {game["name"]}')
                    games_with_images[game['name']] = image_src
                    break


    with open('new_images.json', 'w+') as images:
        json.dump(games_with_images, images, indent=4, sort_keys=True)

driver.close()