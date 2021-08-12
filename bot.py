# bot.py
# coding=utf8
import os
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from anime_queries import search_anime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
courses = {}


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name="?help for usage!"))


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if '?' == message.content[0]:
        done = str(message.content).find(' ')
        if message.content[1:] == 'help':
            await message.channel.send("There's only one command: `?anime <anime name>`")

        elif message.content[1:done] == 'anime':
            # https://myanimelist.net/search/all?q=<QUERY>&cat=all

            message_content = str(message.content[done + 1:])
            message_author = message.author.mention

            # Grab anime info
            anime_raw = search_anime(message_content)

            anime_title = anime_raw.name
            anime_eng_title = anime_raw.eng_name
            anime_score = anime_raw.score
            anime_cover = anime_raw.get_cover()
            anime_episode_list = anime_raw.get_gogo_urls()

            # Grab formatted description

            page = requests.get(anime_raw.get_mal_url())
            soup = BeautifulSoup(page.content, 'html.parser')

            anime_summary = soup.find(itemprop='description').text
            if len(anime_summary) > 1024:
                anime_summary = anime_summary[:1020] + '...'

            # Embed to send
            anime_info = discord.Embed(title='MAL Lookup',
                                       description=f"{message_author} requested \"{message_content}\"",
                                       color=0x2E51A2)
            anime_info.set_thumbnail(url=anime_cover)

            # Depending on if there are two names:
            if anime_eng_title is not None:
                anime_info.add_field(name='Information',
                                     value=f'**Name**:\t{anime_title}\n**English Name:**\t{anime_eng_title}\n**Score:**\t{anime_score}',
                                     inline=False)
            else:
                anime_info.add_field(name='Information',
                                     value=f'**Name**:\t{anime_title}\n**Score:**\t{anime_score}',
                                     inline=False)

            # Add the description to the embed
            anime_info.add_field(name='Description',
                                 value=anime_summary,
                                 inline=False)

            # Grab episode links and add them
            if not anime_raw.is_airing():
                if anime_raw.episodes > 5:
                    for i in range(1, 6):
                        anime_info.add_field(name=f'Episode {i}',
                                             value=f'Click [here]({anime_episode_list[i]}) to watch',
                                             inline=False)
                    anime_info.add_field(name=f'Episodes 6 - {anime_raw.episodes}',
                                         value=f'Click [here](https://www1.gogoanime.ai/category/{anime_episode_list[1][26:-10]}) for more',
                                         inline=False)
                else:
                    for i in range(1, anime_raw.episodes + 1):
                        anime_info.add_field(name=f'Episode {i}',
                                             value=f'Click [here]({anime_episode_list[i]}) to watch',
                                             inline=False)
            else:
                anime_info.add_field(name=f'Episodes',
                                     value=f'{anime_title} is still airing, but episodes can be found [here]({anime_episode_list[1]})',
                                     inline=False)

            anime_info.set_footer(text="Mirubot by Buu",
                                  icon_url='https://cdn.discordapp.com/avatars/193836796411510785/a675c14482b550350be00604ba030701.webp?size=128')

            await message.channel.send(embed=anime_info)


client.run(TOKEN)
