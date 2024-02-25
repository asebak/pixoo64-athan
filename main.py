import time
from datetime import datetime

import requests

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

    morning = (215, 255, 254)
    night = (0, 0, 0)
    dawn_evening = (46, 20, 83)
    red = (255, 30, 39)

    device = get_pixoo_devices()[0]

    pixoo = Pixoo(device['DevicePrivateIP'])

    pixoo.push()

    time.sleep(2)
    api = PrayerTimesApi()

    print('[.] Starting update loop')
    while True:
        prayer_times = api.retrieve_prayer_times()
        current_time = datetime.today()
        current_time_str = current_time.strftime("%H:%M")
        cll = CircularLinkedList()

        for key, value in prayer_times.items():
            athan = datetime.strptime(value["athan"], '%I:%M %p')
            iqama = datetime.strptime(value["iqama"], '%I:%M %p')
            cll.add(PrayerSlot(key, athan, iqama))

        current_slot = cll.traverse_updated(current_time_str)

        next_slot_data = current_slot.next.data

        match next_slot_data.name:
            case 'Magrib' | 'Fajr':
                text_color = morning
                bg_color = dawn_evening
                picture = 'dawn_evening'
            case 'Isha':
                text_color = morning
                bg_color = night
                picture = 'night'
            case _:
                text_color = night
                bg_color = morning
                picture = 'morning'

        warning_text_color = text_color
        start_time = int(next_slot_data.athan.strftime("%H")) * 60 + int(next_slot_data.athan.strftime("%M"))
        end_time = int(next_slot_data.iqama.strftime("%H")) * 60 + int(next_slot_data.iqama.strftime("%H"))
        current_time = datetime.now().hour * 60 + datetime.now().minute
        if start_time <= current_time <= end_time:
            warning_text_color = red

        pixoo.fill(bg_color)
        pixoo.draw_text(next_slot_data.name, (25, 1), text_color)
        pixoo.draw_text("Athan:", (8, 8), text_color)
        pixoo.draw_text("Iqama:", (8, 16), text_color)
        pixoo.draw_text(next_slot_data.athan.strftime("%H:%M"), (36, 8), warning_text_color)
        pixoo.draw_text(next_slot_data.iqama.strftime("%H:%M"), (36, 16), warning_text_color)
        pixoo.draw_image(picture + '.png', xy=(0, 21))

        pixoo.push()

        time.sleep(timeout)


if __name__ == '__main__':
    main()
