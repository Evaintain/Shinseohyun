import discord
import asyncio
import server_everything_id as server_info
import Assistant_commands as commands

async def protection_text_channel(client, message):
    if message.embeds is not None:
        return

    if message.attachments is not None:
        return

    get_guild = client.get_guild(message.author.guild.id)
    get_member = get_guild.get_member(message.author.id)

    member_roles = get_member.roles
    n = 0
    for i in member_roles:
        if int(i.id) == server_info.ban_role_id:
            n = 1
    mame = message.author.guild_permissions.value
    member = message.author
    permissions = discord.Permissions.administrator.flag
    if int(mame) & int(permissions) != 0:
        if len(message.content) > 1500:
            text_channel_send_message = '1500자 이내로 써주시길 바랍니다'
            await ban_process(n, message, member, text_channel_send_message)

    else:
        if len(message.content) > 500:
            text_channel_send_message = '500자 이내로 써주시길 바랍니다'
            await ban_process(n, message, member, text_channel_send_message)

    message_split = message.content.split()
    for i in message_split:
        if message_split.count(i) > 20:
            text_channel_send_message = '같은 단어가 20회 초과 반복되어 도배로 간주합니다'
            await ban_process(n, message, member, text_channel_send_message)

    m_s = []
    for j in message.content:
        if j not in m_s:
            m_s.append(j)
    for k in m_s:
        if int(mame) & int(permissions) != 0:
            if message.content.count(k) > 800:
                text_channel_send_message = '같은 글자가 800회 초과 반복되어 도배로 간주합니다'
                await ban_process(n, message, member, text_channel_send_message)
        else:
            if message.content.count(k) > 200:
                text_channel_send_message = '같은 글자가 200회 초과 반복되어 도배로 간주합니다'
                await ban_process(n, message, member, text_channel_send_message)

async def ban_process(whether_ban, message, member, send_message):
    channel_send_message = await message.channel.send(f'**도배에 걸렸습니다 5초 뒤에 지워집니다 {message.author.mention} {send_message}**', delete_after = 10) #도배에 걸린 사유
    time = 5
    while time > 0:
        await asyncio.sleep(1)
        time -= 1
        await channel_send_message.edit(content = f"도배에 걸렸습니다 {time}초 뒤에 지워집니다 {message.author.mention} {send_message}")
    await message.delete() #유저가 채널에 보낸 메시지 삭제
    await member.add_roles(message.author.guild.get_role(server_info.ban_role_id), reason="도배") #도배 밴
    await asyncio.sleep(120)
    if whether_ban == 1:
        return
    await member.remove_roles(message.author.guild.get_role(server_info.ban_role_id), reason="도배")