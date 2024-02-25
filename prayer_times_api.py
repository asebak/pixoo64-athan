import requests
from bs4 import BeautifulSoup

class PrayerTimesApi:
    def __init__(self):
        pass

    def retrieve_prayer_times(self):
        url = "https://us.mohid.co/sc/rockhill/greenvillemasjid/masjid/widget/api/index/?m=prayertimings"
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        prayer_times_table = soup.findAll('ul')[1]
        new_data = self._parse_prayer_times_table(prayer_times_table)
        return new_data

    def _parse_prayer_times_table(self, elem):
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
