import discord
import asyncio
import random
from random import randint
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

    if message.content.startswith('t!gif'):
     args = message.content.split(" ")
     del args[0]
     buscar = ' '.join(args)
     cantidad = canti(buscar)
     msg = await client.send_message(message.channel, mostrar(buscar,0))
     await client.add_reaction(msg, '🔃')
     
     while True:
         def check(reaction, user):
            if reaction.count != 1 and reaction.emoji == '🔃':
                return 1
            return 0
         res = await client.wait_for_reaction(message=msg, check=check)
         if '{0.reaction.emoji}'.format(res) == '🔃':
          ran = randint(0,cantidad-1)
          await client.edit_message(msg, mostrar(buscar,ran))
          await client.clear_reactions(msg)
          await client.add_reaction(msg, '🔃')
          
    if message.content.startswith('t!creategif'):
     print('---ENTRA AL ELIF---')
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     del args[0]
     tags = ' '.join(args)
     await client.send_message(message.channel, meter(url,tags))

        
def mostrar(buscar,num):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT url FROM giftable where tag like \'%%%s%%\'""", (AsIs(buscar),))
     rows = cur.fetchall()
     resultado = rows[num][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def meter(url, tags):
    print('---ENTRA A LA FUNCION METER---')
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""INSERT INTO giftable (url, tag) VALUES (\"%s\", \"%s\");""", (AsIs(url),AsIs(tags),))
     rows = cur.fetchall()
     resultado = "Se ha introducido el gif adecuadamente"
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    


    
def canti(buscar):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT url FROM giftable where tag like \'%%%s%%\'""", (AsIs(buscar),))
     rows = cur.fetchall()
     resultado = len(rows)
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

client.run(os.environ.get('BOT_TOKEN'))

