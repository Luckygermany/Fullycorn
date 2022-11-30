import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
import discord.ui
import json
import sqlite3

conn = sqlite3.connect('temp.db')
cursor = conn.cursor()


client = commands.Bot(intents=discord.Intents.all(),command_prefix='!!')
client.remove_command("help")

@client.tree.command(name="say")
async def say(interaction: discord.Interaction, title: str, description: str):
    embed = discord.Embed(title=f"{title}", description=f"{description}")
    await interaction.response.send_message(embed=embed)

class btn4(discord.ui.View):
    @discord.ui.button(label="Yes", emoji="✅", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        chan = client.get_channel(interaction.channel_id)
        embed= discord.Embed(title="Ticket closed", description="Ticket will be deleted in 5 seconds")
        q = await chan.send(embed=embed)
        await asyncio.sleep(1)
        embed= discord.Embed(title="Ticket closed", description="Ticket will be deleted in 4 seconds")
        await q.edit(embed=embed)
        await asyncio.sleep(1)
        embed= discord.Embed(title="Ticket closed", description="Ticket will be deleted in 3 seconds")
        await q.edit(embed=embed)
        await asyncio.sleep(1)
        embed= discord.Embed(title="Ticket closed", description="Ticket will be deleted in 2 seconds")
        await q.edit(embed=embed)
        await asyncio.sleep(1)
        embed= discord.Embed(title="Ticket closed", description="Ticket will be deleted in 1 seconds")
        await q.edit(embed=embed)
        await asyncio.sleep(1)
        await chan.delete()
class btn3(discord.ui.View):
    discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="❌")
    async def close(self, interaction: discord.Interaction, button: discord.Button):
        chan = client.get_channel(interaction.channel_id)
        embed = discord.Embed(title=f"{interaction.user.name}", description="Are you sure to close the ticket")
        view = btn4()
        await chan.send(embed=embed, view=view)
    discord.ui.button(label="Claim", emoji="🔒", style=discord.ButtonStyle.green)
    async def claim(self, interaction: discord.Interaction, button: discord.Button):
        ebed= discord.Embed(title=f"Ticket Claim", description=f"> Ticket claimed by {interaction.user.mention}")
        chan = client.get_channel(interaction.channel_id)
        await chan.send(embed=ebed)


class btn2(discord.ui.View):
    discord.ui.button(label="Ticket offnen", emoji="🎟️", style=discord.ButtonStyle.green)
    async def cs(self, interaction: discord.Interaction, button: discord.Button):
        s = interaction.channel_id
        chan = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user}")
        with open(f"{interaction.guild.id}.json", "r") as fp:
            data = json.load(fp)
        b = data[f"{interaction.channel_id}"]["text"]
        embed=discord.Embed(title=f"Ticket from {interaction.user}", description=f"> **Topic:** {b}")
        view = btn3()
        await chan.send(embed=embed, view=view)

class ticketbtn(discord.ui.View):
    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.green)
    async def klndsaa(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Setup Ticket", description="Write the anwsers to the ticket")
        embed.add_field(name="Channel id", value="> Please send me the channel id")
        await interaction.response.send_message(embed=embed)
        def check(m):
            return m.author == interaction.user
        chan = await client.wait_for("message", check=check)
        
        em = discord.Embed(title="Setup Ticket", description="Write the anwsers to the ticket")
        em.add_field(name="Embed topic", value="> Please send me the Embed Topic")
        await interaction.edit_original_response(embed=em)
        topic = await client.wait_for("message", check=check)
        m = discord.Embed(title="Setup Ticket", description="Write the anwsers to the ticket")
        m.add_field(name="Embed text", value="> Please send me the Embed text")
        await interaction.edit_original_response(embed=m)
        text = await client.wait_for("message", check=check)

        cha = client.get_channel(int(chan.content))
        embe = discord.Embed(title=f"{topic.content}", description=f"{text.content}") 
        view = btn2()
        a = await cha.send(embed=embe, view=view)
        with open(f"{interaction.guild.id}.json", "r") as fp:
            data = json.load(fp)
            data[f"{chan.content}"] = {}
            data[f"{chan.content}"][f"topic"] = f"{topic.content}"
            data[f"{chan.content}"][f"text"] = f"{text.content}"
            
        with open(f"{interaction.guild.id}.json", "w") as fp:
            json.dump(data, fp, indent=4)
    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.green)
    async def koiöhs(slef, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("hi")

@client.tree.command(name="setup-ticket", description="Setup the best ticket on discord")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="Ticket", description="under me are bsp for the ticket")
    embed.add_field(name="1️⃣setup ticket ", value="> React with 1️⃣ to setup ticket", inline=False)
    embed.add_field(name="2️⃣ edit ticket", value="> React with 2️⃣ to edit a ticket", inline=False)
    view = ticketbtn()
    await interaction.response.send_message(embed=embed, view=view)

@client.event
async def on_ready():
    print("Online")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

import json
@client.event
async def on_guild_join(guild):
    with open(f"{guild.id}.json", "w") as fp:
        data = ({
                "launge": "en"
            }) 
        json.dump(data, fp, indent=4)

@client.tree.command(name="purge", description="pruge")
async def clear(interaction: discord.Interaction, number : int):

    if number == None:
        await interaction.response.send_message("please add messages how i delete")
    else:
        await interaction.response.send_message(f"deleted {number}")
        await interaction.channel.purge(limit=number)


@client.tree.command(name='ban')
@commands.has_guild_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, member:discord.Member, reason:str):
    if member is None:
        return
    await member.kick(reason=reason)
    embed = discord.Embed(title='BAN', description=f'{member.mention} wurde von {interaction.user.mention} gebannt\n**Grund:** {reason}')
    await interaction.response.send_message(embed=embed)

    
@client.tree.command(name='kick')
@commands.has_guild_permissions(kick_members=True)
async def kick(interaction:discord.Interaction, member:discord.Member):
    if member is None:
        return
    await member.kick()
    embed = discord.Embed(title='KICK',description=f'{member.mention} wurde von {interaction.user.mention} gekickt')
    await interaction.response.send_message(embed=embed)

@client.tree.command(name='ping')
async def ping(interaction:discord.Interaction):
    embed = discord.Embed(title=f'🏓 Pong',description=f'**Ping:** {round(client.latency * 1000)}ms')
    await interaction.response.send_message(embed=embed)


@client.tree.command()
async def servericon(interaction:discord.Interaction):
    embed = discord.Embed()
    embed.set_image(url=interaction.guild.icon)
    await interaction.response.send_message(embed=embed)


@client.tree.command()
async def connection(interaction:discord.Interaction, member:discord.Member=None):
    if member is None:
        member = interaction.user
    if member.voice.channel is None:
        embed = discord.Embed(description=f'{member.name} ist in keinen Sprachkanal')
        await interaction.response.send_message(embed=embed)
    
        

    else:
        embed = discord.Embed(title=f'Connectioninfo of `{member}`')
        embed.add_field(name='<:832598861813776394:1043312680393519245>  Channel',value=f'>>> **{member.voice.channel.name}** {member.voice.channel.mention}')
        embed.add_field(name='<:832598861813776394:1043312680393519245> Channel-ID', value=f'>>> {member.voice.channel.id}')
        embed.add_field(name='<:832598861813776394:1043312680393519245> Members in there', value=f'`{len(member.voice.channel.members)} total Members`')
        embed.add_field(name='<:832598861813776394:1043312680393519245> Full channel?', value=f'>>> {"✅"if member.voice.channel.members is member.voice.channel.user_limit else "❌"}')
        embed.add_field(name='<:832598861813776394:1043312680393519245> Bitrate',value=f'>>> {member.voice.channel.bitrate}')
        embed.add_field(name='<:832598861813776394:1043312680393519245> User join Limit',value=f'>>> `{member.voice.channel.user_limit if member.voice.channel.user_limit else "Nicht gegeben"}`')
        await interaction.response.send_message(embed=embed)



@client.tree.command()
@commands.is_owner()
async def slowmode(interaction:discord.Interaction,channel:discord.TextChannel, seconds: int):
    if channel == None:
        channel = interaction.channel
    else:
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.message.delete()
            await interaction.response.send_message("Du brauchst dafür die Berechtigungen__**Nachrichten verwalten**__ ")
            return
        try:
            if seconds == 0:
                embed = discord.Embed(description=f'Der Slowmode wurde in {channel.mention} deaktiviert')
                await interaction.response.send_message(embed=embed)
                await interaction.channel.edit(slowmode_delay=0)
            elif seconds > 21600:
                embed = discord.Embed(description='Der Slowmode kann nicht über 6 Stunden sein')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                embed = discord.Embed(description=f"Der Slowmode wurde auf `{seconds}` Sekunden in {channel.mention} gestellt")
                await interaction.channel.edit(slowmode_delay=seconds)
                await interaction.response.send_message(embed=embed)
        except Exception:
            print()

@client.tree.command()
async def avatar(interaction:discord.Interaction, member:discord.Member=None):
    if member is None:
        member == interaction.user
    embed = discord.Embed(title=f'{member.display_name}`s Avatar')
    embed.set_image(url=member.display_avatar)
    embed.set_footer(icon_url=interaction.user.display_icon, text=f'Angefragt von {interaction.user.display_name}')
    await interaction.response.send_message(embed=embed)

@client.tree.context_menu(name='Ban ein User')
async def ban_user(interaction:discord.Interaction, member:discord.Member):
    await member.ban()
    await interaction.response.send_message(f'Du hast {member.display_name} gebannt', ephemeral=True)

@client.tree.context_menu(name='Kick ein User')
async def kick_user(interaction:discord.Interaction, member:discord.Member):
    await member.kick()
    await interaction.response.send_message(f'Du hast {member.display_name} gekickt', ephemeral=True)


@client.event
async def on_message(message):
    await client.process_commands(message)
    if client.user.mention in message.content:
        embed = discord.Embed(description=f'Hallo ich wurde von <@449393932288393216> und <@1006641097914732584> programmiert und meine cmds gehen mit:\n \t/cmdname')
        await message.channel.send(embed=embed)

@client.tree.command()
@commands.is_owner()
async def todo(interaction:discord.Interaction, message:str):
    await interaction.channel.purge(limit=1)
    embed = discord.Embed(description=message)
    await client.get_channel(1043814166110142514).send(embed=embed)
    embed=discord.Embed(description='die todo wurde in <#1043814166110142514> gesendet')
    await interaction.response.send_message(embed=embed, delete_after=5)
    await interaction.message.delete()


@client.hybrid_command()
@commands.has_guild_permissions(manage_guild=True)
async def setup_jtc(ctx: commands.Context, category: discord.CategoryChannel, channel: discord.VoiceChannel):
    await Database.setup(ctx.guild.id, category.id, channel.id)
    await ctx.send("Setup abgeschlossen")






@client.event
async def on_voice_state_update(member: discord.Member, before, after):
    cursor.execute(f"SELECT cat FROM setup WHERE gid = {member.guild.id}")
    result = cursor.fetchone()
    cursor.execute(f"SELECT chid FROM setup WHERE gid = {member.guild.id}")
    resul1 = cursor.fetchone()
    if before.channel == None:
        if after.channel.id == int(resul1[0]):
            category = discord.utils.get(member.guild.categories, id=int(result[0]))
            channel = await category.create_voice_channel(name=member.name)
            await member.move_to(channel)
            await member.voice.channel.set_permissions(member, manage_channels=True, manage_permissions=True)

            def check(x, y, z):
                return len(channel.members) == 0

            await client.wait_for('voice_state_update', check=check)
            await channel.delete(reason="TempVoice ist leer")



@client.hybrid_command()
async def ghost(ctx):
    voice_state = ctx.author.voice

    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')


    else:
        await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        embed = discord.Embed(description=f"{ctx.author.voice.channel.mention} ist nun privat")
        await ctx.send(embed=embed)


@client.hybrid_command()
async def unghost(ctx):
    voice_state = ctx.author.voice

    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')


    else:
        await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, view_channel=True)
        embed=discord.Embed(description=f"{ctx.author.voice.channel.name} ist nun öffentlich")
        await ctx.send(embed=embed)



@client.hybrid_command()
async def allow_role(ctx,role:discord.Role):
    voice_state = ctx.author.voice

    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')


    else:
        await ctx.author.voice.channel.set_permissions(role, view_channel=True)
        embed=discord.Embed(description=f"{ctx.author.voice.channel.mention} ist nun für {role} öffentlich")
        await ctx.send(embed=embed)


@client.hybrid_command()
async def deny_role(ctx,role:discord.Role):
    voice_state = ctx.author.voice

    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')


    else:
        await ctx.author.voice.channel.set_permissions(role, view_channel=False)
        embed = discord.Embed(description=f"{ctx.author.voice.channel.mention} ist nun für {role} nicht mehr öffentlich")
        await ctx.send(embed=embed)



@client.hybrid_command()
async def delete_jtc(ctx: commands.Context):
    cursor.execute(f"DELETE FROM setup WHERE gid = {ctx.guild.id}")
    embed=discord.Embed(description="Alle Setups wurden gelöscht")
    await ctx.send(embed=embed)

class Database:
    @staticmethod
    async def execute(operation: tuple, target: str = None):
        with conn:
            cursor.execute(operation[0], operation[1])
        if target:
            a = cursor.fetchone()
            try:
                return a[target]
            except TypeError:
                return None

    @staticmethod
    async def setup(gid: int, category: int, chid: int):
        await Database.execute(("INSERT OR REPLACE INTO setup VALUES (:gid, :category, :chid)", {"gid": gid, "category": category, "chid": chid}))

@client.hybrid_command()
async def voice_name(ctx,*,voicename):
    voice_state = ctx.author.voice
    channel:discord.VoiceChannel
    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')


    else:
        await ctx.author.voice.channel.edit(name=voicename)
        embed = discord.Embed(description=f'Der Sprachkanal wurde zu **{voicename}** geändert')
        await ctx.send(embed=embed, delete_after=5)




@client.hybrid_command()
async def voice_limit(ctx,*,voice_limit):
    voice_state = ctx.author.voice
    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('Du musst in einen Sprachkanal sein')

    else:
        await ctx.author.voice.channel.edit(user_limit=voice_limit)
        embed = discord.Embed(description=f"{ctx.author.voice.channel.mention} ist nun beschränkt auf `{voice_limit}` Benutzer")
        await ctx.send(embed=embed)

@client.hybrid_command()
async def emptest(ctx):

    with conn:
        cursor.execute("SELECT gid, cat, chid FROM setup")
        emp_list = cursor.fetchall()

    for j in range(0):
        column = []
        for i in range(0):
            column += emp_list
        column += "\n"
        emp_list += column
    for column in emp_list:
       for item in column:
           info = print(item, end=" ")
           print()
    await ctx.send(emp_list)


@client.hybrid_command()
async def servers(ctx):
    
    with conn:
        cursor.execute("SELECT gid, cat, chid FROM setup")
        emp_list = cursor.fetchall()

    for j in range(0):
        column = []
        for i in range(0):
            column += emp_list
        column += "\n"
        emp_list += column
    for column in emp_list:
       for item in column:
           print(item, end=" ")
           print()
    msg = '{!s:19s} | {!s:19s} | {!s:19s}\n'.format('GID', 'Kategorie', 'CHID')
    embed = discord.Embed(description=f'{msg}\n{emp_list}')
    await ctx.send(embed=embed)


client.run("MTA0MzgzODU0NDE4MDk1MzEyOA.Gg0dXY.23o3igjag-gR_iJdsdoUcNpJdOjAA364xS35jM")