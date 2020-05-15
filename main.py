import requests
import mysql.connector
import pytz
from datetime import datetime, timedelta
import time

tz = pytz.timezone('Asia/Bangkok')
refresh_time = "14:35"

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="1234",
    database="main")
mycursor = mydb.cursor()

def spacial_round(num):
    num = round(num,3)*10
    if int(str(num)[-1]) < 5:
        result = round(round(num)/10+0.05, 3)
        print(result)
        return result
    else:
        result = round(round(num)/10,3)
        print(result)
        return result

while True:
    now = datetime.now(tz)
    dt_string = now.strftime("%H:%M")

    if dt_string == refresh_time:
        url = "https://crmmobile.bangchak.co.th/webservice/oil_price.aspx"
        data = requests.get(url)
        data.encoding = "utf-8"
        # print(data.content)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data.text,'lxml')
        # print(soup.prettify())
        x = soup.find_all("type") # <- ค่าที่ใช้ในการค้นหา
        today_price = soup.find_all("today")

        price_G91 = float(str(today_price[6])[7:12])
        price_G95 = float(str(today_price[7])[7:12])
        price_D = float(str(today_price[1])[7:12])

        print('\nToday price')
        print('G91\t: {} THB/L'.format(price_G91))
        print('G95\t: {} THB/L'.format(price_G95))
        print('Diesel\t: {} THB/L'.format(price_D))
        print('\n')

        sql = "INSERT INTO today_price (gas_id, current_price, sell_price, date) VALUES (%s, %s, %s, %s)"
        now = datetime.now(tz)
        dt_string = now.strftime("%Y-%m-%d")
        val = [
            (1, price_G91, spacial_round(price_G91+0.9), dt_string),
            (2, price_G95, spacial_round(price_G95+0.9), dt_string),
            (3, price_D, spacial_round(price_D+0.9), dt_string)
        ]

        mycursor.executemany(sql, val)
        mydb.commit()

        mycursor.execute("SELECT * FROM today_price")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

        print("Wait for check time again.")
        time.sleep(65)

    else:
        print(dt_string)
        time.sleep(30)
