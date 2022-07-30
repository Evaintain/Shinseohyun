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
import Assistant_commands as commands
import help_command as help
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('Shinseohyun_TOKEN')

# create intents before creating bot/client instance
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
intents.dm_messages = True
intents.messages = True
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
    
    if payload.user_id != uid:
        return

    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    member = guild.get_member(payload.user_id)

    if str(payload.emoji) == "✔️":
        try:
            await member.move_to(channel = created_voice_channel)
            await closed_channel(None)
        except:
            await commands.voice_move_error(member)

    elif str(payload.emoji) == "✖️":
        await created_voice_channel.delete()
        await send_message.delete()
        await closed_channel(True)
    
    elif str(payload.emoji) == "🟣" or str(payload.emoji) == "🟢" or str(payload.emoji) == "🟠" or str(payload.emoji) == "🔴" or str(payload.emoji) == "⚫":
        await send_message.delete()
        global status
        status = await commands.assistant_raw_reaction_add(payload)

        global server_user_image
        server_user_image = await commands.server_users_image(guild, channel, status)

@client.event
async def on_message(message):
    #도배막기
    await server_chat.protection_text_channel(client, message)
    
    if message.author.bot: #봇끼리 반응 X
        return
    
    if message.content.startswith("서현") or message.content.startswith("%"):
        if message.content.startswith("서현"):
            string = message.content.lower().split()
            n = 1
        else:
            string_old = message.content.lower().split("%")
            string = string_old[1].split()
            n = 0
        try:
            if help.command_list[string[n]] == "채널":
                await message.delete()

                global created_voice_channel
                created_voice_channel = await message.guild.categories[3].create_voice_channel(f"{message.author.name}의 채널")

                await created_voice_channel.set_permissions(message.author, manage_channels = True)

                embed=discord.Embed(title="**[JOIN]**", description=f"**<#{created_voice_channel.id}> 여기를 눌러 입장합니다!**", color=0x0000ff)
                embed.set_footer(text = "이 메시지는 30초 뒤에 삭제됩니다! 채널 이동을 원하시면 ✔️를, 채널 삭제를 원하시면 ✖️를 눌러주세요!")

                global send_message
                send_message = await message.channel.send(embed = embed, delete_after = 30)
                
                global uid #유저 아이디를 전역변수화 시킴으로써 반응에서 이 유저 제외하고 못쓰게 만듦
                uid = message.author.id

                await send_message.add_reaction("✔️") #heavy_check_mark
                await send_message.add_reaction("✖️") #heavy_multiplication_x
            
            if help.command_list[string[n]] == "서버명단":
                await message.delete()

                uid = message.author.id

                embed=discord.Embed(title="**[설명]**", description=f"**🟣 전체 \| 🟢 온라인 \| 🟠 자리비움 \| 🔴 다른 용무중 \| ⚫ 오프라인**", color=0x0000ff)
                embed.set_footer(text = "컴퓨터 | 노트북 에 켜져있는 디스코드만 적용됩니다!")
                send_message = await message.channel.send(embed=embed, delete_after = 30)

                await send_message.add_reaction("🟣") #purple_circle
                await send_message.add_reaction("🟢") #green_circle
                await send_message.add_reaction("🟠") #orange_circle
                await send_message.add_reaction("🔴") #red_circle
                await send_message.add_reaction("⚫") #black_circle
            
        except discord.errors.Forbidden:
            await commands.permisson_error(message)
                
        except Exception as e:
            await commands.notice_error(message, client, e)
        
        

client.run(TOKEN)