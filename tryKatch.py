import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()

TOKEN = os.getenv('TOKEN')
print(TOKEN)

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('.'))
    print('Logged on as {0.user}!'.format(client))

@client.event
async def on_member_join(member):
    print('{member} has joined a server.'.format(member))

@client.event
async def on_member_remove(member):
    print('{member} has left a server.'.format(member))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
        
# @client.event
# async def on_message(message):
#     print('Message from {0.author}: {0.content}'.format(message))
#     if message.author == client.user:
#         return
#     if message.content.startswith('.hello'):
#         await message.channel.send('Hello')
        

@client.command()
async def ping(ctx):
    """Return ping in ms"""
    lat = round(client.latency*1000)
    await ctx.send('{} ms'.format(lat))

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    """Clear specified last messages default is 5"""
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    """Kick a user"""
    await member.kick(reason=reason)
    await ctx.send('Kicked {}'.format(member.mention))

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    """Ban a user"""
    await member.ban(reason=reason)
    await ctx.send('Banned {}'.format(member.mention))

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    """Unban a user"""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator == member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send('Unbanned {}'.format(user.mention))
            return

@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@client.command()
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@client.command(aliases=['random'])
async def member(ctx):
    """Select random member from the server"""
    users = ctx.guild.members
    user = random.choice(users)
    await ctx.send(user)

client.run(TOKEN)
