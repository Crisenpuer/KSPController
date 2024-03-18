import KSP, os, sys, KOSTelnet, time, Misc, subprocess, asyncio
from twitchio.ext import commands
from Misc import log, get_dotenv

# Get env vars
env = get_dotenv()

# Twitch application credentials
TOKEN = env["TW_TOKEN"]

# Global variables
reader = None
writer = None
ping_task = None

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, prefix='?', initial_channels=["crisenpuer",env["TW_CHANNEL"]])

    async def event_ready(self):
        log(f'Logged in as | {self.nick}',"TwitchChatBot",1)
        log(f'User id is | {self.user_id}',"TwitchChatBot",1)
        time.sleep(0.5)
        global reader, writer
        reader, writer = await KOSTelnet.connect_to_kos("127.0.0.1", 5410)
        time.sleep(1)
        await KOSTelnet.send_command(reader,writer,f"1\n'")
        time.sleep(1)
        await KOSTelnet.send_command(reader,writer,'core:doevent("open terminal").')
        await KOSTelnet.send_command(reader,writer,'set terminal:charheight to 20.')
        await KOSTelnet.send_command(reader,writer,'set terminal:width to 40.')
        await KOSTelnet.send_command(reader,writer,'set terminal:height to 32.')
        await start_ping()

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong {ctx.author.name}! Use ?help if you need any :)')

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(f'Hi! Im a bot created by Crisenpuer (and also his alt account LUL ) Use ?whaticando to list my commands!')

    @commands.command()
    async def whaticando(self, ctx: commands.Context):
        await ctx.send(f'Standard: ?ping, ?help, ?whaticando, ?reconnect, ?cpu, ?cmd, ?rickroll, ?status, ?runscipt')
        await ctx.send(f'Mod-only: ?reboot, ?killksp ?startksp')

    @commands.command()
    async def reboot(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await ctx.send(f'Rebooting the bot...')
            global reader, writer
            writer.close()
            reader = None
            writer = None
            os.chdir("D:\\Python\\KSPController")
            python = sys.executable
            subprocess.Popen([python, sys.argv[0]])
            await self.close()
            sys.exit()
        else:
            await ctx.send("You dont have permission to use this command")

    @commands.command()
    async def killksp(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await ctx.send("Attempting to kill KSP...")
            KSP.killgame()
        else:
            await ctx.send("You dont have permission to use this command")

    @commands.command()
    async def startksp(self, ctx: commands.Context):
        if ctx.author.is_mod:
            sg = KSP.startgame()
            if sg:
                await ctx.send("Attempting to start KSP...")
            else:
                await ctx.send("KSP is already running")
        else:
            await ctx.send("You dont have permission to use this command")

    @commands.command()
    async def reconnect(self, ctx: commands.Context):
        global reader, writer
        writer.close()
        reader = None
        writer = None
        await ctx.send("Reconnecting to kOS...")
        reader, writer = await KOSTelnet.connect_to_kos("127.0.0.1", 5410)
        await start_ping()

    @commands.command()
    async def cpu(self, ctx: commands.Context, cpu_id:int):
        global reader, writer
        if isinstance(cpu_id, int):
            if reader == None or writer == None:
                log("Command not sent: Bot is not connected to kOS", "ChatBot", 1)
                await ctx.send("Bot is not connected to kOS, use ?reconnect")
            else:
                log(f"Changing CPU to #{cpu_id}", 'ChatBot', 1)
                await KOSTelnet.send_command(reader,writer,'core:doevent("close terminal").')
                writer.write('^D\n')
                await writer.drain()
                time.sleep(1)
                await KOSTelnet.send_command(reader,writer,f"{cpu_id}\n")
                time.sleep(1)
                await KOSTelnet.send_command(reader,writer,'core:doevent("open terminal").')
                await KOSTelnet.send_command(reader,writer,'set terminal:charheight to 20.')
                await KOSTelnet.send_command(reader,writer,'set terminal:width to 40.')
                await KOSTelnet.send_command(reader,writer,'set terminal:height to 32.')
        else:
            log(f"cpu_id({cpu_id}) is not an int")
            await ctx.send(f"{cpu_id} is not a number")
    
    @commands.command()
    async def det(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await KOSTelnet.send_command(reader,writer,'\x1a\n')
        else:
            await ctx.send("You dont have permission to use this command")
    
    @commands.command()
    async def cmd(self, ctx: commands.Context, command: str):
        global reader, writer
        if reader == None or writer == None:
            await ctx.send("Bot is not connected to kOS, use ?reconnect")
        else:
            await KOSTelnet.send_command(reader, writer, f"{command} // {ctx.author.display_name}")

    @commands.command()
    async def rickroll(self, ctx :commands.Context):
        await ctx.send("Never gonna give you up")
        time.sleep(1)
        await ctx.send("Never gonna let you down")
        time.sleep(1)
        await ctx.send("Never gonna run around and desert you")
        time.sleep(1)
        await ctx.send("Never gonna make you cry")
        time.sleep(1)
        await ctx.send("Never gonna say goodbye")
        time.sleep(1)
        await ctx.send("Never gonna tell a lie and hurt you")

    @commands.command()
    async def status(self, ctx :commands.Context, mode="multi"):
        sts = Misc.status()
        if mode == "single":
            await ctx.send(f"CPU:  {sts[0]}% | RAM:  {sts[1]}MB / {sts[2]}MB")
        else:
            await ctx.send(f"CPU:  {sts[0]}%")
            await ctx.send(f"RAM:  {sts[1]}MB / {sts[2]}MB")

    @commands.command()
    async def runscript(self, ctx :commands.Context, id):
        code, url = Misc.read_from_pastebin(id)
        if code == None:
            ctx.send("Paste not found")
        else:
            global reader, writer
            if reader == None or writer == None:
                await ctx.send("Bot is not connected to kOS, use ?reconnect")
            else:
                await ctx.send(f"Running code from {url}")
                await KOSTelnet.send_command(reader, writer, f"{code} // {ctx.author.display_name}")





async def send_ping():
    global writer
    try:
        while True:
            log("Sending PING message...", 'ChatBot', 1)
            writer.write("\n\r")
            await writer.drain()
            await asyncio.sleep(15)  # Wait for 15 seconds before sending the next PING
    except Exception as e:
        log(f"Error sending PING message: {e}", 'ChatBot', 1)

# paste this to main botv2 script please!
async def start_ping():
    global ping_task
    if ping_task is None:
        ping_task = asyncio.create_task(send_ping())
        log("Started sending PING messages","KOSTelnet",1)
    else:
        log("Already pinging","KOSTelnet",1)

if __name__ == "__main__":
    os.system('cls')
    bot = Bot()
    bot.run()