import os
import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def convert(quote, fg, image, border_color, font_file=None, font_size=None,width=None,height=None):
    x1 = width if width else 612
    y1 = height if height else 612
        
    sentence = f"{quote}"
    
    quote = ImageFont.truetype(os.path.join(BASE_DIR, 'MoDiLipiBot\\fonts', 'NotoSansModiAdvanced.ttf'), 70, layout_engine=ImageFont.LAYOUT_RAQM)

    img = Image.new("RGB", (x1, y1), color=(255,255,255))

    back = Image.open(image, 'r')
    img_w, img_h = back.size
    bg_w, bg_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    bback=back.filter(ImageFilter.BLUR)
    img.paste(bback, offset)
    
    d = ImageDraw.Draw(img)

    sum = 0
    for letter in sentence:
        sum += d.textsize(letter, font=quote)[0]
    average_length_of_letter = sum / len(sentence)

    number_of_letters_for_each_line = (x1 / 1.618) / average_length_of_letter
    incrementer = 0
    fresh_sentence = ""

    for letter in sentence:
        if letter == "-":
            fresh_sentence += "\n\n" + letter
        elif incrementer < number_of_letters_for_each_line:
            fresh_sentence += letter
        else:
            if letter == " ":
                fresh_sentence += "\n"
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer += 1
    dim = d.textsize(fresh_sentence, font=quote)
    x2 = dim[0]
    y2 = dim[1]

    qx = x1 / 2 - x2 / 2
    qy = y1 / 2 - y2 / 2

    d.text((qx-1, qy-1), fresh_sentence, align="center", font=quote, fill=border_color)
    d.text((qx+1, qy-1), fresh_sentence, align="center", font=quote, fill=border_color)
    d.text((qx-1, qy+1), fresh_sentence, align="center", font=quote, fill=border_color)
    d.text((qx+1, qy+1), fresh_sentence, align="center", font=quote, fill=border_color)

    d.text((qx, qy), fresh_sentence, align="center", font=quote, fill=fg)

    return img


def get_base64(image):
    img = Image.open(image)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode()

