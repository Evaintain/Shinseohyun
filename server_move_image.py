import discord
import asyncio

from discord import user
from discord import embeds
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import io
import requests 

def join_quit_image(status,member):
    left_margin = 15
    right_margin = 15
    top_margin = 15
    bottom_margin = 15
    picture_size = 120

    font_dir = 'font/malgunsl.ttf'

    x = left_margin + picture_size + right_margin
    y = top_margin + picture_size + bottom_margin

    font = ImageFont.truetype(font_dir, 70)
    size = font.getsize(f'[Join] {member}')[0]

    base_image = Image.new('RGB',(x + size + right_margin , y + 15))

    url = str(member.avatar_url).replace("webp?size=1024","jpg")
    res_url = requests.get(url).content
    img = Image.open(io.BytesIO(res_url))
    re_img = img.resize((120,120))
    base_image.paste(re_img, (15 ,15))
    text_color = (255, 255, 255)

    draw = ImageDraw.Draw(base_image)
    draw.text((x, 15), f'[{status}] {member}', text_color, font = font)
                
    f = io.BytesIO()
    base_image.save(f, "PNG")
    f.seek(0)
    image = discord.File(f)
    image.filename = "image.png"
    return image