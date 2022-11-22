import asyncio
from cProfile import label
from turtle import title
from discord import Member
import discord
from discord.ext import commands
from discord.ui import Button, View
import discord.ui
import random
from time import sleep
import json

import youtube_dl
import os
from discord import Embed

from datetime import datetime
from colorama import Back, Fore, Style
import datetime
import platform
import time
from discord import app_commands

client = commands.Bot(intents=discord.Intents.all(),command_prefix='!!')
client.remove_command("help")


@client.tree.command(name="say")
@app_commands.describe(title='Title', description="Description")
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
@app_commands.describe(number='messages')
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


client.run("MTA0MzgzODU0NDE4MDk1MzEyOA.Gm-tpo.NUiUkG6VnBC0omzDf0niqic4JxWojUQztcD9R4")