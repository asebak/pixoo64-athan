import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from circular_linked_list import CircularLinkedList, PrayerSlot
from pixoo import Pixoo
from prayer_times_api import PrayerTimesApi

timeout = 60


# Hardware Apis
def get_pixoo_devices():
    response = (requests.post(
        "https://app.divoom-gz.com/Device/ReturnSameLANDevice",
        timeout=100,
    ))
    device_list = response.json()['DeviceList']
    return device_list


def main():
    print('[.] Booting..')

    morning = (215,255,254)
    night = (0, 0, 0)
    dawn_evening = (46, 20, 83)

    device = get_pixoo_devices()[0]

    pixoo = Pixoo(device['DevicePrivateIP'])
    pixoo.draw_image('morning.png', xy=(0, 21))

    pixoo.push()

    time.sleep(2)
    api = PrayerTimesApi()

    print('[.] Starting update loop')
    while True:
        prayer_times = api.retrieve_prayer_times()
        current_time = datetime.today().strftime("%H:%M")
        cll = CircularLinkedList()

        for key, value in prayer_times.items():
            athan = datetime.strptime(value["athan"], '%I:%M %p')
            iqama = datetime.strptime(value["iqama"], '%I:%M %p')
            cll.add(PrayerSlot(key, athan, iqama))

        current_slot = cll.traverse_updated(current_time)

        next_slot_data = current_slot.next.data

        pixoo.fill(morning)
        pixoo.draw_text(next_slot_data.name, (20, 0), night)
        pixoo.draw_text("Athan: " + next_slot_data.athan.strftime("%H:%M"), (8, 8), night)
        pixoo.draw_text("Iqama: " + next_slot_data.iqama.strftime("%H:%M"), (8, 16), night)
        pixoo.draw_image('morning.png', xy=(0, 21))

        pixoo.push()

        time.sleep(timeout)


if __name__ == '__main__':
    main()
