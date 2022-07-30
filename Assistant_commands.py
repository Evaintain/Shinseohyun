import discord
import asyncio

import server_everything_id as server_info
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import io
import requests 

async def notice_error(message, client, e):
    embed_to_server = await notice_error_assistant(e)
    await message.channel.send(embed=embed_to_server, delete_after = 30)
            
    Bot_owner = client.get_user(server_info.server_owner_id)
    channel = await Bot_owner.create_dm()
    embed_to_Bot_owner = await notice_error_assistant(e)
    embed_to_Bot_owner.add_field(name = "서버", value = f'{message.author.guild.name}')
    await channel.send(embed = embed_to_Bot_owner)

async def notice_error_assistant(e):
    embed = discord.Embed(title="**에러!**", description=f"**오류가 발생했습니다!**", color=0x0000ff)
    embed.add_field(name="내용", value=f"```{e}```")
    return embed

async def permisson_error(message):
    embed_to_server = await notice_error_assistant("권한 설정의 오류입니다. 봇을 다시 초대하거나 권한을 넣어주세요")
    embed_to_server.add_field(name="권한", value=f"```메시지 관리, 채널 관리, 메시지 보내기, 메시지 기록 보기, 링크 첨부, 반응 추가하기, 멤버 이동```")
    embed_to_server.add_field(name="링크", value=f"[봇 초대](<https://discord.com/api/oauth2/authorize?client_id=883327869881831444&permissions=285232208&scope=bot>)", inline = False)
    await message.channel.send(embed=embed_to_server, delete_after = 30)

async def voice_move_error(member):
    channel = await member.create_dm()
    error_embed = await notice_error_assistant("음성채널에 연결되어 있지 않습니다!")
    await channel.send(embed = error_embed)

async def server_users_image(guild, channel, status):
    left_margin = 5
    right_margin = 5
    top_margin = 5
    bottom_margin = 5
    picture_size = 20
    picture_margin = 5
    font_size = 15
    player_list = []
    member_list = []
    member_list_append_list = []
    fontsize_list = []
    fontsize_list_append_list = []
    max_size_list = []
    max_size = 0
    draw_try = 0
    size_try = 0
    row_maximum = 15
    member_try = 0

    font_dir = 'font/malgunsl.ttf'
    
    for p in guild.members:
        if p.bot != True and str(p.desktop_status) in status: 
            player_list.append(p) # 여기서 사람만 리스트에 들어감


    for i in player_list:
        font = ImageFont.truetype(font_dir, 20)
                        
        member_list_append_list.append(i)
        fontsize_list_append_list.append(font.getsize(f'{i.name}')[0])
        member_try +=1

        if len(member_list_append_list) == row_maximum:
            member_list.append(member_list_append_list)
            fontsize_list.append(fontsize_list_append_list)
            member_list_append_list = []
            fontsize_list_append_list = []

        if (len(player_list) - member_try) == 0:
            member_list.append(member_list_append_list)
            fontsize_list.append(fontsize_list_append_list)
                        

    for k in fontsize_list:
        max_size_list.append(max(k))
        max_size += max(k)
        max_size += picture_size

    if len(fontsize_list) == 1:
        length_size = len(fontsize_list_append_list)
    else:
        length_size = row_maximum


    x = left_margin + picture_size + picture_margin
    y = top_margin
    x_picture = 0

    base_image = Image.new('RGB',(left_margin + max_size + right_margin, top_margin + length_size * (picture_size + picture_margin) + bottom_margin))

    for l in member_list:
        for j in l:
            url = str(j.avatar_url).replace("webp?size=1024","jpg")
            res_url = requests.get(url).content
            img = Image.open(io.BytesIO(res_url))
            re_img = img.resize((picture_size, picture_size))
            base_image.paste(re_img, (left_margin + x_picture ,y))
            text_color = (255, 255, 255)
            font = ImageFont.truetype(font_dir, font_size)

            draw = ImageDraw.Draw(base_image)
            draw.text((x, y), f'{j.name}', text_color, font = font)

            y += picture_margin + picture_size
            draw_try += 1
            if draw_try % row_maximum == 0:
                x += max_size_list[size_try]
                x_picture += max_size_list[size_try]
                y -= (picture_margin + picture_size) * row_maximum

                
    f = io.BytesIO()
    base_image.save(f, "PNG")
    f.seek(0)
    image = discord.File(f)
    image.filename = "image.png"
    await channel.send(file = image, delete_after = 30)

async def assistant_raw_reaction_add(payload):
    if str(payload.emoji) == "🟣":
        return ["online","idle","dnd","offline"]

    elif str(payload.emoji) == "🟢":
        return ["online"]

    elif str(payload.emoji) == "🟠":
        return ["idle"]
    
    elif str(payload.emoji) == "🔴":
        return ["dnd"]
    
    elif str(payload.emoji) == "⚫":
        return ["offline"]
