import psycopg2
import csv

DB_host = 'localhost'
DB_name = 'uploadfile'
DB_user = 'postgres'
DB_password = '1234'

conn = psycopg2.connect(host=DB_host, dbname=DB_name, user=DB_user, password=DB_password)
print(conn)
cur = conn.cursor()
f = open(r'C:\Users\ASUS\Documents\deepspeech\mic_vad_streaming\output.csv') #File path
cur.copy_from(f, "users", sep=",")
conn.commit()
f.close()
#conn.close()