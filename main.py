from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
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
    
    # find and click login - with multiple selectors
    print("Looking for login button...")
    login_selectors = [
        "//a[contains(., 'Log in')]",
        "//button[contains(., 'Log in')]",
        "//span[contains(., 'Log in')]/parent::button",
        "//a[@href='/login']",
        "//button[@data-testid='loginButton']"
    ]
    
    login_clicked = False
    for selector in login_selectors:
        if wait_and_click(driver, By.XPATH, selector, timeout=3):
            print("✓ Login button clicked")
            login_clicked = True
            time.sleep(2)
            break
    
    if not login_clicked:
        print("❌ Could not find login button")
        raise Exception("Login button not found")
    
    # use facebook login - with multiple selectors
    print("Looking for Facebook login option...")
    facebook_selectors = [
        "//button[contains(., 'Facebook')]",
        "//span[contains(., 'Facebook')]/parent::button",
        "//button[contains(@aria-label, 'Facebook')]",
        "//div[contains(., 'Facebook')]/ancestor::button",
        "//button[@data-testid='facebookLogin']"
    ]
    
    facebook_clicked = False
    for selector in facebook_selectors:
        if wait_and_click(driver, By.XPATH, selector, timeout=5):
            print("✓ Facebook login clicked")
            facebook_clicked = True
            time.sleep(3)
            break
    
    if not facebook_clicked:
        print("❌ Could not find Facebook login button")
        # Try to see what login options are available
        print("Available login options:")
        try:
            login_options = driver.find_elements(By.XPATH, "//button | //a[contains(., 'Log')]")
            for option in login_options:
                print(f" - {option.text}")
        except:
            pass
        raise Exception("Facebook login button not found")
    
    # wait for fb popup to appear with longer timeout
    print("Waiting for Facebook login popup...")
    try:
        WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
        print("✓ Facebook popup detected")
    except TimeoutException:
        print("❌ Facebook popup did not appear")
        print("Current window handles:", len(driver.window_handles))
        raise Exception("Facebook login popup timeout")
    
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
    else:
        print("❌ Could not find email field")
        # Try alternative selectors for email
        alt_email_selectors = ["//input[@name='email']", "//input[@type='email']"]
        for selector in alt_email_selectors:
            email_field = wait_for_element(driver, By.XPATH, selector, timeout=3)
            if email_field:
                email_field.clear()
                email_field.send_keys(FB_Email)
                print("✓ Email entered (alternative selector)")
                break
    
    # fill in password
    print("Entering Facebook password...")
    password_field = wait_for_element(driver, By.ID, "pass", timeout=10)
    if password_field:
        password_field.clear()
        password_field.send_keys(FB_Password)
        print("✓ Password entered")
    else:
        print("❌ Could not find password field")
        # Try alternative selectors for password
        alt_password_selectors = ["//input[@name='pass']", "//input[@type='password']"]
        for selector in alt_password_selectors:
            password_field = wait_for_element(driver, By.XPATH, selector, timeout=3)
            if password_field:
                password_field.clear()
                password_field.send_keys(FB_Password)
                print("✓ Password entered (alternative selector)")
                break
    
    # submit the login form
    print("Clicking Facebook login button...")
    login_button_selectors = [
        "input[type='submit']",
        "button[type='submit']",
        "//button[contains(., 'Log In')]",
        "//input[contains(@value, 'Log In')]"
    ]
    
    login_submitted = False
    for selector in login_button_selectors:
        if wait_and_click(driver, By.CSS_SELECTOR if '[' in selector else By.XPATH, selector, timeout=5):
            print("✓ Facebook login submitted")
            login_submitted = True
            break
    
    if not login_submitted:
        print("⚠️ Could not find login button, trying to submit form by pressing Enter...")
        try:
            password_field.send_keys(Keys.ENTER)
            print("✓ Login submitted via Enter key")
        except:
            print("❌ Could not submit login form")
    
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
                
                # Better OTP submit button selectors
                otp_selectors = [
                    "//button[contains(., 'Submit')]",
                    "//button[contains(., 'Verify')]",
                    "//button[contains(., 'Next')]",
                    "//button[@type='submit']",
                    "//button[contains(@class, 'button') and contains(., 'Continue')]"
                ]
                
                otp_submitted = False
                for selector in otp_selectors:
                    if wait_and_click(driver, By.XPATH, selector, timeout=3):
                        print("✓ OTP submit button clicked")
                        otp_submitted = True
                        break
                
                if not otp_submitted:
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
    
    # Improved popup handling with more selectors
    popups_to_handle = [
        ("location permission", "//button[contains(., 'Allow')]", 3),
        ("notification permission", "//button[contains(., 'Notify me')]", 3),
        ("notification skip", "//button[contains(., \"I'll miss out\") or contains(., 'Not interested')]", 3),
        ("face verification", "//button[contains(., 'Maybe later') or contains(., 'Skip')]", 3),
        ("premium offer", "//button[contains(., 'No Thanks') or contains(., 'Continue')]", 3),
        ("close popup", "//button[@aria-label='Close']", 3),
        ("close popup", "//button[contains(@class, 'close')]", 3)
    ]
    
    for popup_name, selector, timeout in popups_to_handle:
        print(f"Checking for {popup_name}...")
        if wait_and_click(driver, By.XPATH, selector, timeout):
            print(f"✓ {popup_name} handled")
            time.sleep(2)
    
    print("\n✅ Login complete! Ready for automation.")
    
    # now let's start swiping - LIKE ONLY
    print("Starting to LIKE profiles automatically...")
    swipe_count = 0
    max_swipes = 100  # increased limit since you're liking
    
    while swipe_count < max_swipes:
        try:
            time.sleep(1.5)  # reduced wait time for faster swiping
            
            # Multiple selectors for like button (Like)
            like_selectors = [
                '//*[@id="main-content"]/div[1]/div/div/div/div[1]/div/div/div[5]/div/div[4]/button',  # Your specific XPath
                '//button[contains(@aria-label, "Like")]',
                '//button[contains(@data-testid, "like")]',
                '//button[contains(@title, "Like")]',
                '//button[.//*[contains(text(), "Like")]]',
                '//button[.//*[contains(@aria-label, "Like")]]',
                '//button[contains(@class, "button") and contains(@class, "like")]',
                '//span[contains(text(), "Like")]/ancestor::button',
                '//button[contains(., "Like")]',
                '//button[contains(@class, "like")]',
                # Additional selectors for different Tinder layouts
                '//button[contains(@data-test-id, "gamepadLike")]',
                '//button[contains(@aria-label, "Add to Likes")]',
            ]
            
            like_clicked = False
            
            # Try each selector until one works
            for selector in like_selectors:
                try:
                    like_btn = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    like_btn.click()
                    swipe_count += 1
                    print(f"✓ Swipe {swipe_count}: LIKED ❤️")
                    like_clicked = True
                    break
                except:
                    continue
            
            # If no like button found, try pressing Right Arrow key as fallback
            if not like_clicked:
                try:
                    body = driver.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.ARROW_RIGHT)  # Right arrow often likes
                    swipe_count += 1
                    print(f"✓ Swipe {swipe_count}: LIKED (Right Arrow) ❤️")
                    like_clicked = True
                except:
                    pass
            
            # If still no success, check for various conditions
            if not like_clicked:
                print(f"⚠️ Could not find like button for swipe {swipe_count + 1}, checking for issues...")
                time.sleep(2)
                
                # Check if we're out of likes
                try:
                    out_of_likes = driver.find_elements(By.XPATH, "//*[contains(text(), 'out of likes') or contains(text(), 'See Who Likes You') or contains(text(), 'Get Tinder Gold')]")
                    if out_of_likes:
                        print("🚫 Out of likes for today!")
                        break
                except:
                    pass
                
                # Check for match popup
                try:
                    match_popup = driver.find_elements(By.XPATH, "//*[contains(text(), 'It\'s a Match') or contains(text(), 'You matched')]")
                    if match_popup:
                        print("🎉 MATCH! Closing popup...")
                        # Try to close match popup
                        body.send_keys(Keys.ESCAPE)
                        time.sleep(1)
                        continue
                except:
                    pass
                
                # Check for any other popups
                popup_closed = False
                popup_selectors = [
                    "//button[contains(., 'Maybe Later')]",
                    "//button[contains(., 'Not interested')]",
                    "//button[contains(., 'No Thanks')]",
                    "//button[@aria-label='Close']",
                    "//button[contains(@class, 'close')]",
                    "//button[contains(., 'Keep Swiping')]"
                ]
                
                for selector in popup_selectors:
                    try:
                        close_btn = driver.find_element(By.XPATH, selector)
                        close_btn.click()
                        print("✓ Closed popup")
                        popup_closed = True
                        time.sleep(1)
                        break
                    except:
                        continue
                
                if popup_closed:
                    continue
                
                print("⏳ Waiting a bit longer and retrying...")
                time.sleep(3)
                
        except Exception as e:
            print(f"❌ Error on swipe {swipe_count + 1}: {str(e)[:100]}")
            time.sleep(2)
            
            # Try to recover by pressing Escape
            try:
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.ESCAPE)
                time.sleep(1)
            except:
                pass
    
    print(f"\n✅ Finished! Liked {swipe_count} profiles.")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    # keep browser open so we can see what happened
    print("\nScript finished. Browser will remain open.")
    input("Press Enter to close the browser...")
    driver.quit()
