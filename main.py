from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup
from more_itertools import peekable

from pixoo import Pixoo
from itertools import cycle

timeout = 3600


# Prayer time apis
def retrieve_prayer_times():
    url = "https://us.mohid.co/sc/rockhill/greenvillemasjid/masjid/widget/api/index/?m=prayertimings"
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data)
    prayer_times_table = soup.findAll('ul')[1]
    new_data = parse_prayer_times_table(prayer_times_table)
    return new_data


def parse_prayer_times_table(elem):
    result = {}
    for sub in elem.find_all('li', recursive=False):
        if sub.div is None:
            continue
        data = {}
        prayer_name = str(sub.next_element.strip())
        athan = sub.find("div", {"class": "prayer_azaan_div"})
        if athan is not None:
            data["athan"] = str(athan.text.strip())
        else:
            continue
        iqama = sub.find("div", {"class": "prayer_iqama_div"})
        if iqama is not None:
            data["iqama"] = str(iqama.text.strip())
        result[prayer_name] = data
    return result


# Hardware Apis
def get_pixoo_devices():
    response = (requests.post(
        "https://app.divoom-gz.com/Device/ReturnSameLANDevice",
        timeout=100,
    ))
    device_list = response.json()['DeviceList']
    return device_list


# Calculations

def get_total_minutes(t):
    tt = t.split(':')
    return tt[0] * 60 + tt[1] * 1


def is_current_prayer(current, start, end):
    t = get_total_minutes(current)
    s = get_total_minutes(start)
    e = get_total_minutes(end)
    r = False

    if e > s:
        if s <= t < e:
            r = True
    else:
        r = is_current_prayer(current, end, start)

    return r


def main():
    print('[.] Booting..')

    # A pleasant green color. Like a yet-to-be-ripe banano
    green = (99, 199, 77)
    red = (255, 0, 68)
    white = (255, 255, 255)

    device = get_pixoo_devices()[0]

    pixoo = Pixoo(device['DevicePrivateIP'])
    pixoo.fill((46, 20, 83))
    pixoo.draw_image('background.png', xy=(0, 21))

    pixoo.push()

    time.sleep(2)

    print('[.] Starting update loop')
    while True:
        current_iteration = 0
        prayer_times = retrieve_prayer_times()
        total_length = len(prayer_times.items())
        current_time = datetime.today().strftime("%I:%M %p")

        pool = cycle(prayer_times)

        for item in pool:
            is_current = is_current_prayer(current_time, prayer_times[item]["athan"], prayer_times[next_item]["athan"])
            print(item)
            #next(pool)

         #      for key, value in prayer_times.items():
          #         is_current_prayer()
        # pixoo.draw_text(key, (0, current_iteration * 8), white)
        # pixoo.draw_text(value["iqama"], (10, current_iteration * 8), white)
        # current_iteration = current_iteration + 1

        #     pixoo.draw_text("Athan", (18, 2), white)
        #    pixoo.draw_text("Iqama", (42, 2), white)
        #    pixoo.draw_text("Fajr", (0, 12), white)
        #    pixoo.draw_text("6:42AM", (18, 12), white)
        #    pixoo.draw_text("ahmad", (42, 12), white)
        # pixoo.draw_line((0, 2), (64, 2), white)
        # pixoo.draw_text("Athan", (0, 2), white)
        # pixoo.draw_text("Iqama", (0, 2), white)
        pixoo.push()

        time.sleep(timeout)


if __name__ == '__main__':
    main()
