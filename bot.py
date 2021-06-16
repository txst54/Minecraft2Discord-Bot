import os

# import aiohttp
import discord # pip install discord
from dotenv import load_dotenv # pip install python-dotenv
import screenutils as sc # pip install screenutils
from pyngrok import ngrok # pip install pyngrok

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
mc_player_list = os.getenv('MC_PLAYER_LIST')
# discord_ids = os.getenv('DISCORD_IDS')
mc = mc_player_list.split(',')
# ds = discord_ids.split(',')
# uuids = dict(zip(mc, ds))
@client.event
async def on_ready():
	ip_log = client.get_channel(int(os.getenv('IP_LOG')))
	wormhole = client.get_channel(int(os.getenv('WORMHOLE')))
	print(f"{client.user} has connected to discord!")
	print("Initializing Screens")
	server = sc.Screen('server')
	if(server.exists):
		server.enable_logs()
		print('Server session already exists')
		
	else:
		print('Server session does not exist, initializing...')
		server.initialize()
		server.enable_logs()
		server.send_commands('cd ../server') # change path to path of the server file
		server.send_commands('./run.bat') # change the bat/sh file to whatever bat/sh file starts the server
		for f in server.logs:
			if("help" in f):
				break
			if len(f) > 1:
				print(f)
	print('Done initializing server')
	ip = ngrok.connect(25565, "tcp")
	await ip_log.send(ip) # sends IP in the IP Logs Channel
	print('Done initializing NGROK')
	print(f"Running Screens:{sc.list_screens()}") # output should be at least 1 screen and one of the screens should be called server. Depends on how many other screen sessions you are running. 
	while True:
		for line in server.logs:
			status = [x for x in mc if('<'+x+'>' in line)]
			if bool(status):
				content = line.split('<'+status[0]+'>')[1][:-4]
				# sender = await client.fetch_user(uuids[status[0]])
				await wormhole.send(status[0]+": "+content)
client.run(TOKEN)
