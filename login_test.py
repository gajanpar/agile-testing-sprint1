import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- KONFIGURASI ---
TEST_MODE = "real" 

def setup_driver():
    chrome_options = Options()
    # Hapus komentar di bawah jika ingin mode tanpa tampilan (headless)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--log-level=3") # Kurangi log sampah console
    
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

def run_tests():
    driver = setup_driver()
    all_passed = True
    
    try:
        print(f"🚀 Memulai Test Mode: {TEST_MODE.upper()}\n")

        # ---------------------------------------------------------
        # TC-01: LOGIN SUKSES
        # ---------------------------------------------------------
        print("Running TC-01 (Standard User)...", end=" ")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        try:
            WebDriverWait(driver, 5).until(EC.url_contains("inventory.html"))
            print("✅ PASS")
        except:
            print("❌ FAIL")
            all_passed = False

        # ---------------------------------------------------------
        # TC-02: USER TERKUNCI
        # ---------------------------------------------------------
        print("Running TC-02 (Locked Out User)...", end=" ")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").clear() # Bersihkan input sebelumnya
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        try:
            error_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
            )
            if "locked out" in error_elem.text:
                print("✅ PASS")
            else:
                print(f"❌ FAIL (Text mismatch: {error_elem.text})")
                all_passed = False
        except:
            print("❌ FAIL (Element not found)")
            all_passed = False

        # ---------------------------------------------------------
        # TC-03: KREDENSIAL SALAH (DEBUG MODE)
        # ---------------------------------------------------------
        print("Running TC-03 (Invalid User)...")
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("invalid_user")
        driver.find_element(By.ID, "password").send_keys("invalid_pass")
        driver.find_element(By.ID, "login-button").click()
        
        try:
            # Mengambil elemen error container
            error_container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
            )
            
            # --- BAGIAN DEBUGGING ---
            actual_text = error_container.text
            print(f"   🔎 [DEBUG] Teks dari website: '{actual_text}'")
            # ------------------------

            expected_text = "Username and password do not match any user in this service"
            
            if expected_text in actual_text:
                print("   ✅ TC-03: PASS")
            else:
                print(f"   ❌ TC-03: FAIL. Harapan: '{expected_text}'")
                all_passed = False
                
        except Exception as e:
            print(f"   💥 Error System: {str(e)}")
            all_passed = False

    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        all_passed = False
        
    finally:
        driver.quit()
        return all_passed

if __name__ == "__main__":
    success = run_tests()
    
    print("-" * 30)
    if success:
        print("🎉 SEMUA TEST LULUS — READY FOR DEPLOYMENT")
        sys.exit(0)
    else:
        print("⚠️  ADA TEST GAGAL — BLOCK DEPLOYMENT")
        sys.exit(1)