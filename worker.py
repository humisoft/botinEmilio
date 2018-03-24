import discord
import asyncio
import random
import time
import json
import os
import psycopg2
from psycopg2.extensions import AsIs
import pprint

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
    print('------')



@client.event
async def on_message(message):
    messageAuthor = message.author
    messageChannel = message.channel
    messageTimestamp = message.timestamp

    if message.content.startswith('t!botin'):
     args = message.content.split(" ")
     del args[0]
     buscar = ' '.join(args)
     
     msg = await client.send_message(message.channel, mensaj(buscar))
     await client.add_reaction(msg, '👍')
     await client.add_reaction(msg, '👎')
     
     def check(reaction, user):
        if reaction.count != 1:
            if reaction.emoji == '👍':
             return mensaj(buscar)
             #edit = await client.edit_message(msg, rows[0][1])
            return 1
        return 0
     res = await client.wait_for_reaction(message=msg, check=check)
     await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))

   
            
async def mensaj(buscar):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT url FROM giftable where tag like \'%%%s%%\' order by random() limit 1""", (AsIs(buscar),))
     rows = cur.fetchall()
     resultado = str(rows[0][0])
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

client.run(os.environ.get('BOT_TOKEN'))

