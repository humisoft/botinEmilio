import discord
import asyncio
import random
import time
import json
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

    #BD 
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        
        if message.content.startswith('t!botin'):
         args = message.content.split(" ")
         del args[0]
         buscar = ' '.join(args)
         cur=conn.cursor()
         cur.execute("""SELECT url FROM giftable where tag like \'%%%s%%\' order by random();""", (AsIs(buscar),))
         rows = cur.fetchall()
         #bueno#
         ###msg = await client.send_message(message.channel, rows[0][0])
         ###reac = await client.add_reaction(msg, '👍')
         ###rea = await client.wait_for_reaction(['👍'], message=reac)
         #termina bueno#
         rea = await bot.send_message(msg.message.channel,'Te gusta?')
         await bot.add_reaction(rea,'👎')
         await bot.add_reaction(rea,'👍')
         await asyncio.sleep(5)
         cache_rea = discord.utils.get(on_message, id=rea.id)
         #rea = client.get_reaction_users('👍', limit=1, after=279395402606706688)
         if cache_rea is '👍':
            rand = randint(0, 2)
            newMsg = rows[0][rand]
            print("rand : "+rand)
            print("newmsg : "+newMsg)
            edit = await client.edit_message(msg, newMsg) 
         else:
            print("no reaccion")
         #for row in rows:
            #msg = await client.send_message(message.channel, row[0])
            #await client.add_reaction(msg, 'U+27A1')
            #await client.add_reaction(msg, 'U+2B05')
            #rea = client.get_reaction_users('👍', limit=1, after=279395402606706688)
            #if rea == '👍':
            #    edit = await client.edit_message(msg, "editadooo")    
            #else:
            #    edit = await client.edit_message(msg, "noeditado")
            
         cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

client.run(os.environ.get('BOT_TOKEN'))

