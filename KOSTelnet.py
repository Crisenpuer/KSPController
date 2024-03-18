import asyncio, telnetlib3
from datetime import datetime
from Misc import OLDlog, log

ping_task = None

# Function to send command to KOS Telnet server
async def send_command(reader: None, writer, command:str):
    log(command)
    # Send command to kOS telnet server
    writer.write(f"{command}\n\r")
    await writer.drain()

# Function to connect to KOS Telnet server
async def connect_to_kos(ip:str, port:int):
    now = datetime.now().strftime("%H:%M:%S")
    try:
        OLDlog('KSPTelnet', "Connecting to KOS Telnet server...")
        reader, writer = await telnetlib3.open_connection(ip, port)
        OLDlog('KSPTelnet', "Connection established", 0)
        resp = await reader.readuntil(b">")
        OLDlog('KSPTelnet', f"Response: {resp.decode(encoding='utf-8', errors='ignore')}")

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



async def send_ping(writer: telnetlib3.TelnetWriter):
    try:
        while True:
            OLDlog('KSPTelnet', "Sending PING message...", 1)
            writer.write(b"//ping")
            await writer.drain()
            await asyncio.sleep(15)  # Wait for 15 seconds before sending the next PING
    except Exception as e:
        OLDlog('KSPTelnet', "Error sending PING message:", e)


# Function to stop sending "PING" messages
async def stop_ping():
    global ping_task
    if ping_task:
        ping_task.cancel()
        ping_task = None
        log("Stopped ping","KOSTelnet",1)
    else:
        log("Not pinging already","KOSTelnet",1)

# Setting telnet terminal to XTERM
# async def set_xterm_emulation(tn):
#     # Send "IAC DO TERMINAL TYPE" (Request client's terminal type)
#     tn.sock.sendall(telnetlib.IAC + telnetlib.DO + telnetlib.TERMINAL_TYPE)
#     # Receive response from server
#     response = tn.expect([telnetlib.IAC + telnetlib.WILL + telnetlib.TERMINAL_TYPE, ], timeout=10)[2]
#     # Send "IAC SB TERMINAL-TYPE SEND IAC SE" (Client's terminal type is XTERM)
#     tn.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TERMINAL_TYPE + telnetlib.SEND + b'\x00' + telnetlib.IAC + telnetlib.SE)