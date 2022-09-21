from discord.ext import commands
import discord
import random
from discord import Permissions

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 178838842160185344  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

# WARMUP

@bot.command()
async def name(ctx):  # When someone types !name
    await ctx.send(ctx.author) # Send the user's name

@bot.command()
async def d6(ctx): # When someone types !d6
    random.seed(random.random()) # Seed the random number generator
    await ctx.send(random.randint(1, 6)) # Send a random number between 1 and 6

@bot.event
async def on_message(message):
    if message.content == 'Salut tout le monde': # If the message is 'Salut tout le monde'
        await message.channel.send('Salut tout seul ' + message.author.mention) # Send a message back mentionning the user
    else:
        await bot.process_commands(message)

# ADMIN

@bot.command()
async def admin(ctx, user : discord.Member): # When someone types !admin @user
    if discord.utils.get(ctx.guild.roles, name="admin") == None: # If the role doesn't exist
        admin_permission=Permissions()# Create a new permission object
        admin_permission.update(manage_channels=True, kick_members=True, ban_members=True)
        await ctx.guild.create_role(name="admin", permissions=admin_permission) # Create the role
    role = discord.utils.get(ctx.guild.roles, name="admin") # Get the role
    await user.add_roles(role) # Assign the role to the user

@bot.command()
async def ban(ctx, user: discord.Member):
    await ctx.guild.ban(user) # Ban the user

@bot.command()
async def count(ctx):
    offline = 0
    online = 0
    idle = 0
    doNotDisturb = 0
    for member in ctx.guild.members: # For each member in the server
        if member.status == discord.Status.offline: # If the member is offline and so on...
            offline += 1 # Add 1 to the counter
        elif member.status == discord.Status.online:
            online += 1
        elif member.status == discord.Status.idle:
            idle += 1
        elif member.status == discord.Status.dnd:
            doNotDisturb += 1
    await ctx.send("Online: " + str(online) + "\nOffline: " + str(offline) + "\nIdle: " + str(idle) + "\nDo not disturb: " + str(doNotDisturb)) # Send the counters

# FUN AND GAMES :)

@bot.command()
async def xkcd(ctx):
    await ctx.send("https://xkcd.com/" + str(random.randint(1, 2500))) # Send a random xkcd comic (betweeen 1 and 2500)

@bot.command()
async def poll(ctx, *, question):
    await ctx.send("@here" + question)   # Mention @here and send the question
    embed = discord.Embed(               # Create an embed
        title=":bar_chart: " + question, # Set the title
        color=0x00ff00                   # Set the color
    )
    embed.set_footer(text="React to vote!") # Set the footer
    message = await ctx.send(embed=embed)   # Send the embed
    await message.add_reaction("👍")        # Add the reactions
    await message.add_reaction("👎")

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

token = ""
bot.run(token)  # Starts the bot