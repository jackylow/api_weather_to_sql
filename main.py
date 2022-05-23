import requests
import psycopg2
from config import API_KEY, my_database, user_name, my_password, my_host, my_port
from city import cities

head = {
    "X-Yandex-API-Key": API_KEY
}


def our_connection(database, user, password, host, port):
    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return connection


con = our_connection(my_database, user_name, my_password, my_host, my_port)


def create_table():
    cur = con.cursor()
    cur.execute("""CREATE TABLE WEATHER (
        City TEXT,
        Temperature INT);""")


create_table()


def filling_table():
    cur = con.cursor()
    for key in cities:
        response = requests.get(url="https://api.weather.yandex.ru/v2/forecast?", params=cities[key], headers=head)
        weather = response.json()
        cur.execute(f"INSERT INTO weather (City, Temperature) VALUES ('{key}', {weather['fact']['temp']})")
        print(weather['fact']['temp'])


filling_table()

con.commit()
con.close()
