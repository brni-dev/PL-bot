import discord
from discord import app_commands
from asyncio import sleep
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TOKEN = str(getenv('TOKEN'))
GUILD_ID = 1230567621884117042 # Server/Guild ID of PL (currently set to test server)
LOG_ID = "1230570080312492044" # ID of the logging channel used

def get_guild(): discord.Object(id=GUILD_ID) # i cant be bothered

@client.event
async def on_ready():
    # IMPORTANT!!!
    # TODO: Find out why the app still keeps the cleared commands and doesn't
    # properly sync the new ones which produces a "Command not found" error

    tree.clear_commands(guild=get_guild())
    print("Tree refreshed automatically")

    await sleep(15)
    print("Waited 15 seconds")

    await tree.sync(guild=get_guild())
    print("Tree synced automatically")
    
    #await tree.sync(guild=None)
    # other command for clearing the tree (i suppose?)
    # by just syncing the tree with a null guild
    # use at your own risk
    
    

@tree.context_menu(name="Report", guild=get_guild())
async def Report(interaction: discord.Interaction, message: discord.Message):
    LOG_CHANNEL = await interaction.guild.fetch_channel(LOG_ID)
    UID = message.author.id # UID of the member that wrote the reported message
    R_UID = interaction.user.id # UID of the member that reported the message
    CHANNEL_ID = interaction.channel_id # ID of the channel the reported message is in
    MSG_ID = message.id # ID of the reported message itself
    MSG_LINK = f"https://discord.com/channels/{GUILD_ID}/{CHANNEL_ID}/{MSG_ID}" # Build the link string of the reported message
    await LOG_CHANNEL.send(f"User <@!{R_UID}> reported a message sent by <@!{UID}>\n{MSG_LINK}")
    await interaction.response.send_message("Your message has been reported to the staff.", ephemeral=True)


# debug commands
"""
@tree.context_menu(name="Clear tree", guild=get_guild())
async def Tree_clear(interaction: discord.Interaction, message: discord.Message):
    tree.clear_commands(guild=get_guild())
    print("Tree refreshed manually")
    await interaction.response.send_message("The tree has been refreshed.", ephemeral=True)

@tree.context_menu(name="Sync tree", guild=get_guild())
async def Tree_sync(interaction: discord.Interaction, message: discord.Message):
    await tree.sync(guild=get_guild())
    print("Tree synced manually")
    await interaction.response.send_message("The tree has been synced.", ephemeral=True)

@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    await interaction.response.send_message("I work")
"""

client.run(TOKEN)
