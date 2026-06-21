import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
DB_CONF = {
    "host" : os.getenv("DB_HOST", "localhost"),
    "port" : os.getenv("DB_PORT", 3306),
    "database" : os.getenv("DB_NAME", "UNOpraise"),
    "user" : os.getenv("DB_USER", "root"),
    "password" : os.getenv("DB_PASSWORD", "")
}


def consultar_DB(query):
    cnx = mysql.connector.connect(**DB_CONF)
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df

query = """SELECT tc.tipo,c.color FROM tipoCarta tc
join carta c on tc.id = c.id_tipo;
"""
tabla = consultar_DB(query)
print(tabla)