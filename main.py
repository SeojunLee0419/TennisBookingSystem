import os
import json
import dropbox
import streamlit as st

from dropbox.exceptions import AuthError
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


LOCAL_FILE_PATH = "config.json"
DROPBOX_FILE_PATH = f"/config/{LOCAL_FILE_PATH}"


def upload_config_file_to_dropbox():
    with dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN) as dbx:
        try:
            # Upload the file
            with open(LOCAL_FILE_PATH, "rb") as f:
                dbx.files_upload(f.read(), DROPBOX_FILE_PATH, mode=dropbox.files.WriteMode("overwrite"))

            print("File uploaded to Dropbox.")
        except AuthError as e:
            print("Error authenticating with Dropbox: %s" % e)


st.title('NY Winter Tennis Club')
st.write('Hello, *World!* :sunglasses:')

config = {'active': st.toggle('Activate', value=True, help='reservation a tennis court')}

date_str = st.date_input("Booking day?", value="today", format="YYYY/MM/DD")
formatted_date = date_str.strftime("%B %d, %Y - %A")
st.write('Date:', formatted_date)

config['booking_date'] = formatted_date

# t = st.time_input('Booking time?', datetime.time(19, 00), step=3600)

# November 04, 2023 - Saturday
# formatted_time = t.strftime('%I:%M %p')
# st.write('Time:', formatted_time)

options = st.multiselect(
    'Booking time?',
    ['07:00 PM', '08:00 PM', '09:00 PM'],
    ['07:00 PM'],
    help="keep the time order"
)

config['booking_time'] = options
st.json(config)

# st.write('You selected:', options)

if st.button("Submit", type="primary"):
    # Write the dictionary to a JSON file
    with open(LOCAL_FILE_PATH, "w") as json_file:
        json.dump(config, json_file, indent=4)

    upload_config_file_to_dropbox()
    st.write(f"Configuration written to {LOCAL_FILE_PATH}")

#
# {
#     "active": false,
#     "booking_date": "November 08, 2023 - Wednesday",
#     "booking_time": [
#         "07:00 PM",
#         "08:00 PM"
#     ]
# }