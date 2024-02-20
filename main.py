from pixoo import Pixoo
import os
import time
import requests
timeout = 3600
def retrieve_prayer_times():
    return None

def get_pixoo_devices():
    response = (requests.post(
        "https://app.divoom-gz.com/Device/ReturnSameLANDevice",
        timeout=100,
    ))
    device_list = response.json()['DeviceList']
    return device_list

def main():
    print('[.] Booting..')


    # A pleasant green color. Like a yet-to-be-ripe banano
    green = (99, 199, 77)
    red = (255, 0, 68)
    white = (255, 255, 255)

    # Retrieve some config

    device = get_pixoo_devices()[0]

    # Set up a connection and show the background
    pixoo = Pixoo(device['DevicePrivateIP'])
    pixoo.draw_image('background.png')
    pixoo.get
    settings = pixoo.get_settings()
    # pixoo.set_brightness(100) # Only used sometimes if the screen isn't bright enough
    pixoo.draw_text('-----', (20, 49), green)
    pixoo.draw_text('------', (20, 43), green)
    pixoo.draw_text('-------------', (7, 57), green)
    pixoo.push()

    time.sleep(2)

    print('[.] Starting update loop')
    while True:
        prayer_times = retrieve_prayer_times()


        pixoo.draw_image('background.png')

        # Draw the change percentage
        pixoo.draw_text(f'1%', (20, 49), green)

        # Draw current price
        pixoo.draw_text(f'2', (20, 43), green)

        # Draw current F@H stats
        pixoo.draw_text(f'F@H 3', (7, 57), green)

        # Push to the display
        pixoo.push()

        # Wait a bit before updating everything
        time.sleep(timeout)


if __name__ == '__main__':
    main()


