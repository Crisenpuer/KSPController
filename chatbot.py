import KSP, os, sys, KOSTelnet, time, Misc, subprocess
from twitchio.ext import commands
from Misc import log, get_dotenv

# Get env vars
env = get_dotenv()

# Twitch application credentials
TOKEN = env["TW_TOKEN"]

# Global variables
reader = None
writer = None

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, prefix='?', initial_channels=["crisenpuer",env["TW_CHANNEL"]])

    async def event_ready(self):
        log(f'Logged in as | {self.nick}',"TwitchChatBot",1)
        log(f'User id is | {self.user_id}',"TwitchChatBot",1)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong {ctx.author.name}! Use ?help if you need any :)')

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(f'Hi! Im a bot created by Crisenpuer (and also his alt account LUL ) Use ?whaticando to list my commands!')

    @commands.command()
    async def whaticando(self, ctx: commands.Context):
        await ctx.send(f'?ping, ?help, ?whaticando, ?reboot, ?killksp ?startksp, ?reconnect, ?cpu, ?cmd, ?rickroll, ?status')

    @commands.command()
    async def reboot(self, ctx: commands.Context):
        await ctx.send(f'Rebooting the bot...')
        argv = sys.argv
        python = sys.executable
        await self.close()
        os.execv(python, [python] + argv)

    @commands.command()
    async def killksp(self, ctx: commands.Context):
        await ctx.send("Attempting to kill KSP...")
        KSP.killgame()

    @commands.command()
    async def startksp(self, ctx: commands.Context):
        sg = KSP.startgame()
        if sg:
            await ctx.send("Attempting to start KSP...")
        else:
            await ctx.send("KSP is already running")

    @commands.command()
    async def reconnect(self, ctx: commands.Context):
        global reader, writer
        reader, writer = await KOSTelnet.connect_to_kos("127.0.0.1", 5410)
        await ctx.send("Reconnecting to kOS...")
        await KOSTelnet.start_ping()

    @commands.command()
    async def cpu(self, ctx: commands.Context, cpu_id: int):
        global reader, writer
        if reader == None or writer == None:
            log("Command not sent: Bot is not connected to kOS", "ChatBot", 1)
            await ctx.send("Bot is not connected to kOS, use ?reconnect")
        else:
            log(f"Changing CPU to #{cpu_id}", 'ChatBot', 1)
            await KOSTelnet.send_command('\x04')
            time.sleep(0.5)
            await KOSTelnet.send_command(cpu_id)
    
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
    async def status(self, ctx :commands.Context):
        sts = Misc.status()
        raport = f"CPU:  {sts[0]}%\n     RAM:  {sts[1]}MB / {sts[2]}MB\n     Platform: {sts[3]}\n\n          KSP status: {sts[4]}\n     Telnet status: {sts[5]}"
        await ctx.send(raport)


if __name__ == "__main__":
    os.system('cls')
    bot = Bot()
    bot.run()