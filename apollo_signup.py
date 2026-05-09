import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run_signup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Required for GitHub Actions
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize Driver
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Go to Apollo Signup
        driver.get("https://www.apollo.io/sign-up")
        
        # 2. Click Sign up with Microsoft
        ms_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Sign up with Microsoft')]")))
        ms_btn.click()

        # 3. Click "Create one!" on Microsoft Page
        create_btn = wait.until(EC.element_to_be_clickable((By.ID, "signup")))
        create_btn.click()

        # 4. Fill random email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "floatingLabelInput4")))
        email_field.send_keys(f"user_{generate_random_string()}@outlook.com")
        
        next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        next_btn.click()

        # 5. Fill Password
        pass_field = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        pass_field.send_keys("Hellobd1@")
        driver.find_element(By.ID, "nextButton").click()

        # 6. Name Fields
        first_name = wait.until(EC.presence_of_element_located((By.ID, "firstNameInput")))
        first_name.send_keys(generate_random_string(5))
        driver.find_element(By.ID, "lastNameInput").send_keys(generate_random_string(5))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 7. Handling the "Press and Hold" Captcha
        # Note: Automated solvers for "Press and Hold" are complex. 
        # This attempts a basic click-and-hold action.
        try:
            captcha_element = wait.until(EC.presence_of_element_located((By.ID, "MnSwDbaTWhDkJKn")))
            actions = ActionChains(driver)
            actions.click_and_hold(captcha_element).perform()
            time.sleep(10) # Hold for 10 seconds to simulate human
            actions.release(captcha_element).perform()
        except Exception as e:
            print("Captcha interaction failed or not present:", e)

        print("Flow completed.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_signup()
