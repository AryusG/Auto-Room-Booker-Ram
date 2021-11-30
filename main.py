from next_two_days import NewDateTwoDaysAhead
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os


class AutoRoomBooker():
    def __init__(self):
        self.driver = webdriver.Safari()
        self.driver.maximize_window()
        self.two_days_ahead = NewDateTwoDaysAhead()


    def pick_two_days_ahead(self):
        day_month_year_list = self.two_days_ahead.get_day_month_year()
        tda_day = day_month_year_list[0]
        tda_month_string = self.two_days_ahead.get_month_string()
        tda_year = str(day_month_year_list[2])

        date_div_class = 'ui-datepicker-title'

        stale_element_thrown = True
        while stale_element_thrown:
            try:
                date_div_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, date_div_class)))
                date_div_string = date_div_element.text
                date_div_split = date_div_string.split()
                month = date_div_split[0]
                year = date_div_split[1]

                stale_element_thrown = False

            except StaleElementReferenceException:
                pass

        while month != tda_month_string or year != tda_year:
            next_month_xpath = '//*[@id="navigation-calendar"]/div/div/a[2]'
            try:
                next_month_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, next_month_xpath)))
                next_month_element.click()

                date_div_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, date_div_class)))
                date_div_string = date_div_element.text
                date_div_split = date_div_string.split()
                month = date_div_split[0]
                year = date_div_split[1]

            except (StaleElementReferenceException):
                print("StaleElementReferenceException occured")
            
            time.sleep(0.1)

        no_such_element_thrown = True
        while no_such_element_thrown:
            try:
                day_a_xpath = f"//a[text()='{tda_day}']"
                day_a_tag = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, day_a_xpath)))
                day_a_tag.click()
                no_such_element_thrown = False

            except (NoSuchElementException, StaleElementReferenceException):
                print("day_a_tag errors")


    def pick_two_hours_ahead(self, current_time):
        time_list = current_time.split(":") 
        hours = int(time_list[0])
        mins_str = time_list[1]

        if hours == 23:
            hours = 1
        elif hours == 24:
            hours = 0
        else:
            hours += 2

        hours_str = str(hours)

        return f"{hours_str}:{mins_str}"

    
    def get_current_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        return current_time


    def login(self):
        load_dotenv()
        ram_webpage = "https://ram.asimut.net"
        user_name = os.getenv("LOGIN")
        password = os.getenv("PASS")
        
        self.driver.get(ram_webpage)

        login_xpath = '//*[@id="login-username-2606"]'
        pass_xpath = '//*[@id="login-password-2606"]'
        button_login_xpath = '//*[@id="2606"]/button'

        login_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, login_xpath)))

        time.sleep(1)

        login_element.send_keys(user_name)
        self.driver.find_element_by_xpath(pass_xpath).send_keys(password)
        self.driver.find_element_by_xpath(button_login_xpath).click()
    

    def book_general_practice_room(self, room_name_str):
        start_time = self.get_current_time()

        g_practice_room_xpath = '//*[@id="left-column"]/h2[1]/a'
        try:
            g_practice_room_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, g_practice_room_xpath)))
            g_practice_room_element.click()

        except StaleElementReferenceException:
            pass
        
        self.pick_two_days_ahead()

        name_room_is_clicked = False
        while name_room_is_clicked is False:
            try:
                name_xpath = f"//a[normalize-space()='{room_name_str}']"
                room_name_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, name_xpath)))
                print(room_name_element)
                room_name_element.click()
                print(f"YAY WE CLICKED {room_name_str}")
                name_room_is_clicked = True
            except (ElementNotInteractableException, StaleElementReferenceException):    
                print('name_room_stale_element_exception')
        
        if name_room_is_clicked:
            create_booking_xpath = '//*[@id="function-span"]/p[1]/a'
            create_booking_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, create_booking_xpath)))
            create_booking_element.click()

        time_xpath = '//*[@id="event-starttime"]'
        time_xpath_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, time_xpath)))
        time_xpath_element.send_keys(start_time)

        end_time_xpath = '//*[@id="event-endtime"]'
        end_time_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, end_time_xpath)))

        for i in range(5):
            end_time_element.send_keys(Keys.BACK_SPACE)
            print(i)

        end_time_element.send_keys(self.pick_two_hours_ahead(start_time))  

bot = AutoRoomBooker()
print(bot.get_current_time())
bot.login()
bot.book_general_practice_room('CK21 (General Practice Room)')



time.sleep(10)