import discord
import asyncio
#import os
import random
import time
import json
import asyncio
#import asyncpg
#import bd.py
import os
import psycopg2
from psycopg2.extensions import AsIs

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
    #print(countIterable(client.messages))
    #print(message.author)
    #print(message.channel)
    #print(message.timestamp)
    messageAuthor = message.author
    messageChannel = message.channel
    messageTimestamp = message.timestamp

    # BD Select 
    try:
        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        if message.content.startswith('t!botin'):
         #print("esto es message"+message.content)
         args = message.content.split(" ")
         #print("esto es args 0 con todo"+args[0])
         del args[0]
         #print("esto es args 0 sin el 0"+args[0])
         buscar = ' '.join(args)
         #print("esto es el args en buscar todo string"+buscar)
         cur=conn.cursor()
         #sql = """SELECT url FROM giftable where tag like '%%%s%%' order by random() limit 1;"""
         #params = (buscar)
         #print("esto es el select: "+sql)
         #cur.execute(sql, params)
         #cur.execute("""SELECT url FROM giftable where tag like %s order by random() limit 1;""", ('%' + buscar + '%'))
         cur.execute("""SELECT url FROM giftable where tag like \'%%%s%%\' order by random() limit 1;""", (AsIs(buscar),))
         rows = cur.fetchall()
         for row in rows:
            #await client.send_message(message.channel, row[0])
            msg = await client.send_message(message.channel, row[0])
            await client.add_reaction(msg, "::arrow_left::")
            #msg = await client.send_message(message.channel, 'React with thumbs up or thumbs down.')
            res = await client.wait_for_reaction(['👍', '👎'], message=msg)
            await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))
         cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

client.run(os.environ.get('BOT_TOKEN'))

