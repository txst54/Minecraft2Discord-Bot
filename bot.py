import os

import aiohttp
import discord
from dotenv import load_dotenv
import screenutils as sc
from pyngrok import ngrok

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
mc_player_list = os.getenv('MC_PLAYER_LIST')
discord_ids = os.getenv('DISCORD_IDS')
mc = mc_player_list.split(',')
ds = discord_ids.split(',')
uuids = dict(zip(mc, ds))
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
		server.send_commands('cd ../server')
		server.send_commands('./run.bat')
		for f in server.logs:
			if("help" in f):
				break
			if len(f) > 1:
				print(f)
	print('Done initializing server')
	ip = ngrok.connect(25565, "tcp")
	await ip_log.send(ip)
	print('Done initializing NGROK')
	print(f"Running Screens:{sc.list_screens()}")
	while True:
		i = 0
		for line in server.logs:
			status = [x for x in mc if('<'+x+'>' in line)]
			if bool(status):
				print(status)
				print(f'{status[0]} said a thing!')
				content = line.split('<'+status[0]+'>')[1][:-4]
				print(content)
				sender = await client.fetch_user(uuids[status[0]])
				print(sender.avatar)
				async with aiohttp.ClientSession() as session:
					async with session.get(str(sender.avatar_url)) as r:
						data = await r.read()
				print("Edited Bot!")
				#if(client.user.name != sender.name):
				#	await client.user.edit(username=sender.name)
				print("Bot has a name!")
				await wormhole.send(status[0]+": "+content)
				path = "sigma.PNG"
				fp = open(path, 'rb')
				pfp = fp.read()
				await client.user.edit(username="MineServer")
client.run(TOKEN)
