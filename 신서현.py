# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
from http import server
import os
from venv import create

import discord
import asyncio

import time
from discord import DiscordException, user
from discord import embeds
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import io
import requests
import server_move_image as movement
import server_everything_id as server_info
import server_chatting_protection as server_chat
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('Shinseohyun_TOKEN')

# create intents before creating bot/client instance
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
# create the instance
client = discord.Client(intents=intents)

async def closed_channel(status):
    if status == True:
        return

    while not client.is_closed():
        await asyncio.sleep(30)
        if len(created_voice_channel.members) == 0:
            await created_voice_channel.delete()
            break

@client.event #켜지는코드 및 상태메세지 돌아가는 것 정리
async def on_ready():
    g="서현 채널 (채널명)"
    await client.change_presence(status = discord.Status.idle, activity = discord.Game(g))
    
@client.event #역할 자동지급, join_log
async def on_member_join(member):
    channel=client.get_channel(server_info.join_channel_id)
    image = movement.join_quit_image("Join",member)
    await channel.send(file = image)
    await member.add_roles(client.get_guild(server_info.guild_id).get_role(server_info.common_role_id), reason="디스코드봇 자동부여")

@client.event #quit_log
async def on_member_remove(member):
    channel=client.get_channel(server_info.quit_channel_id)
    image = movement.join_quit_image("Quit",member)
    await channel.send(file = image)

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id != send_message.id or payload.member.bot == True:
        return

    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if str(payload.emoji) == "✔️":
        await member.move_to(channel = created_voice_channel)
        await closed_channel(None)
    elif str(payload.emoji) == "✖️":
        await created_voice_channel.delete()
        await send_message.delete()
        await closed_channel(True)

@client.event
async def on_message(message):
    #도배막기
    await server_chat.protection_text_channel(message)
    
    if message.author.bot: #봇끼리 반응 X
        return
    
    if message.content.startswith("서현"):
        string_old = message.content.lower().split("서현")
        string = string_old[1].split()
        try:
            if string[0] == "채널":
                await message.delete()
                user_limit_num = None
                for i in string:
                    splitstring = i.split("'")
                    if len(splitstring) != 1:
                        if splitstring[1].isdecimal() == True:
                            user_limit_num = int(splitstring[1])
                            del_num = string.index(i)
                            del string[del_num]
                        else:
                            embed=discord.Embed(description="**정수를 입력해야 합니다!**", color=0x0000ff)
                            await message.channel.send(embed=embed, delete_after = 3)
                            return

                channellist = string
                del channellist[0]
                channelname = ' '.join(channellist)
                global created_voice_channel
                created_voice_channel = await message.guild.categories[3].create_voice_channel(channelname, user_limit=user_limit_num)
                embed=discord.Embed(title="**[JOIN]**", description=f"**<#{created_voice_channel.id}> 여기를 눌러 입장합니다!**", color=0x0000ff)
                embed.set_footer(text = "이 메시지는 30초 뒤에 삭제됩니다! 채널 이동을 원하시면 ✔️를, 채널 삭제를 원하시면 ✖️를 눌러주세요!")

                global send_message
                send_message = await message.channel.send(embed=embed, delete_after = 30)
                await send_message.add_reaction("✔️") #heavy_check_mark
                await send_message.add_reaction("✖️") #heavy_multiplication_x
                
        except Exception as e:
            embed=discord.Embed(title="**에러!**", description=f"**오류가 발생했습니다!**", color=0x0000ff)
            embed.add_field(name = "내용", value = f"```{e}```")
            await message.channel.send(embed=embed, delete_after = 30)
            
            Bot_owner = client.get_user(server_info.server_owner_id)
            channel = await Bot_owner.create_dm()
            embed=discord.Embed(title="**에러!**", description=f"**니가 또 코딩을 잘못했습니다!**", color=0x0000ff)
            embed.add_field(name = "내용", value = f"```{e}```")
            embed.add_field(name = "서버", value = f'{message.author.guild.name}')
            await channel.send(embed=embed)

client.run(TOKEN)