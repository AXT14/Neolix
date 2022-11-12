import discord
import os
import keep_alive
import random
from discord.ext import commands

npx = commands.Bot(command_prefix = '-')
npx.sniped_messages = {}
npx.remove_command("help")

@npx.event
async def on_ready():
   await npx.change_presence(activity = discord.Streaming(name = "-Help", url = "https://www.twitch.tv/nexuspr1mex"))
   print('NEXUS PR1ME X Is Online!')

@npx.event
async def on_message_delete(message):
  npx.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@npx.command(aliases = ['snipe', 'SNIPE'])
async def Snipe(ctx):
  contents, author, channel_name, time = npx.sniped_messages[ctx.guild.id]

  embed = discord.Embed(description=contents, color=discord.Color.green(), timestamp=time)
  embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
  embed.set_footer(text=f"Deleted In : #{channel_name}")
  
  await ctx.channel.send(embed=embed)

@npx.command(aliases = ['ping', 'PING'])
async def Ping(ctx):
 await ctx.send(f'Pong! - {round(npx.latency * 1000)} ms')

@npx.command(aliases = ['unban', 'UNBAN'])
@commands.has_permissions(ban_members=True)
async def Unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned {user.mention}")

@npx.command(aliases = ['hello', 'hi', 'Hi', 'HELLO', 'HI'])
async def Hello(ctx):
 await ctx.send("Hello! Im NEXUS PR1ME X")

@npx.command(aliases=['8ball', '8Ball', '8BALL'])
async def eightball(ctx, *,quetion):
     responses  = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Maybe."]

     await ctx.send(f':8ball: Answer: {random.choice(responses)}')

@npx.command(aliases=['Say', 'SAY'])
async def say(ctx, saymsg = None):
    if saymsg == None:
         return await ctx.send('You Must Tell Me a Message!')
    await ctx.send(saymsg)

@npx.group(invoke_without_command = True)
async def Help(ctx):
    embed = discord.Embed(title = "Commands [v3.1]", description = ("*NEXUS PR1ME X Commands*"),color = ctx.author.color)

    embed.add_field(name = "Snipe `[-Snipe | -snipe | -SNIPE]`", value = "Snipes/Shows Deleted Message!", inline=False)    
    embed.add_field(name = "8Ball `[-eightball | -8Ball | -8BALL | -8ball]`", value = "Answers Your Questions!", inline=False)    
    embed.add_field(name = "Kick `[-Kick | -kick | -KICK]`", value = "Kicks A Member", inline=False)  
    embed.add_field(name = "Ban `[-Ban | -ban | -BAN]`", value = "Bans A Member!", inline=False)    
    embed.add_field(name = "Unban `[-Unban | -unban | -UNBAN]`", value = "Unbans A Member!", inline=False)    
    embed.add_field(name = "Hello `[-Hello | -hello | -HELLO | -hi | -Hi | -HI]`", value = "Say Hello!", inline=False)    
    embed.add_field(name = "Say `[-Say | -say | -SAY]`", value = "Say What You Command NEXUS PR1ME X To Say!", inline=False)    
    embed.add_field(name = "Help `[-Help]`", value = "Shows This Message", inline=False)    
    embed.add_field(name = "Ping`[-Ping | -ping | -PING]`", value = "Tells Bot Latency", inline=False)    
    embed.add_field(name = "Update Log `[-UpdateLog]`", value = "Tells What What Is Added In The Last Update", inline=False)    
    embed.add_field(name = "Slowmode `[-slowmode <Seconds> | -Slowmode <Seconds> | -SLOWMODE <Seconds>]`", value = "Make The Channel Slowmode!", inline=False)  
    embed.add_field(name = "Code `[-Code]`", value = "Show's The NEXUS PR1ME X Code Link!", inline=False)  

    await ctx.send(embed = embed)

@npx.group()
async def UpdateLog(ctx):
    embed = discord.Embed(title = "Update Log [v3.1 - 3.1.0]", description = ("NEXUS PR1ME X Update Log [ ' - ' is Removed, ' + ' is Added, ' * ' is Changed]"),color = ctx.author.color)

    embed.add_field(name = "+ Code Command", value = "Added `-Code` Command!", inline=False)    
    embed.add_field(name = "* Icon", value = "Changed The Icon!", inline=False)  

    await ctx.send(embed = embed)

@npx.command(aliases = ['SLOWMODE', 'Slowmode'])
async def slowmode(ctx,time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This Command Requires ``Manage Message``')
        return
    try:
        if time == 0:
            await ctx.send('Slowmode Is Off')
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            await ctx.send(f'You Cannot Set Slowmode Above 6 Hours.')
            return
        else:
             await ctx.channel.edit(slowmode_delay = time)
             await ctx.send(f'Slowmode Set To {time} seconds!')
    except Exception:
        await ctx.send('Oops!')

@npx.command(aliases = ['kick', 'KICK'])
async def Kick(ctx, member : discord.Member, *, reason=None):
        if (not ctx.author.guild_permissions.kick_members):
           await ctx.send('This Command Requires ``Kick Members``')
           return
        else:
             await member.kick(reason=reason)
             embed = discord.Embed(title = "Kick", description = (f'Kicked {member.mention}'),color = ctx.author.color)
             await ctx.send(embed = embed)

@npx.command(aliases = ['ban', 'BAN'])
async def Ban(ctx, member : discord.Member, *, reason=None):
        if (not ctx.author.guild_permissions.ban_members):
           await ctx.send('This Command Requires ``Ban Members``')
           return
        else:
             await member.ban(reason=reason)
             embed = discord.Embed(title = "Ban", description = (f'Banned {member.mention}'),color = ctx.author.color)
             await ctx.send(embed = embed)

@npx.group()
async def Code(ctx):
    embed = discord.Embed(title = "NEXUS PR1ME X Code!", description = ("NEXUS PR1ME X"),color = ctx.author.color)

    embed.add_field(name = "Code!", value = "Here Is NEXUS PR1ME X Code! https://replit.com/@EXTFT41/NEXUS-PR1ME-X#main.py", inline=False)    


    await ctx.send(embed = embed)
