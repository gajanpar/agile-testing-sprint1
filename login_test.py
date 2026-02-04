# login_test.py
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def setup_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=firefox_options
    )

def run_tests():
    driver = setup_driver()
    all_passed = True

    try:
        print("🧪 Running TC-01: Login valid")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        print("✅ TC-01: PASS")

        print("🧪 Running TC-02: User terkunci")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        error_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        if "locked out" in error_elem.text.lower():
            print("✅ TC-02: PASS")
        else:
            print("❌ TC-02: FAIL")
            all_passed = False

        print("🧪 Running TC-03: Kredensial salah")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("invalid")
        driver.find_element(By.ID, "password").send_keys("invalid")
        driver.find_element(By.ID, "login-button").click()
        
        error_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_text = error_elem.text
        if "username and password do not match" in error_text.lower():
            print("✅ TC-03: PASS")
        else:
            print(f"❌ TC-03: FAIL – Pesan: '{error_text}'")
            all_passed = False

    except Exception as e:
        print(f"💥 Exception: {str(e)}")
        all_passed = False
    finally:
        driver.quit()
        return all_passed

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n🎉 SEMUA TEST LULUS — READY FOR DEPLOYMENT")
        sys.exit(0)
    else:
        print("\n⚠️  ADA TEST GAGAL — BLOCK DEPLOYMENT")
        sys.exit(1)
