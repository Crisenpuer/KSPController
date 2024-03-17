import discord, os, psutil, platform, Misc, KSP
import discord.app_commands as app_commands
from Misc import OLDlog, log

MY_GUILD = discord.Object(id=KSP.GUILD_ID)  # replace with your guild id

tn = None
ksp = None

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    OLDlog(client.user.name,f"(ID: {client.user.id}) zaOLDlogowany! Zglaszam gotowość!")
    print('----------------------------------------------------------------------------------------------------')
    channel = client.get_channel(1218548556147851325)
    if channel is not None:
        await channel.send('Bot is ready!')
    else:
        OLDlog(client.user.name,"ERROR Starting channel is None")
    global ksp
    global tn
    ksp = KSP.check_ksp_status()
    if not ksp:
        tn = None

@client.tree.command()
async def selfdestruct(interaction: discord.Integration):
    """Shutdown bot and KSP (WARNING!!! There will be no way to start the bot after running this command!)"""
    OLDlog(client.user.name,'/selfdestruct', 2)
    await interaction.response.send_message("Shutting down KSP and bot...")
    Misc.start_ksp()
    await client.close()

@client.tree.command()
async def status(interaction: discord.Integration):
    """Status"""
    OLDlog(client.user.name,'/status', 1)
    Misc.status()
@client.tree.command()
async def restart(interaction: discord.Integration):
    """Restart bot"""
    log('/restart', client.user.name, 1)
    await interaction.response.send_message("Restarting the bot...")
    
    KSP.restart()
    
@client.tree.command()
async def startksp(interaction: discord.Integration):
    """Start KSP"""
    temp = KSP.startgame()
    if temp:
        await interaction.user.send("Attempting to start KSP...")
    else:
        await interaction.user.send("KSP is already running...")

@client.tree.command()
async def closeksp(interaction: discord.Integration):
    """Close KSP"""
    log("/closeksp", client.user.name, 1)
    await interaction.response.send_message("Attempting to close KSP...")
    KSP.close_ksp()

if __name__ == "__main__":
    os.system('cls')
    client.run(KSP.TOKEN)