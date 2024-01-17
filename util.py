import json
import os

import dropbox
from bs4 import BeautifulSoup
from dropbox.exceptions import AuthError
from dotenv import load_dotenv
import datetime


# ["07:00 PM", "08:00 PM", "09:00 PM"]
# ['19', '20', '21']
def convert_to_24_hour_format(booking_times):
    converted_times = []

    for time_str in booking_times:
        time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
        converted_time = time_obj.strftime("%H")
        converted_times.append(converted_time)
    return converted_times


# https://blog.devgenius.io/mastering-dropbox-api-communication-with-python-e2b001b371a8
'''
{
  "access_token": "sl.Bpnwzqm8uSBaMN_Mu_dWhyDCUhqyPcR1PyXBIt8NpLDwSScVm7EcBr02POJZgYxK7l82al_o59AkebbgdjkjJBpFaW4DdDw0XVuvMi49rd8nKj5E87GPaaFv2tgu2qCfiRQMG74jKH7R",
  "token_type": "bearer",
  "expires_in": 14400,
  "refresh_token": "cShUbeHWdusAAAAAAAAAAeCycrb_UBOslZm2Bx4GHW66xi4smwvYsOic8M_di3rq",
  "scope": "account_info.read files.content.read files.content.write files.metadata.read",
  "uid": "65835844",
  "account_id": "dbid:AAA_dVr8e1IEqoSDo1MZCMltmkttgSC8fHs"
}
'''

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

LOCAL_FILE_PATH = "config.json"
DROPBOX_FILE_PATH = f"/config/{LOCAL_FILE_PATH}"


def download_config_file_from_dropbox():
    # https://stackoverflow.com/questions/70641660/how-do-you-get-and-use-a-refresh-token-for-the-dropbox-api-python-3-x
    with dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN) as dbx:
        try:
            metadata, res = dbx.files_download(DROPBOX_FILE_PATH)

            # Save the downloaded JSON data to a local file
            with open(LOCAL_FILE_PATH, "wb") as local_file:
                local_file.write(res.content)
            print(f"Downloaded '{DROPBOX_FILE_PATH}' to '{LOCAL_FILE_PATH}'")
        except dropbox.exceptions.HttpError as e:
            print(f"Error downloading file: {e}")
    return LOCAL_FILE_PATH


def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        return config_data

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{file_path}': {e}")
        return None


def full_screen_shot(driver, file_name):
    height = driver.execute_script('return document.documentElement.scrollHeight')
    width = driver.execute_script('return document.documentElement.scrollWidth')
    driver.set_window_size(width, height)
    driver.save_screenshot(file_name)


def convert_message(buffer, html):
    # html = driver.page_source
    try:
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', {'id': 'GridView3'})

        data = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            row_data = []
            for cell in cells:
                cell_text = cell.get_text(strip=True)
                if cell_text != '':
                    row_data.append(cell_text)
            data.append(row_data)

        # report_data = {}
        for row in data:
            time = row[0]
            if time != '11:00  PM' and time != '10:00  PM' and time != '09:00  PM':
                print(row)
                buffer.write("" + str(row) + "\n")

    except Exception:
        # print(html)
        return False


if __name__ == "__main__":
    download_config_file_from_dropbox()

    '''
    import dropbox

    LOCAL_FILE_PATH = "config.json"
    DROPBOX_FILE_PATH = f"/config/{LOCAL_FILE_PATH}"

    load_dotenv()

    APP_KEY = os.getenv("APP_KEY")
    APP_SECRET = os.getenv("APP_SECRET")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


    def upload_config(dbx):
        try:
            # Upload the file
            with open(LOCAL_FILE_PATH, "rb") as f:
                dbx.files_upload(f.read(), DROPBOX_FILE_PATH, mode=dropbox.files.WriteMode("overwrite"))

            print("File uploaded to Dropbox.")
        except AuthError as e:
            print("Error authenticating with Dropbox: %s" % e)

    def download_config(dbx):
        # Download the file from Dropbox
        try:
            metadata, res = dbx.files_download(DROPBOX_FILE_PATH)

            # Save the downloaded JSON data to a local file
            with open(LOCAL_FILE_PATH, "wb") as local_file:
                local_file.write(res.content)

            print(f"Downloaded '{DROPBOX_FILE_PATH}' to '{LOCAL_FILE_PATH}'")
        except dropbox.exceptions.HttpError as e:
            print(f"Error downloading file: {e}")


    with dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN) as dbx:
        download_config(dbx)
    
    '''
