import os
import sys
from io import StringIO
from time import sleep

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from kakao import send_kakao_talk
from util import full_screen_shot, convert_to_24_hour_format, download_config_file_from_dropbox, load_config

# write file
buffer = StringIO()

# load config.json
config_file = download_config_file_from_dropbox()
config = load_config(config_file)
print(config)

if config["active"]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()

    driver.get("https://nyta.chelseareservations.com/")

    username = driver.find_element(By.ID, "UsernameTextBox")
    password = driver.find_element(By.ID, "PasswordTextBox")

    booking_date = config['booking_date']
    booking_times = config['booking_time']
    buffer.write(booking_date + "\n")
    buffer.write(str(booking_times) + "\n")
    # booking_date = "November 09, 2023 - Thursday"
    # booking_date = "November 10, 2023 - Friday"
    # booking_times = ["07:00 PM", "08:00 PM", "09:00 PM"]
    booking_times_24_hour = convert_to_24_hour_format(booking_times)

    # Todo
    username.send_keys(os.getenv("MEMBER1"))
    password.send_keys(os.getenv("MEMBER1_PASS"))

    login_button = driver.find_element(By.ID, "btnTennis")
    login_button.click()

    cookies = driver.get_cookies()

    # for cookie in cookies:
    #     print(f"Name: {cookie['name']}, Value: {cookie['value']}")

    kakao_talk_message = StringIO()

    driver.get("https://nyta.chelseareservations.com/tennis/TNBookingNew.aspx")

    member_number_1 = driver.find_element(By.ID, "RequestTabPage_pnlBooking_txtMemberNoL01P1")
    member_number_2 = driver.find_element(By.ID, "RequestTabPage_pnlBooking_txtMemberNoL01P2")

    # Todo
    member_number_1.send_keys(os.getenv("MEMBER1"))
    member_number_2.send_keys(os.getenv("MEMBER2"))

    select = Select(driver.find_element(By.ID, "RequestTabPage_pnlBooking_ddlHours"))

    # [0]: start_time
    select.select_by_value(booking_times_24_hour[0])
    select_date = Select(driver.find_element(By.ID, "RequestTabPage_pnlBooking_ddlPlayDate"))
    options = select_date.options

    # buffer = StringIO()
    dates_list = []
    for option in options:
        dates_list.append(option.get_attribute("value"))
        # sleep(10)

    do_reservation = False
    for day in dates_list:
        # exclude SAT, SUN day
        if day in ['Saturday', 'Sunday']:
            continue

        print(day)
        # if 'Tuesday' in day or 'Thursday':
        if day in booking_date:
            do_reservation = True

        buffer.write(day + "\n")

        select_date = Select(driver.find_element(By.ID, "RequestTabPage_pnlBooking_ddlPlayDate"))
        select_date.select_by_value(day)

        display_button = driver.find_element(By.ID, "RequestTabPage_pnlBooking_btnDisplayTimes")
        driver.execute_script("arguments[0].click();", display_button)

        sleep(5)

        # html_page = driver.page_source

        try:
            if do_reservation:
                first_row_time_element = driver.find_element(By.CSS_SELECTOR,
                                                             "#GridView3 tr:nth-child(1) td:nth-child(1) a")
                first_row_time_text = first_row_time_element.text
                # reserve at 8:00 PM
                if first_row_time_text in booking_times:
                    print(":Selected Time:" + first_row_time_text)
                    buffer.write(first_row_time_text + "\n")

                    # click selected time
                    first_row_time_element.click()
                    sleep(10)

                    # submit
                    print(":Submit")
                    submit_button = driver.find_element(By.ID, "btnSubmit")
                    driver.execute_script("arguments[0].click();", submit_button)
                    # save screen
                    full_screen_shot(driver, f"reservation_{day}.png")
                    # send to kakao_talk
                    send_kakao_talk(f"Reservation is done:{day}")
                else:
                    print(first_row_time_text)
                    buffer.write(first_row_time_text + "\n")

        except Exception as e:
            print(e)
            buffer.write(e + "\n")
            full_screen_shot(driver, f"error_{day}.png")
        finally:
            do_reservation = False
            if day in booking_date:
                full_screen_shot(driver, f"full_screen_{day}.png")

        # if convert_message(buffer, html_page) is False:
        #     screen_capture = f"screenshot_{day}.png"
        #     print(screen_capture)
        #     driver.save_screenshot(screen_capture)

    driver.quit()

else:
    buffer.write('skip booking' + "\n")


current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

with open("booking_report_status.txt", "a") as file:
    file.write('---Result---' + "\n")
    file.write(formatted_time + "\n")
    buffer.seek(0)
    data = buffer.read()
    file.write(data)

print('write done!')

# print('---Result---')
# buffer.seek(0)
# data = buffer.read()
# print(data)

# send_kakao_talk(data)
