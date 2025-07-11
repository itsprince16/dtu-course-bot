from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ROLL_NO = "23/ME/333"
PASSWORD = "123"
LOGIN_URL = "https://reg.exam.dtu.ac.in/student/login"
COURSE_PAGE = "https://reg.exam.dtu.ac.in/student/courseRegistration/64d63a4d613f0cc3d4e8d337"
TARGET_COURSE = "VALUE ENGINEERING"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    driver.get(LOGIN_URL)
    try:
        roll_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "roll_no"))
        )
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Login")]')

        roll_input.clear()
        roll_input.send_keys(ROLL_NO)
        password_input.send_keys(PASSWORD)
        login_button.click()
        print("✅ Login submitted...")

        WebDriverWait(driver, 10).until(EC.url_contains("/student"))
        print("🎉 Logged in successfully!")
    except Exception as e:
        print("❌ Login failed:", e)
        driver.quit()
        exit()

def monitor_and_register():
    driver.get(COURSE_PAGE)
    time.sleep(3)
    while True:
        driver.refresh()
        print("🔁 Page refreshed...")
        try:
            rows = driver.find_elements(By.XPATH, '//table//tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 5:
                    course_name = cells[0].text.strip().upper()
                    seats = cells[5].text.strip()

                    if TARGET_COURSE in course_name:
                        print(f"📌 {course_name} - Seats: {seats}")
                        if seats.isdigit() and int(seats) > 0:
                            print(f"🎯 Registering for {TARGET_COURSE}...")
                            register_btn = cells[6].find_element(By.XPATH, './/button[contains(text(), "Register")]')
                            register_btn.click()
                            print("✅ Registered Successfully!")
                            return
        except Exception as e:
            print("⚠️ Error during scan:", e)

        time.sleep(5)

try:
    login()
    monitor_and_register()
except Exception as e:
    print("💥 Bot crashed:", e)
finally:
    print("🔥 Bot Stopped")
    driver.quit()
