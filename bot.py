import discord
from discord.ext import commands
import config
import asyncio
import logging
import os
import aiohttp

handler = logging.FileHandler(filename='chatgptlite.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level=logging.DEBUG, handler=handler, root=False)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=config.ext, intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'\nLogged as: {bot.user.name} - {bot.user.id}\nConnected to:')
    for i in bot.guilds:
        print(
        f'{i}'
        )
    print(f'Bot is ready to go!') 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='chat gpt'))

@bot.command(hidden=True)
async def status(ctx, arg, arg2, arg3=None):
    author = ctx.message.author
    if author.id == 626811868249325578:
        if arg == 'playing':
            await bot.change_presence(activity=discord.Game(name=arg2))
        elif arg == 'streaming':
            await bot.change_presence(activity=discord.Streaming(name=arg2, url=arg3))
        elif arg == 'listening':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg2))
        elif arg == 'watching':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg2))
        await ctx.send('Status Updated')
        await ctx.channel.purge(limit=2)
        print('Status Updated')
    else:
        await ctx.send('Fuck off. You are not authorized')



@bot.command(hidden=True)
async def gpt(ctx: commands.context, *, prompt: str):
    async with aiohttp.ClientSession() as session:
        payload={
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 50,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "best_off": 1,
        }
        headers = {"Authorization": f"Bearer {config.api}"}
        async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
            response = await resp.json()
            embed = discord.Embed(title="Chat Gpt Lite Response:", description=response["choices"][0]["text"])
            await ctx.reply(embed=embed)

async def main():
    async with bot:
        await bot.start(config.token, reconnect=True)

asyncio.run(main())
