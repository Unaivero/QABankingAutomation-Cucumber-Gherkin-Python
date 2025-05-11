from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class MobileLoginPage:
    """Page object for the mobile login page."""
    
    # Common Locators (for both Android and iOS)
    LOGIN_TITLE = (MobileBy.XPATH, "//android.widget.TextView[@text='Welcome to MyBank']|//XCUIElementTypeStaticText[@name='Welcome to MyBank']")
    
    # Android-specific Locators
    USERNAME_INPUT_ANDROID = (MobileBy.ID, "com.mybank.banking:id/usernameInput")
    PASSWORD_INPUT_ANDROID = (MobileBy.ID, "com.mybank.banking:id/passwordInput")
    LOGIN_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/loginButton")
    BIOMETRIC_LOGIN_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/biometricLoginButton")
    FORGOT_PASSWORD_LINK_ANDROID = (MobileBy.ID, "com.mybank.banking:id/forgotPasswordLink")
    FORGOT_USERNAME_LINK_ANDROID = (MobileBy.ID, "com.mybank.banking:id/forgotUsernameLink")
    REGISTER_LINK_ANDROID = (MobileBy.ID, "com.mybank.banking:id/registerLink")
    ERROR_MESSAGE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/errorMessage")
    
    # iOS-specific Locators
    USERNAME_INPUT_IOS = (MobileBy.ACCESSIBILITY_ID, "usernameInput")
    PASSWORD_INPUT_IOS = (MobileBy.ACCESSIBILITY_ID, "passwordInput")
    LOGIN_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "loginButton")
    BIOMETRIC_LOGIN_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "biometricLoginButton")
    FORGOT_PASSWORD_LINK_IOS = (MobileBy.ACCESSIBILITY_ID, "forgotPasswordLink")
    FORGOT_USERNAME_LINK_IOS = (MobileBy.ACCESSIBILITY_ID, "forgotUsernameLink")
    REGISTER_LINK_IOS = (MobileBy.ACCESSIBILITY_ID, "registerLink")
    ERROR_MESSAGE_IOS = (MobileBy.ACCESSIBILITY_ID, "errorMessage")
    
    def __init__(self, driver):
        """Initialize the login page with Appium driver."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('mobile_login_page')
        
        # Determine platform
        self.is_android = 'platformName' in driver.capabilities and driver.capabilities['platformName'].lower() == 'android'
        self.logger.info(f"Initialized mobile login page (Platform: {'Android' if self.is_android else 'iOS'})")
    
    def is_login_page_displayed(self):
        """Check if the login page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_TITLE))
            return True
        except TimeoutException:
            return False
    
    def enter_username(self, username):
        """Enter username in the username field."""
        locator = self.USERNAME_INPUT_ANDROID if self.is_android else self.USERNAME_INPUT_IOS
        username_field = self.wait.until(EC.element_to_be_clickable(locator))
        username_field.clear()
        username_field.send_keys(username)
        self.logger.info(f"Entered username: {username}")
    
    def enter_password(self, password):
        """Enter password in the password field."""
        locator = self.PASSWORD_INPUT_ANDROID if self.is_android else self.PASSWORD_INPUT_IOS
        password_field = self.wait.until(EC.element_to_be_clickable(locator))
        password_field.clear()
        password_field.send_keys(password)
        self.logger.info("Entered password (masked)")
    
    def tap_login_button(self):
        """Tap the login button."""
        locator = self.LOGIN_BUTTON_ANDROID if self.is_android else self.LOGIN_BUTTON_IOS
        login_button = self.wait.until(EC.element_to_be_clickable(locator))
        login_button.click()
        self.logger.info("Tapped login button")
    
    def tap_biometric_login_button(self):
        """Tap the biometric login button."""
        locator = self.BIOMETRIC_LOGIN_BUTTON_ANDROID if self.is_android else self.BIOMETRIC_LOGIN_BUTTON_IOS
        biometric_button = self.wait.until(EC.element_to_be_clickable(locator))
        biometric_button.click()
        self.logger.info("Tapped biometric login button")
    
    def tap_forgot_password_link(self):
        """Tap the 'Forgot Password' link."""
        locator = self.FORGOT_PASSWORD_LINK_ANDROID if self.is_android else self.FORGOT_PASSWORD_LINK_IOS
        forgot_password = self.wait.until(EC.element_to_be_clickable(locator))
        forgot_password.click()
        self.logger.info("Tapped 'Forgot Password' link")
    
    def tap_forgot_username_link(self):
        """Tap the 'Forgot Username' link."""
        locator = self.FORGOT_USERNAME_LINK_ANDROID if self.is_android else self.FORGOT_USERNAME_LINK_IOS
        forgot_username = self.wait.until(EC.element_to_be_clickable(locator))
        forgot_username.click()
        self.logger.info("Tapped 'Forgot Username' link")
    
    def tap_register_link(self):
        """Tap the 'Register' link."""
        locator = self.REGISTER_LINK_ANDROID if self.is_android else self.REGISTER_LINK_IOS
        register = self.wait.until(EC.element_to_be_clickable(locator))
        register.click()
        self.logger.info("Tapped 'Register' link")
    
    def get_error_message(self):
        """Get the error message displayed on failed login."""
        try:
            locator = self.ERROR_MESSAGE_ANDROID if self.is_android else self.ERROR_MESSAGE_IOS
            error_element = self.wait.until(EC.visibility_of_element_located(locator))
            error_text = error_element.text
            self.logger.info(f"Error message displayed: {error_text}")
            return error_text
        except TimeoutException:
            self.logger.info("No error message displayed")
            return ""
    
    def is_error_message_displayed(self):
        """Check if an error message is displayed."""
        return self.get_error_message() != ""
    
    def mock_successful_biometric_auth(self):
        """Mock a successful biometric authentication (for testing in emulators)."""
        if self.is_android:
            # For Android emulator, we need to handle the system dialog
            try:
                # Different approaches might be needed depending on emulator version
                # This is an example for Android emulator
                if 'fingerprint' in self.driver.capabilities.get('deviceScreenSize', ''):
                    # Use fingerprint authentication API for newer Android versions
                    self.driver.fingerprint(1)  # 1 is typically a valid fingerprint ID
                else:
                    # Handle dialog for older versions
                    allow_button = self.driver.find_element(MobileBy.ID, "android:id/button1")
                    allow_button.click()
                self.logger.info("Mocked successful Android biometric authentication")
            except Exception as e:
                self.logger.warning(f"Could not mock Android biometric auth: {e}")
        else:
            # For iOS Simulator
            try:
                # iOS simulators have different methods for TouchID/FaceID
                self.driver.execute_script("mobile: enrollBiometric", {"isEnabled": True})
                self.driver.execute_script("mobile: sendBiometricMatch", {"type": "touchId", "match": True})
                self.logger.info("Mocked successful iOS biometric authentication")
            except Exception as e:
                self.logger.warning(f"Could not mock iOS biometric auth: {e}")
    
    def login(self, username, password):
        """Perform login with username and password."""
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login_button()
        self.logger.info(f"Attempted login with username: {username}")
