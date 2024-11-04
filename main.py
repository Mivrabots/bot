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

@bot.command(name="ban")
async def ban(ctx, user: discord.User, *, reason=None):
            guild = ctx.guild
            author = ctx.author

            # Check if the user has one of the allowed roles
            if not any(role.id in ban_roles for role in author.roles):
                await ctx.send("You do not have permission to use this command.")
                return

            try:
                # Fetch the member and proceed with banning
                member = await guild.fetch_member(user.id)

                # Ban the member
                await guild.ban(member, reason=reason)

                # DM the user about the ban
                dm_message = f"You have been banned from {guild.name}."
                if reason:
                    dm_message += f"\nReason: {reason}"
                try:
                    await user.send(dm_message)
                except discord.Forbidden:
                    await ctx.send("Unable to DM the user. They may have DMs disabled.")

                # Log the ban in a specific channel
                log_channel = discord.utils.get(guild.text_channels, name="THCHANNEL")  # Replace with your log channel's name
                if log_channel:
                    embed = discord.Embed(title="User Banned", color=discord.Color.red())
                    embed.add_field(name="User", value=f"{user} (ID: {user.id})", inline=False)
                    embed.add_field(name="Banned by", value=ctx.author.mention, inline=False)
                    if reason:
                        embed.add_field(name="Reason", value=reason, inline=False)
                    await log_channel.send(embed=embed)
                await ctx.send(f"{user} has been banned.")

            except discord.NotFound:
                await ctx.send("User not found.")
            except discord.Forbidden:
                await ctx.send("I do not have permission to ban this user.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

        # Error handling for missing permissions or arguments
@ban.error
async def ban_error(ctx, error):
            if isinstance(error, commands.MissingPermissions):
                await ctx.send("You don't have permission to ban members.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Please mention the user or provide their ID, and a reason if needed.")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("Invalid user. Please mention a valid user or provide their ID.")

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
