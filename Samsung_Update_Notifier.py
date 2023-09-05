import requests
from bs4 import BeautifulSoup
import datetime
from pushbullet import PushBullet

def send_notification(token, title, text):
    # Get the instance using the access token

    pb = PushBullet(token)

    # Send the data by passing the main title

    # and text to be send

    devices = pb.devices

    result = devices[1].push_note(title, text)

    return result

def trunc_datetime(someDate):
    return someDate.replace(day=1)

def latest_update(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    today = datetime.date.today()

    job_elements = soup.find_all("div", class_="row", style_="")
    release_dates = []
    for update in job_elements:
        texts = update.find_all("div", class_="col-md-3")
        for text in texts:
            date = text.text
            if 'Release Date' in date:
                date_array = date.split((" : "))
                a = trunc_datetime(today)
                datetime_object = datetime.datetime.strptime(date_array[1], '%Y-%m-%d').date()
                b = trunc_datetime(datetime_object)
                if a == b:
                    print("New release!")
def check_website_for_update(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    today = datetime.date.today()

    job_elements = soup.find_all("div", class_="row", style_="")
    release_dates = []
    for update in job_elements:
        texts = update.find_all("div", class_="col-md-3")
        for text in texts:
            date = text.text
            if 'Release Date' in date:
                date_array = date.split((" : "))
                a = trunc_datetime(today)
                datetime_object = datetime.datetime.strptime(date_array[1], '%Y-%m-%d').date()
                b = trunc_datetime(datetime_object)
                if a == b:
                    return "New release!"

def get_link_to_check(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    language_picker = soup.find_all("div", class_="container")

    languages_array = []
    for repElem in language_picker:
        picker = repElem.find_all("div", class_="col-md-2")
        for pick in picker:
            languages = pick.find_all("option")
            #link = languages.get('value')
            for language in languages:
                if ('English' in language):
                    link = language['value']
                    languages_array.append(link)
                    break


    return languages_array[0][6:]


if __name__ == '__main__':
    device_code = 'SM-R890'
    csc_codes = ['ATO', 'ZTO', 'BGL', 'XEZ', 'XEF', 'DBT', 'EUR', 'XEH','ITV', 'LUX', 'XEO', 'TPH']
    country_name = ['Austria', 'Brazil', 'Bulgaria', 'Czech Republic', 'France', 'Germany', 'Greece', 'Hungary', 'Italy', 'Luxembourg', 'Poland', 'Portugal']
    #URL = "https://doc.samsungmobile.com/SM-R890/019946210827/eng.html"

    url_start = "https://doc.samsungmobile.com/"

    f = open("token", "r")
    access_token = f.read()

    for i in range(len(csc_codes)):

        URL = url_start + device_code + "/" + csc_codes[i] + "/doc.html" #"https://doc.samsungmobile.com/SM-R890/TPH/doc.html"

        link = get_link_to_check(URL)

        title = check_website_for_update(url_start + link)

        if title is not None:
            send_notification(access_token, title, country_name[i])




