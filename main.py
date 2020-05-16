import requests
import pytz
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

tz = pytz.timezone('Asia/Bangkok')
refresh_time = "05:00"

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
    try:
        now = datetime.now(tz)
        dt_string = now.strftime("%H:%M")

        if dt_string == refresh_time:
            url = "https://crmmobile.bangchak.co.th/webservice/oil_price.aspx"
            data = requests.get(url)
            data.encoding = "utf-8"
            # print(data.content)
            soup = BeautifulSoup(data.text,'lxml')
            # print(soup.prettify())
            x = soup.find_all("type") # <- ค่าที่ใช้ในการค้นหา
            today_price = soup.find_all("today")

            price_G91 = (float(str(today_price[6])[7:12]))
            price_G95 = (float(str(today_price[7])[7:12]))
            price_D = (float(str(today_price[1])[7:12]))

            Sprice_G91 = spacial_round(float(str(today_price[6])[7:12])+0.9)
            Sprice_G95 = spacial_round(float(str(today_price[7])[7:12])+0.9)
            Sprice_D = spacial_round(float(str(today_price[1])[7:12])+0.9)

            print('\nToday price')
            print('G91\t: {} THB/L'.format(price_G91))
            print('G95\t: {} THB/L'.format(price_G95))
            print('Diesel\t: {} THB/L'.format(price_D))
            print('\n')

            payload = "http://35.240.230.42/production/today_price.php?g91-c=" + str(price_G91) + "&g91-s=" + str(Sprice_G91) + "&g95-c=" + str(price_G95) + "&g95-s=" + str(Sprice_G95) + "&desel-c=" + str(price_D) + "&desel-s=" + str(Sprice_D)
            # url = "http://35.240.230.42/production/today_price.php?g91-c=0&g91-s=0&g95-c=0&g95-s=0&desel-c=0&desel-s=0"
            data = requests.get(payload)

            print('send payload to server ,wait for refresh again')
            time.sleep(65)
            pass

        else:
            print(dt_string)
            time.sleep(30)
            pass

    except:
        print('error')
        pass
