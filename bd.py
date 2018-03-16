import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')