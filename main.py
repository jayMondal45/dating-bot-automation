from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

FB_Email = "your_email_here"
FB_Password = "your_password_here"
My_Number = "your_phone_number_here"

# NOTE: Automating Tinder may violate their Terms of Service
# Use at your own risk

# helper function to wait for elements
def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and return it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element to be clickable and click it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except TimeoutException:
        print(f"Timeout waiting to click element: {value}")
        return False

# chrome setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

try:
    print("Opening Tinder...")
    driver.get("https://tinder.com")
    
    # accept cookies popup
    print("Accepting cookies...")
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Accept') or contains(., 'I accept')]", timeout=5):
        print("✓ Cookies accepted")
        time.sleep(1)
    
    # find and click login
    print("Looking for login button...")
    if wait_and_click(driver, By.XPATH, "//a[contains(., 'Log in')]", timeout=5):
        print("✓ Login button clicked")
        time.sleep(2)
    
    # use facebook login
    print("Looking for Facebook login option...")
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Facebook')]", timeout=5):
        print("✓ Facebook login clicked")
        time.sleep(3)
    
    # wait for fb popup to appear
    print("Waiting for Facebook login popup...")
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    
    base_window = driver.window_handles[0]
    fb_login_window = driver.window_handles[1]
    driver.switch_to.window(fb_login_window)
    print("✓ Switched to Facebook login window")
    
    # fill in facebook email
    print("Entering Facebook email...")
    email_field = wait_for_element(driver, By.ID, "email", timeout=10)
    if email_field:
        email_field.clear()
        email_field.send_keys(FB_Email)
        print("✓ Email entered")
    
    # fill in password
    print("Entering Facebook password...")
    password_field = wait_for_element(driver, By.ID, "pass", timeout=10)
    if password_field:
        password_field.clear()
        password_field.send_keys(FB_Password)
        print("✓ Password entered")
    
    # submit the login form
    print("Clicking Facebook login button...")
    if wait_and_click(driver, By.CSS_SELECTOR, "input[type='submit']", timeout=5):
        print("✓ Facebook login submitted")
    
    # give it some time to load
    time.sleep(5)
    
    # check if there's a captcha
    print("Checking for CAPTCHA...")
    try:
        captcha_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Security Check') or contains(text(), 'security check') or contains(@class, 'recaptcha') or contains(@id, 'recaptcha') or contains(text(), 'checkpoint')]")
        if captcha_elements:
            print("⚠️ CAPTCHA detected!")
            input("Please solve the CAPTCHA manually in the browser, then press Enter here...")
            print("✓ Continuing after CAPTCHA...")
            time.sleep(3)
    except:
        pass
    
    # click continue as button on facebook
    print("Looking for Facebook consent button...")
    if wait_and_click(driver, By.XPATH, "//div[@role='button' and contains(., 'Continue as')]", timeout=15):
        print("✓ Facebook consent granted")
        time.sleep(3)
    
    # go back to main tinder window
    print("Switching back to Tinder...")
    driver.switch_to.window(base_window)
    print("✓ Back on Tinder main window")
    time.sleep(3)
    
    # check if phone verification is needed
    print("Checking for phone verification...")
    try:
        phone_field = wait_for_element(driver, By.XPATH, "//input[@type='tel' or @id='phone_number']", timeout=5)
        if phone_field:
            print("Phone verification required")
            phone_field.clear()
            phone_field.send_keys(My_Number)
            print("✓ Phone number entered")
            
            # click continue
            if wait_and_click(driver, By.XPATH, "//button[contains(., 'Continue') or contains(., 'Next')]", timeout=5):
                print("✓ Phone submission clicked")
                time.sleep(3)
                
                print("\n⚠️ VERIFICATION CODE REQUIRED")
                print("👉 Enter the OTP code in the browser, then press Enter here")
                print("    (I will click the submit button for you)\n")
                input("Press Enter AFTER entering the OTP code...")
                
                # try to click submit automatically
                print("Looking for OTP submit button...")
                if wait_and_click(driver, By.XPATH, '//*[@id="q484845104"]/div/div/div[2]/div[2]/div[4]/button', timeout=5):
                    print("✓ OTP submit button clicked")
                else:
                    print("⚠️ Could not find submit button automatically")
                    print("Please click the 'Next' button manually in the browser now")
                    input("Press Enter after clicking the button...")
                
                # wait for verification to complete
                print("Waiting for OTP verification to complete...")
                time.sleep(5)
                
                # make sure we moved past the OTP screen
                try:
                    WebDriverWait(driver, 10).until_not(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or contains(@placeholder, 'code')]"))
                    )
                    print("✓ OTP verified successfully")
                except TimeoutException:
                    print("⚠️ Still on OTP screen - waiting a bit longer...")
                    time.sleep(5)
    except TimeoutException:
        print("✓ No phone verification needed")
    
    time.sleep(3)
    
    # handle location permission popup
    print("Checking for location permission...")
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Allow')]", timeout=3):
        print("✓ Location permission granted")
        time.sleep(2)
    
    # handle notification popup
    print("Checking for notification permission...")
    clicked_notify = False
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Notify me')]", timeout=5):
        print("✓ Notifications enabled (Notify me)")
        time.sleep(3)
        clicked_notify = True
    
    if not clicked_notify:
        if wait_and_click(driver, By.XPATH, "//button[contains(., \"I'll miss out\")]", timeout=3):
            print("✓ Skipped notifications (I'll miss out)")
            time.sleep(2)
    
    # skip face verification if it pops up
    print("Checking for face verification screen...")
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Maybe later')]", timeout=5):
        print("✓ Face verification skipped (Maybe later)")
        time.sleep(3)
    
    # dismiss any random popups
    print("Checking for additional popups...")
    if wait_and_click(driver, By.XPATH, "//button[contains(., 'Not interested')]", timeout=3):
        print("✓ Additional popup dismissed")
        time.sleep(2)
    
    print("\n✅ Login complete! Ready for automation.")
    
    # now let's start swiping - REJECT ONLY
    print("Starting to REJECT profiles automatically...")
    swipe_count = 0
    max_swipes = 50  # safety limit
    
    while swipe_count < max_swipes:
        try:
            time.sleep(2)  # wait for profile to load
            
            # Multiple selectors for reject button (Nope/Dislike)
            reject_selectors = [
                '//button[contains(@aria-label, "Nope")]',
                '//button[contains(@data-testid, "dislike")]',
                '//button[contains(@title, "Nope")]',
                '//button[.//*[contains(text(), "Nope")]]',
                '//button[.//*[contains(@aria-label, "Nope")]]',
                '//button[contains(@class, "button") and contains(@class, "dislike")]',
                '//span[contains(text(), "Nope")]/ancestor::button',
                '//button[contains(., "Nope")]',
                '//button[contains(@class, "dislike")]',
            ]
            
            reject_clicked = False
            
            # Try each selector until one works
            for selector in reject_selectors:
                try:
                    reject_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    reject_btn.click()
                    swipe_count += 1
                    print(f"✓ Swipe {swipe_count}: REJECTED ❌")
                    reject_clicked = True
                    break
                except:
                    continue
            
            # If no reject button found, try pressing Escape key as fallback
            if not reject_clicked:
                from selenium.webdriver.common.keys import Keys
                try:
                    body = driver.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.ESCAPE)  # Escape key often rejects
                    swipe_count += 1
                    print(f"✓ Swipe {swipe_count}: REJECTED (ESC key) ❌")
                    reject_clicked = True
                except:
                    pass
            
            # If still no success, wait and try again
            if not reject_clicked:
                print(f"⚠️ Could not find reject button for swipe {swipe_count + 1}, waiting...")
                time.sleep(3)
                
                # Check if we're out of swipes or have a popup
                try:
                    out_of_swipes = driver.find_elements(By.XPATH, "//*[contains(text(), 'out of likes') or contains(text(), 'See Who Likes You')]")
                    if out_of_swipes:
                        print("🚫 Out of swipes for today!")
                        break
                except:
                    pass
                
        except Exception as e:
            print(f"❌ Error on swipe {swipe_count + 1}: {str(e)[:100]}")
            time.sleep(2)
            
            # Check for common popups and close them
            popup_selectors = [
                "//button[contains(., 'Maybe Later')]",
                "//button[contains(., 'Not interested')]",
                "//button[contains(., 'No Thanks')]",
                "//button[@aria-label='Close']",
                "//button[contains(@class, 'close')]"
            ]
            
            for selector in popup_selectors:
                try:
                    close_btn = driver.find_element(By.XPATH, selector)
                    close_btn.click()
                    print("✓ Closed popup")
                    time.sleep(1)
                    break
                except:
                    continue
    
    print(f"\n✅ Finished! Rejected {swipe_count} profiles.")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    # keep browser open so we can see what happened
    print("\nScript finished. Browser will remain open.")
    input("Press Enter to close the browser...")
    driver.quit()