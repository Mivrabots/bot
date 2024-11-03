import discord
from discord.ext import commands
from keep_alive import keep_alive
keep_alive()
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

token = os.environ['token']

bot = commands.Bot(command_prefix=".", intents=intents)

#roles that can warn by the role id
warning_roles = [1301691322532364362, 1301691322532364363, 1301691322532364364, 1301691322532364365, 1301691322532364366, 1301691322532364367, 1301691322574442560, 1302025511169687673, 1301691322566180915, 1301691322566180914, 1301691322566180914, 1301691322566180913]

ban_roles = [1301691322574442560, 1302025511169687673, 1301691322574442559, 1301691322566180915, 1301691322532364364, 1301691322532364365, 1301691322532364366, 1301691322532364367,]

kick_roles = [1301691322532364363, 1301691322532364364, 1301691322532364365, 1301691322532364366, 1301691322532364367, 1302692653925928960, 1302025511169687673, 1301691322566180915]

developers_roles = [1301691322343755814, 1301691322389893246]

log_channel = 1302688575774789714

owner_id = 1258620191890341921

#ban message
ban_message = "You have been banned from the server. If you think this is a mistake, please contact a server administrator."

#kick message
kick_message = "You have been kicked from the server. If you think this is a mistake, please contact a server administrator."

#warn message
warn_message = "You have been warned in the server. If you think this is a mistake, pleas contact a server administrator."

#ban command and dm they the ban message and log in THCHANNEL AS embeded message and say the reasin for banned
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if any(role.id in ban_roles for role in ctx.message.author.roles):
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned.")
        await ctx.send(ban_message)
        channel = bot.get_channel(log_channel)
        embed = discord.Embed(title="Ban", description=f"{member} has been banned by {ctx.message.author} for {reason}", color=0xff0000)
        await channel.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")

#kick command and dm them the kick message and log in THCHANNEL AS embeded message and say the
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if any(role.id in kick_roles for role in ctx.message.author.roles):
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")
        await ctx.send(kick_message)
        channel = bot.get_channel(log_channel)
        embed = discord.Embed(title="Kick", description=f"{member} has been kicked by {ctx.message.author} for {reason}", color=0xff0000)
        await channel.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")

#warn command and dm them the warn message and log in THCHANNEL AS embeded message and say the reason
@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if any(role.id in warning_roles for role in ctx.message.author.roles):
        await ctx.send(f"{member} has been warned.")
        await ctx.send(warn_message)
        channel = bot.get_channel(log_channel)
        embed = discord.Embed(title="Warn", description=f"{member} has been warned by {ctx.message.author} for {reason}", color=0xff0000)
        await channel.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")


#dev commands

#addbanrole command and add the role to the ban_roles list
@bot.command()
async def addbanrole(ctx, role: discord.Role):
    if any(role.id in developers_roles for role in ctx.message.author.roles):
        ban_roles.append(role.id)
        await ctx.send(f"{role.name} has been added to the ban roles list.")
    else:
        await ctx.send("You do not have permission to use this command.")

#addkickrole command and add the role to the kick_roles list
@bot.command()
async def addkickrole(ctx, role: discord.Role):
    if any(role.id in developers_roles for role in ctx.message.author.roles):
        kick_roles.append(role.id)
        await ctx.send(f"{role.name} has been added to the kick roles list.")
    else:
        await ctx.send("You do not have permission to use this command.")

#addwarnrole command and add the role to the warning_roles list
@bot.command()
async def addwarnrole(ctx, role: discord.Role):
    if any(role.id in developers_roles for role in ctx.message.author.roles):
        warning_roles.append(role.id)
        await ctx.send(f"{role.name} has been added to the warning roles list.")
    else:
        await ctx.send("You do not have permission to use this command.")

#rembanrole command and remove the role from the ban_roles list
@bot.command()
async def rembanrole(ctx, role: discord.Role):
    if any(role.id in developers_roles for role in ctx.message.author.roles):
        ban_roles.remove(role.id)
        await ctx.send(f"{role.name} has been removed from the ban roles list.")
    else:
        await ctx.send("You do not have permission to use this command.")


#remkickrole command and remove the role from the kick_roles list
@bot.command()
async def remkickrole(ctx, role: discord.Role):
    if any(role.id in developers_roles for role in ctx.message.author.roles):
        kick_roles.remove(role.id)
        await ctx.send(f"{role.name} has been removed from the kick roles list.")
    else:
        await ctx.send("You do not have permission to use this command.")

#owner commands 

#ownerban command and ban the member and dm the owner the log and not in a channel
@bot.command()
async def ownerban(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.id == owner_id:
        await member.ban(reason=reason)

#ownerkick command and kick the member and dm the owner the log and not in a channel
@bot.command()
async def ownerkick(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.id == owner_id:
        await member.kick(reason=reason)

#remdevrole command and remove the role from the developers_roles list
@bot.command()
async def remdevrole(ctx, role: discord.Role):
    if ctx.message.author.id == owner_id:
        developers_roles.remove(role.id)
      
#status command and change the bot status to what u want
@bot.command()
async def status(ctx, *, status):
    if ctx.message.author.id == owner_id:
        await bot.change_presence(activity=discord.Game(name=status))

                        



  





bot.run(token)