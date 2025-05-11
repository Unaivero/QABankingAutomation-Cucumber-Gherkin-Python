from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import json
import tempfile

logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}

def get_android_driver(context):
    """Initialize and return Android driver for Appium."""
    config = load_config()
    mobile_config = config.get('mobile', {})
    
    # Override with context user data if available
    app_package = context.config.userdata.get('android_app_package', 
                                            mobile_config.get('android_app_package', 'com.mybank.banking'))
    app_activity = context.config.userdata.get('android_app_activity', 
                                             mobile_config.get('android_app_activity', 'com.mybank.banking.MainActivity'))
    appium_server = context.config.userdata.get('appium_server_url', 
                                              mobile_config.get('appium_server_url', 'http://localhost:4723/wd/hub'))
    
    # Setup desired capabilities
    desired_caps = {
        'platformName': 'Android',
        'deviceName': context.config.userdata.get('android_device_name', 'Android Emulator'),
        'appPackage': app_package,
        'appActivity': app_activity,
        'automationName': 'UiAutomator2',
        'newCommandTimeout': 300,
        'noReset': False,  # Set to True to maintain app state between sessions
        'fullReset': False  # Set to True for a complete reset (uninstall/install)
    }
    
    # Add additional capabilities from config
    additional_caps = context.config.userdata.get('android_capabilities', {})
    desired_caps.update(additional_caps)
    
    logger.info(f"Initializing Android driver with capabilities: {desired_caps}")
    
    try:
        driver = webdriver.Remote(appium_server, desired_caps)
        driver.implicitly_wait(10)
        logger.info("Android driver initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Android driver: {e}")
        raise

def get_ios_driver(context):
    """Initialize and return iOS driver for Appium."""
    config = load_config()
    mobile_config = config.get('mobile', {})
    
    # Override with context user data if available
    bundle_id = context.config.userdata.get('ios_bundle_id', 
                                          mobile_config.get('ios_bundle_id', 'com.mybank.banking'))
    appium_server = context.config.userdata.get('appium_server_url', 
                                              mobile_config.get('appium_server_url', 'http://localhost:4723/wd/hub'))
    
    # Setup desired capabilities
    desired_caps = {
        'platformName': 'iOS',
        'deviceName': context.config.userdata.get('ios_device_name', 'iPhone Simulator'),
        'platformVersion': context.config.userdata.get('ios_platform_version', '16.0'),
        'bundleId': bundle_id,
        'automationName': 'XCUITest',
        'newCommandTimeout': 300,
        'noReset': False,  # Set to True to maintain app state between sessions
        'fullReset': False  # Set to True for a complete reset
    }
    
    # Add additional capabilities from config
    additional_caps = context.config.userdata.get('ios_capabilities', {})
    desired_caps.update(additional_caps)
    
    logger.info(f"Initializing iOS driver with capabilities: {desired_caps}")
    
    try:
        driver = webdriver.Remote(appium_server, desired_caps)
        driver.implicitly_wait(10)
        logger.info("iOS driver initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize iOS driver: {e}")
        raise

def take_screenshot(driver, scenario_name, step_name=None):
    """Take a screenshot and save it to a temporary file."""
    try:
        # Create a temp dir if it doesn't exist
        screenshot_dir = os.path.join(tempfile.gettempdir(), 'mobile_screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generate filename
        import time
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        scenario_name = scenario_name.replace(' ', '_').replace('/', '_')
        
        if step_name:
            step_name = step_name.replace(' ', '_').replace('/', '_')
            filename = f"{timestamp}_{scenario_name}_{step_name}.png"
        else:
            filename = f"{timestamp}_{scenario_name}.png"
        
        filepath = os.path.join(screenshot_dir, filename)
        
        # Take the screenshot
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved to {filepath}")
        
        return filepath
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        return None

def close_driver(driver):
    """Safely close the driver."""
    try:
        if driver:
            driver.quit()
            logger.info("Mobile driver closed successfully")
    except Exception as e:
        logger.error(f"Error closing mobile driver: {e}")

def handle_unexpected_alert(driver):
    """Handle any unexpected alerts that might appear."""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        logger.warning(f"Unexpected alert found: {alert_text}")
        alert.accept()
        logger.info("Alert accepted")
        return True
    except:
        return False

def wait_for_element(driver, locator, timeout=10):
    """Wait for an element to be visible and return it."""
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))
    return element

def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    """Wait for an element to be clickable and return it."""
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))
    return element

def scroll_to_text(driver, text):
    """Scroll to find text (Android)."""
    try:
        if hasattr(driver, 'find_element_by_android_uiautomator'):
            driver.find_element_by_android_uiautomator(
                f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView('
                f'new UiSelector().textContains("{text}").instance(0))'
            )
            logger.info(f"Scrolled to text: {text}")
            return True
        else:
            # For newer Appium versions
            driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 
                              f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView('
                              f'new UiSelector().textContains("{text}").instance(0))')
            logger.info(f"Scrolled to text: {text}")
            return True
    except Exception as e:
        logger.error(f"Failed to scroll to text '{text}': {e}")
        return False

def swipe(driver, start_x, start_y, end_x, end_y, duration=None):
    """Perform a swipe gesture."""
    try:
        if duration is None:
            driver.swipe(start_x, start_y, end_x, end_y)
        else:
            driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        return True
    except Exception as e:
        logger.error(f"Failed to perform swipe: {e}")
        return False

def swipe_down(driver):
    """Swipe down on the screen."""
    size = driver.get_window_size()
    start_x = size['width'] // 2
    start_y = size['height'] // 3
    end_y = size['height'] * 2 // 3
    
    return swipe(driver, start_x, start_y, start_x, end_y)

def swipe_up(driver):
    """Swipe up on the screen."""
    size = driver.get_window_size()
    start_x = size['width'] // 2
    start_y = size['height'] * 2 // 3
    end_y = size['height'] // 3
    
    return swipe(driver, start_x, start_y, start_x, end_y)

def tap_back_button(driver):
    """Tap the back button (Android)."""
    try:
        driver.press_keycode(4)  # Android back button keycode
        logger.info("Tapped back button")
        return True
    except Exception as e:
        logger.error(f"Failed to tap back button: {e}")
        return False

def enable_network_connection(driver, airplane_mode=False, wifi=True, data=True):
    """Set network connection settings."""
    try:
        # Create network bitmap (0: None, 1: Airplane Mode, 2: Wifi, 4: Data)
        mode = 0
        if airplane_mode:
            mode += 1
        if wifi:
            mode += 2
        if data:
            mode += 4
        
        driver.set_network_connection(mode)
        logger.info(f"Set network connection to: airplane={airplane_mode}, wifi={wifi}, data={data}")
        return True
    except Exception as e:
        logger.error(f"Failed to set network connection: {e}")
        return False
