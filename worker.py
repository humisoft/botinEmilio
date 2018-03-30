import discord
import asyncio
import random
from random import randint
import time
import json
import os
import psycopg2
from psycopg2.extensions import AsIs
import requests
import mimetypes

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

    #MOSTRAR GIF CON REACCION
    if message.content.startswith('.gif'):
     args = message.content.split(" ")
     del args[0]
     buscar = '%\' and tag like \'%'.join(args)
     cantidad = canti(buscar)
     #em = discord.Embed(title='Gif', url=infoUrl(buscar,0), description=infoTag(buscar,0), color=0xff0000)
     #em.set_image(url=infoUrl(buscar,0))
     if infoUrl(buscar,0) or infoTag(buscar,0):
         stri =  infoUrl(buscar,0) + ' \n**' + infoTag(buscar,0) + '**'
         msg = await client.send_message(message.channel, str(stri))
         await client.add_reaction(msg, '🔃')
         while True:
             def check(reaction, user):
                if reaction.count != 1 and reaction.emoji == '🔃' and messageAuthor == user:
                    return 1
                return 0
             res = await client.wait_for_reaction(message=msg, check=check)
             if '{0.reaction.emoji}'.format(res) == '🔃':
              ran = randint(0,cantidad-1)
              #em2 = discord.Embed(title='Gif', url=infoUrl(buscar,ran), description=infoTag(buscar,ran), color=0xff0000)
              #em2.set_image(url=infoUrl(buscar,ran))
              #await client.edit_message(msg, embed=em2)
              stri = infoUrl(buscar,ran) + ' \n**' + infoTag(buscar,ran) + '**'
              await client.edit_message(msg, str(stri))
              await client.clear_reactions(msg)
              await client.add_reaction(msg, '🔃')
     else:
      await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')
    #METER GIF
    if message.content.startswith('.creategif'):
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     del args[0]
     tags = ' '.join(args)
     compo = comprobarUrl(url)
     if compo != None:
      await client.send_message(message.channel, ':octagonal_sign:ESTE GIF YA ESTA EN LA BASE DE DATOS:octagonal_sign:')
     else:
      meter(url,tags)
      await client.delete_message(message)
    #ACTUALIZAR TAG GIF 
    if message.content.startswith('.updategif'):
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     del args[0]
     tags = ' '.join(args)
     compo = comprobarUrl(url)
     if compo != None:
      ran = randint(1000,9999)
      await client.send_message(message.channel, '```ESCRIBE ESTE NUMERO PARA ACEPTAR EL UPDATE: '+ str(ran) + '```')
      nume = str(ran)
      if await client.wait_for_message(author=message.author, content=nume):
       actualizar(url,tags)
      # if await client.wait_for_message(author=message.author, content != nume):
       # await client.send_message(message.channel, 'HAS FRACASADO AL PONER EL CODIGO DE SEGURIDAD, NO SE UPDATEARA')
     else:
      await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF EN LA BASE DATOS:octagonal_sign:')
    
    #BORRAR GIF
    if message.content.startswith('.deletegif'):
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     compo = comprobarUrl(url)
     if compo != None:
      delete(url)
     else:
      await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF EN LA BASE DATOS:octagonal_sign:')
    
    #AYUDA  
    if message.content.startswith('.help'):
     help = discord.Embed(title='AYUDA', url='http://lavozpopular.com/wp-content/uploads/2014/09/Muere-Emilio-Bot%C3%ADn.jpg', description='Botin', color=0xff0000)
     help.set_image(url='http://lavozpopular.com/wp-content/uploads/2014/09/Muere-Emilio-Bot%C3%ADn.jpg')
     help.add_field(name='Mostrar Gif', value='.gif tags', inline=True)
     help.add_field(name='Ejemplo Mostrar Gif', value='.gif motos marquez', inline=True)
     help.add_field(name='Guardar Gif', value='.creategif url tags', inline=True)
     help.add_field(name='Ejemplo Guardar Gif', value='.creategif http://wwww.susto.com/imagen.gif susto', inline=True)
     help.add_field(name='Editar tags de Gif', value='.updategif url tags', inline=True)
     help.add_field(name='Ejemplo Editar tags de Gif', value='.updategif http://wwww.susto.com/imagen.gif susto discord', inline=True)
     await client.send_message(message.channel, embed=help)

     
#SACA URL AL BUSCAR POR TAGS            
def infoUrl(buscar,num):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT url FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = rows[num][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#SACA TAGS DEL GIF             
def infoTag(buscar,num):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT tag FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = rows[num][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#COMPRUEBA SI ENCUENTRA LA URL A RAIZ DE UNA URL            
def comprobarUrl(url):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT url FROM giftable where url = \'%s\'""", (AsIs(url),))
     rows = cur.fetchall()
     resultado = rows[0][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#ACTUALIZA TAGS DE GIF
def actualizar(url, tags):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""UPDATE giftable SET tag =\'%s\' where url = \'%s\';""", (AsIs(tags),AsIs(url),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    
            
#BORRA GIF BD          
def delete(url):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""DELETE from giftable where url = \'%s\';""", (AsIs(url),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  
            
#METE URL Y TAGS EN BD            
def meter(url, tags):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""INSERT INTO giftable (url, tag) VALUES (\'%s\', \'%s\');""", (AsIs(url),AsIs(tags),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  


#SACA LA CANTIDAD DE GIFS CON ESOS TAGS   
def canti(buscar):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT url FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = len(rows)
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#RUN
client.run(os.environ.get('BOT_TOKEN'))

