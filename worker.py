import discord
import asyncio
import random
import time
import json
#from tinydb import TinyDB, Query

# INFORMATION:
# SERVER.ID: '188966409672458241'
# SERVER.NAME: 'VANDALPC'

client = discord.Client()
global bot_status
bot_status = False
bot_analisis = False


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Bot status: ' + str(bot_status))
    print('------')



@client.event
async def on_message(message):
	listen_owner_commands(message)
	
	#print(countIterable(client.messages))
	#print(message.author)
	#print(message.channel)
	#print(message.timestamp)
	messageAuthor = message.author
	messageChannel = message.channel
	messageTimestamp = message.timestamp
	#db = TinyDB('simianDB.json')
	#db.insert({'author': str(messageAuthor), 'channel': str(messageChannel), 'timestamp': str(messageTimestamp)})

	if "t!sami" in message.content:
		await client.send_typing(message.channel)
		await client.send_message(message.channel, ball8(message))

	# TESTING SHIT
	if message.author.id == '189116063806521346': # GonarcH
		#await client.send_message(message.channel, answers_for_gonarch(message))
		#logs = returnLog(message)
		#for message in logs:
		#	print('Channel: '+message.channel)
		await get_logs_from(message)
        #print(counter)
	# TESTING SHIT

	if message.author.id == '189116063806521346' and bot_status == True: # GonarcH
		await client.send_message(message.channel, answers_for_gonarch(message))
	elif message.author.id == '190402725224251402' and bot_status == True: # XxmorwullxX
		#await client.send_message(message.channel, answers_for_morwull(message))
		pass
	elif message.author.id == '121402438140821504' and bot_status == True: # Rammus
		#await client.send_message(message.channel, answers_for_rammus(message))
		pass
	elif message.author.id == '188945469479583746' and bot_status == True: # omakehell
		#await client.send_message(message.channel, answers_for_omakehell(message))
		pass
	elif message.author.id == '199229442151677952' and bot_status == True: # omakehell
		#await client.send_message(message.channel, answers_for_aldal(message))
		pass
	client.messages.clear()
	#db.close()

async def get_logs_from(me):
    async for m in client.logs_from(me.channel, limit=5000):
    	for e in m.attachments:
    		dataDump = json.dumps(e)
    		data = json.loads(dataDump)
    		#print(data['url'])
    		f = open('porn_urls.txt','a')
    		f.write('\n' + data['url'])
    		f.close()
		#f.write('\n' + 'hello world')
        #print(m.timestamp)
        #print(m.embed.url)
        #print('--------------------------------------')
        #print('--------------------------------------')

def returnLog(m):
	logs = client.logs_from(m.channel)
	return logs

def countIterable(i):
	numberOfMembers = 0
	for mem in i:
		numberOfMembers = numberOfMembers + 1
	return numberOfMembers


def ball8(m):
	"""8ball functionality with a flavour"""
	"""client.send_typing(message.channel)"""
	lcl_message = m
	random_index = 0
	answers_for_8ball_list = ['Cock',
	'Black cock para ti',
	'COCKS',
	'Pene',
	'BBC',
	'Cocktastic',
	'White cock',
	'Ass to mouth',
	'Aldal']
	random_index = random.randint(0, 8)
	print('8ball function')
	print(random_index)
	answer = answers_for_8ball_list[random_index]
	timeToWait = (len(answer)/4)
	print('ball8 time to wait value:')
	print(timeToWait)
	if timeToWait < 10:
		time.sleep(timeToWait)
	else:
		time.sleep(10)
	return answer

def answers_for_gonarch(m):
	"""This method handles the answers for user GonarcH"""
	time.sleep(1)
	lcl_message = m
	random_index = 0
	gonarch_answer_list = ['Jugando a 4K en un monitor HDReady : D',
	'Kawai',
	'o me se alguno de aqui que va de masterace y luego anda dandole caña al "FFXV a new empire".\
	Pero bueno cada uno que juegue a lo que quiera, just saying.',
	'El horizon partiendo la pana y eso que es una IP nueva.']
	random_index = random.randint(0, 3)
	print(random_index)
	return gonarch_answer_list[random_index]

def answers_for_morwull(m):
	"""This method handles the answers for user XxmorwullxX"""
	lcl_message = m
	return 'Kawai'

def answers_for_rammus(m):
	"""This method handles the answers for user Rammus"""
	lcl_message = m
	return 'Yo me se alguno de aqui que va de masterace y luego anda dandole caña al "FFXV a new empire".\
	 Pero bueno cada uno que juegue a lo que quiera, just saying.'

def answers_for_omakehell(m):
	"""This method handles the answers for user omakehell"""
	lcl_message = m
	return 'El horizon partiendo la pana y eso que es una IP nueva.'

def answers_for_aldal(m):
	"""This method handles the answers for user omakehell"""
	lcl_message = m
	return 'El horizon partiendo la pana y eso que es una IP nueva.'
			
def listen_owner_commands(m):
	"""Listens for commands only the owner can issue"""
	lcl_message = m
	global bot_status
	if lcl_message.author.id == '189116063806521346': # GonarcH
		if lcl_message.content == 'put yourself away':
			bot_status = False
			#await client.send_message(message.channel, '[ENTERING SLEEP MODE]')
			print('[ENTERING SLEEP MODE]')
		elif lcl_message.content == 'bring yourself back online':
			bot_status = True
			#await client.send_message(message.channel, '[LEAVING SLEEP MODE]')
			print('[LEAVING SLEEP MODE]')

def printServerInfoToConsole():
	"""Print Server Info to console"""
	for n in client.servers:
		print('server.name: ' + n.name)
		print('server.id: ' + n.id)			
				

# Returns True if the user is online
def isUserOnline(u):
	if u.status.name == 'online':
		return True
	else:
		return False


# Get ALL users/members of the server
def printAllUsersToConsole(c):
	usuarios = c.get_all_members()
	for n in usuarios:
		#print(n.status.name)
		print('User Name: ' + n.name)
		print('User Id: ' + n.id)
		print('-----------------------------')
	

    client.run(<process.env.BOT_TOKEN>)