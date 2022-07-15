import discord
import asyncio
import server_everything_id as server_info

async def check_whether_num(message ,string):
    for i in string:
        splitstring = i.split("'")
        if len(splitstring) != 1:
            if splitstring[1].isdecimal() == True:
                user_limit_num = int(splitstring[1])
                del_num = string.index(i)
                del string[del_num]

                return user_limit_num
            else:
                embed=discord.Embed(description="**정수를 입력해야 합니다!**", color=0x0000ff)
                await message.channel.send(embed=embed, delete_after = 3)

                return None

async def notice_error(message, client, e):
    embed_to_server = discord.Embed(title="**에러!**", description=f"**오류가 발생했습니다!**", color=0x0000ff)
    embed_to_server.add_field(name="내용", value=f"```{e}```")
    await message.channel.send(embed=embed_to_server, delete_after = 30)
            
    Bot_owner = client.get_user(server_info.server_owner_id)
    channel = await Bot_owner.create_dm()
    embed_to_Bot_owner=discord.Embed(title="**에러!**", description=f"**니가 또 코딩을 잘못했습니다!**", color=0x0000ff)
    embed_to_Bot_owner.add_field(name = "내용", value = f"```{e}```")
    embed_to_Bot_owner.add_field(name = "서버", value = f'{message.author.guild.name}')
    await channel.send(embed = embed_to_Bot_owner)

