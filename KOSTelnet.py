import asyncio
from datetime import datetime
from Misc import OLDlog

# Function to send command to KOS Telnet server
async def send_command(reader, writer, command):
    now = datetime.now().strftime("%H:%M:%S")
    try:
        if reader and writer:
            OLDlog('KSPTelnet', "Sending command...")
            writer.write(command.encode() + b"\r\n")
            await writer.drain()
            OLDlog('KSPTelnet', "Command sent:", command)

            # Read the response (if needed)
            response = await reader.readuntil(b">")  # Adjust termination string as needed
            OLDlog('KSPTelnet', "Response:", response.decode())
        else:
            OLDlog('KSPTelnet', "Not connected to KOS Telnet server")
    except Exception as e:
        print("[KSPTelnet] Error:", e)

# Function to connect to KOS Telnet server
async def connect_to_kos(ip, port):
    now = datetime.now().strftime("%H:%M:%S")
    try:
        OLDlog('KSPTelnet', "Connecting to KOS Telnet server...")
        reader, writer = await asyncio.open_connection(ip, port)
        OLDlog('KSPTelnet', "Connection established", 0)
        return reader, writer
    except ConnectionRefusedError:
        OLDlog('KSPTelnet', "Connection error: Connection refused")
        return None, None
    
# Function to disconnect from KOS Telnet server
async def disconnect_from_kos(reader, writer):
    now = datetime.now().strftime("%H:%M:%S")
    try:
        if reader and writer:
            OLDlog('KSPTelnet', "Disconnecting from KOS Telnet server...")
            writer.close()
            await writer.wait_closed()
            OLDlog('KSPTelnet', "Connection closed")
        else:
            OLDlog('KSPTelnet', "Not connected to KOS Telnet server")
    except Exception as e:
        OLDlog('KSPTelnet', "Error:", e)

async def send_ping(writer):
    try:
        while True:
            OLDlog('KSPTelnet', "Sending PING message...", 1)
            writer.write(b"")
            await writer.drain()
            await asyncio.sleep(30)  # Wait for 30 seconds before sending the next PING
    except Exception as e:
        OLDlog('KSPTelnet', "Error sending PING message:", e)



# paste this to main botv2 script please!
async def start_ping(ctx):
    global ping_task
    global writer
    if ping_task is None:
        ping_task = asyncio.create_task(send_ping(writer))
        await ctx.send("Started sending PING messages")
    else:
        await ctx.send("Already sending PING messages")

# Function to stop sending "PING" messages
async def stop_ping(ctx):
    global ping_task
    if ping_task:
        ping_task.cancel()
        ping_task = None
        await ctx.send("Stopped sending PING messages")
    else:
        await ctx.send("Not sending PING messages")


# Setting telnet terminal to XTERM
# async def set_xterm_emulation(tn):
#     # Send "IAC DO TERMINAL TYPE" (Request client's terminal type)
#     tn.sock.sendall(telnetlib.IAC + telnetlib.DO + telnetlib.TERMINAL_TYPE)
#     # Receive response from server
#     response = tn.expect([telnetlib.IAC + telnetlib.WILL + telnetlib.TERMINAL_TYPE, ], timeout=10)[2]
#     # Send "IAC SB TERMINAL-TYPE SEND IAC SE" (Client's terminal type is XTERM)
#     tn.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TERMINAL_TYPE + telnetlib.SEND + b'\x00' + telnetlib.IAC + telnetlib.SE)