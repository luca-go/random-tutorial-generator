import requests
import json
from whapi import get_id, random_article, return_details, get_images
import random
import time
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont
import os

path = (os.path.dirname(os.path.realpath(__file__)))

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

    im1 = Image.open(imlistio[0])           #for cycle somehow breaks the resizing
    im2 = Image.open(imlistio[1])
    im3 = Image.open(imlistio[2])
    im4 = Image.open(imlistio[3])

    im1 = im1.resize((800, 600))
    im2 = im2.resize((800, 600))
    im3 = im3.resize((800, 600))
    im4 = im4.resize((800, 600))

    back = Image.new('RGBA', (1600, 1500), 'white')
    back_im = back.copy()
    back_im.paste(im1, (0, 300))
    back_im.paste(im2, (800, 300))
    back_im.paste(im3, (0, 900))
    back_im.paste(im4, (800, 900))

    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype(path + '/Roboto-Regular.ttf', 80)

    draw.text((5, 20), get_title(),(0,0,0),font=font)

    back_im.save(path + '/tutorial.png', quality=100)
    back_im.show()

if __name__ == "__main__":
    print_tutorial()