import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '$', intents = intents)

channel_user_log = # insert channel ID here for auto-join channel
channel_banned_usernames = # insert channel ID here containing a list of messages for all usernames to ban
guild_id = # insert server ID here

@bot.command()
async def banusers(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        return

    if ctx.guild.id == guild_id:

        search_terms = []
        for channel in ctx.guild.channels:
            if (channel.id == channel_banned_usernames):
                messages = await channel.history(limit=200).flatten()
                for message in messages:
                    search_terms.append(message.content.lower())

        for term in search_terms:
            for member in ctx.guild.members:
                if (term in member.name.lower()):
                    print("Banning: " + member.name.lower())
                    await member.ban(reason = "Unallowed Username")

        # wait for tatsumaki to write join / leave messages
        await asyncio.sleep(5)

        # purge messages in member log
        for channel in ctx.guild.channels:
            if (channel.id == channel_user_log):
                to_delete = []
                messages = await channel.history(limit=200).flatten()
                for message in messages:
                    for term in search_terms:
                        if term in message.content.lower():
                            to_delete.append(message)
                            continue
                    
                    for member in message.mentions:
                        for term in search_terms:
                            if term in member.name.lower():
                                to_delete.append(message)

                await channel.delete_messages(to_delete)
                break
    
    await ctx.message.delete()

@bot.event
async def on_member_join(member):
    if member.guild.id == guild_id:

        search_terms = []
        for channel in member.guild.channels:
            if (channel.id == channel_banned_usernames):
                messages = await channel.history(limit=200).flatten()
                for message in messages:
                    search_terms.append(message.content.lower())

        print("user: " + str(member.name) + " joined!")

        banned = False

        for term in search_terms:
            if term in member.name.lower():
                print("Banning user: " + str(member.name))
                banned = True
                await member.ban(reason = "Unallowed Username")
                break

        if banned == True:

            # wait for tatsumaki to write join / leave messages
            await asyncio.sleep(5)

            # purge
            for channel in member.guild.channels:
                if (channel.id == channel_user_log):
                    to_delete = []
                    messages = await channel.history(limit=200).flatten()
                    for message in messages:
                        if (term in message.content.lower()):
                            to_delete.append(message)
                            continue
                        for member in message.mentions:
                            if (term in member.name.lower()):
                                to_delete.append(message)

                    await channel.delete_messages(to_delete)
                    return

@bot.event
async def on_ready():
    print("Bot online")

token = #insert token here
bot.run(token)
