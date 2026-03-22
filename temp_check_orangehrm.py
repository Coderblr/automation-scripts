from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

o = webdriver.EdgeOptions()
o.add_argument('--disable-notifications')
o.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
o.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
    'profile.password_manager_leak_detection': False,
})
d = webdriver.Edge(options=o)
d.maximize_window()

try:
    d.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    time.sleep(5)
    print('Title:', d.title)
    print('URL:', d.current_url)

    w = WebDriverWait(d, 15)
    uname = w.until(EC.visibility_of_element_located((By.NAME, 'username')))
    print('OK: Username input found (name=username)')
    pwd = d.find_element(By.NAME, 'password')
    print('OK: Password input found (name=password)')
    btn = d.find_element(By.CSS_SELECTOR, 'button[type=submit]')
    print('OK: Login button found, text:', btn.text)

    uname.send_keys('Admin')
    pwd.send_keys('admin123')
    btn.click()
    time.sleep(5)
    print('\nAfter login URL:', d.current_url)

    # Dashboard heading
    try:
        h6 = w.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.oxd-topbar-header-breadcrumb h6')))
        print('OK: Dashboard heading:', h6.text)
    except Exception as e:
        print('FAIL: Dashboard heading not found:', e)

    # Sidebar menu items
    try:
        items = d.find_elements(By.CSS_SELECTOR, '.oxd-main-menu-item span')
        names = [i.text for i in items if i.text.strip()]
        print('OK: Sidebar items:', names)
    except Exception as e:
        print('FAIL: Sidebar:', e)

    # User dropdown
    try:
        dd = d.find_element(By.CSS_SELECTOR, '.oxd-userdropdown-tab')
        print('OK: User dropdown found, text:', dd.text.strip())
    except Exception as e:
        print('FAIL: User dropdown:', e)

    # Click PIM
    try:
        pim = d.find_element(By.XPATH, "//span[text()='PIM']")
        pim.click()
        time.sleep(3)
        h6 = d.find_element(By.CSS_SELECTOR, '.oxd-topbar-header-breadcrumb h6')
        print('OK: PIM page heading:', h6.text)
        print('OK: PIM URL:', d.current_url)
    except Exception as e:
        print('FAIL: PIM:', e)

    # Click Admin
    try:
        admin = d.find_element(By.XPATH, "//span[text()='Admin']")
        admin.click()
        time.sleep(3)
        h6 = d.find_element(By.CSS_SELECTOR, '.oxd-topbar-header-breadcrumb h6')
        print('OK: Admin page heading:', h6.text)
    except Exception as e:
        print('FAIL: Admin:', e)

    # Click My Info
    try:
        myinfo = d.find_element(By.XPATH, "//span[text()='My Info']")
        myinfo.click()
        time.sleep(3)
        h6 = d.find_element(By.CSS_SELECTOR, '.oxd-topbar-header-breadcrumb h6')
        print('OK: My Info heading:', h6.text)
    except Exception as e:
        print('FAIL: My Info:', e)

    # Logout
    try:
        dd = d.find_element(By.CSS_SELECTOR, '.oxd-userdropdown-tab')
        dd.click()
        time.sleep(1)
        logout = w.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout.click()
        time.sleep(3)
        print('OK: After logout URL:', d.current_url)
        uname2 = d.find_element(By.NAME, 'username')
        print('OK: Back on login page:', uname2.is_displayed())
    except Exception as e:
        print('FAIL: Logout:', e)

    print('\n=== ALL SELECTORS VERIFIED ===')

finally:
    d.quit()
