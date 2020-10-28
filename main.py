import requests
import json
from whapi import get_id, random_article, return_details
import random
import time
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont
import os

path = (os.path.dirname(os.path.realpath(__file__)))
api = 'https://www.wikihow.com/api.php?format=json&action='

def get_images(id):
    images = []
    r = requests.get(api + 'parse&prop=images&pageid=' + str(id))
    data = r.json()
    image_list = data['parse']['images']
    if not image_list:
        raise ParseError
    else:
        for i in image_list:
            im_data = requests.get(api + 'query&titles=File:' + i + '&prop=imageinfo&iiprop=url')
            image_info = im_data.json()
            pages = image_info['query']['pages']
            for key in pages.keys():
                image_url = pages[key]['imageinfo'][0]['url']
                if image_url != 'https://www.wikihow.com/images/7/78/Incomplete_856.gif':
                    images.append(image_url)
                
    return images

def get_title():
    random_howto = random_article() #returns an ID

    article_info = return_details(random_howto) #gets the info in a dict

    title = 'How to ' + (article_info['title'])

    text = title
    n = 42

    words = iter(text.split())
    lines, current = [], next(words)
    for word in words:
        if len(current) + 1 + len(word) > n:
            lines.append(current + ' \n')
            current = word
        else:
            current += ' ' + word
    lines.append(current)

    titleok = '\n'.join(lines)

    return titleok

def print_tutorial():

    imlistio = []
    for k in range (4):
        images = []

        random_howto = random_article()
        first_list = get_images(random_howto)

        max1 = len(first_list)
        images.append(first_list[random.randrange(0,max1)])

        max = len(images)
        image1 = images[random.randrange(0,max)]

        response = requests.get(image1)
        img = io.BytesIO(response.content)
        imlistio.append(img)    #imgs to be resized
        time.sleep(0.5)
        k = k + 1        

    
    listresized = list(map(resize, imlistio))

    back = Image.new('RGBA', (1600, 1500), 'white')
    back_im = back.copy()
    back_im.paste(listresized[0], (0, 300))
    back_im.paste(listresized[1], (800, 300))
    back_im.paste(listresized[2], (0, 900))
    back_im.paste(listresized[3], (800, 900))

    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype(path + '/Roboto-Regular.ttf', 80)

    draw.text((5, 20), get_title(),(0,0,0),font=font)

    back_im.save(path + '/tutorial.png', quality=100)
    back_im.show()

def resize(im):
    image = Image.open(im)
    resized_image = image.resize((800, 600))
    return resized_image


if __name__ == "__main__":
    print_tutorial()