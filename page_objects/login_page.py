from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class LoginPage:
    """Page object for the login page of the MyBank application."""
    
    # Locators - updated to match realistic web application selectors
    USERNAME_INPUT = (By.ID, "login-username")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "btn-login")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Forgot Password')]")
    FORGOT_USERNAME_LINK = (By.XPATH, "//a[contains(text(), 'Forgot Username')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Register')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "login-error-message")
    ACCOUNT_LOCKED_MESSAGE = (By.ID, "account-locked-message")
    
    # 2FA Elements
    TOTP_INPUT = (By.ID, "security-code")
    TOTP_SUBMIT_BUTTON = (By.ID, "verify-code-btn")
    TOTP_RESEND_BUTTON = (By.ID, "resend-code-btn")
    TOTP_HELP_LINK = (By.ID, "2fa-help-link")
    
    # Biometric Elements
    BIOMETRIC_PROMPT = (By.ID, "biometric-auth-prompt")
    USE_PASSWORD_INSTEAD_LINK = (By.ID, "use-password-link")
    
    # Security Questions Elements
    SECURITY_QUESTION_TEXT = (By.ID, "security-question")
    SECURITY_ANSWER_INPUT = (By.ID, "security-answer")
    SECURITY_SUBMIT_BUTTON = (By.ID, "verify-answer-btn")
    
    def __init__(self, driver):
        """Initialize the login page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('login_page')
    
    def navigate(self):
        """Navigate to the login page."""
        base_url = self.driver.base_url if hasattr(self.driver, 'base_url') else "https://mybank.example.com"
        self.driver.get(f"{base_url}/login")
        self.logger.info("Navigated to login page")
        return self
    
    def is_login_page_displayed(self):
        """Check if the login page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            self.logger.info("Login page is displayed")
            return True
        except TimeoutException:
            self.logger.warning("Login page is not displayed")
            return False
    
    def enter_username(self, username):
        """Enter username in the username field."""
        username_element = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        username_element.clear()
        username_element.send_keys(username)
        self.logger.info(f"Entered username: {username}")
        return self
    
    def enter_password(self, password):
        """Enter password in the password field."""
        password_element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        password_element.clear()
        password_element.send_keys(password)
        self.logger.info("Entered password (masked)")
        return self
    
    def check_remember_me(self, check=True):
        """Check or uncheck the 'Remember Me' checkbox."""
        remember_me = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        is_checked = remember_me.is_selected()
        
        if (check and not is_checked) or (not check and is_checked):
            remember_me.click()
            self.logger.info(f"Remember Me checkbox {'checked' if check else 'unchecked'}")
        
        return self
    
    def click_login_button(self):
        """Click the login button."""
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()
        self.logger.info("Clicked login button")
        return self
    
    def click_forgot_password(self):
        """Click the 'Forgot Password' link."""
        forgot_password = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_password.click()
        self.logger.info("Clicked 'Forgot Password' link")
        from page_objects.forgot_password_page import ForgotPasswordPage
        return ForgotPasswordPage(self.driver)
    
    def click_forgot_username(self):
        """Click the 'Forgot Username' link."""
        forgot_username = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        forgot_username.click()
        self.logger.info("Clicked 'Forgot Username' link")
        from page_objects.forgot_username_page import ForgotUsernamePage
        return ForgotUsernamePage(self.driver)
    
    def click_register(self):
        """Click the 'Register' link."""
        register = self.wait.until(EC.element_to_be_clickable(self.REGISTER_LINK))
        register.click()
        self.logger.info("Clicked 'Register' link")
        from page_objects.registration_page import RegistrationPage
        return RegistrationPage(self.driver)
    
    def login(self, username, password, remember_me=False):
        """Perform login with given credentials."""
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            self.check_remember_me(True)
        self.click_login_button()
        self.logger.info(f"Attempted login with username: {username}")
        
        # Detect if we need to handle 2FA
        try:
            if self.is_2fa_input_displayed():
                self.logger.info("2FA prompt detected")
                return self  # Return self for handling 2FA
            elif self.is_security_question_displayed():
                self.logger.info("Security question prompt detected")
                return self  # Return self for handling security question
            elif self.is_biometric_prompt_displayed():
                self.logger.info("Biometric prompt detected")
                return self  # Return self for handling biometric prompt
        except (TimeoutException, NoSuchElementException):
            pass
        
        # If no special authentication method needed, check for success/error
        if self.is_error_message_displayed():
            self.logger.warning(f"Login failed. Error: {self.get_error_message()}")
            return self
        
        # If we got here, login was likely successful
        self.logger.info("Login successful")
        from page_objects.dashboard_page import DashboardPage
        return DashboardPage(self.driver)
    
    def get_error_message(self):
        """Get the error message displayed on failed login."""
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            error_text = error_element.text
            self.logger.info(f"Error message displayed: {error_text}")
            return error_text
        except TimeoutException:
            self.logger.info("No error message displayed")
            return ""
    
    def is_error_message_displayed(self):
        """Check if an error message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except TimeoutException:
            return False
    
    def is_account_locked_message_displayed(self):
        """Check if account locked message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_LOCKED_MESSAGE))
            self.logger.warning("Account locked message displayed")
            return True
        except TimeoutException:
            return False
    
    # 2FA Methods
    def is_2fa_input_displayed(self):
        """Check if 2FA input is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOTP_INPUT))
            return True
        except TimeoutException:
            return False
    
    def enter_2fa_code(self, code):
        """Enter 2FA code."""
        totp_input = self.wait.until(EC.element_to_be_clickable(self.TOTP_INPUT))
        totp_input.clear()
        totp_input.send_keys(code)
        self.logger.info(f"Entered 2FA code: {code}")
        return self
    
    def submit_2fa_code(self):
        """Submit 2FA code."""
        totp_submit = self.wait.until(EC.element_to_be_clickable(self.TOTP_SUBMIT_BUTTON))
        totp_submit.click()
        self.logger.info("Submitted 2FA code")
        
        # Check if login was successful or not
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            self.logger.warning(f"2FA verification failed. Error: {error.text}")
            return self
        except TimeoutException:
            # If no error, assume success
            self.logger.info("2FA verification successful")
            from page_objects.dashboard_page import DashboardPage
            return DashboardPage(self.driver)
    
    def click_resend_2fa_code(self):
        """Click the 'Resend Code' button."""
        resend_button = self.wait.until(EC.element_to_be_clickable(self.TOTP_RESEND_BUTTON))
        resend_button.click()
        self.logger.info("Clicked 'Resend Code' button")
        return self
    
    # Security Question Methods
    def is_security_question_displayed(self):
        """Check if security question is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SECURITY_QUESTION_TEXT))
            return True
        except TimeoutException:
            return False
    
    def get_security_question(self):
        """Get the text of the security question."""
        question_element = self.wait.until(EC.visibility_of_element_located(self.SECURITY_QUESTION_TEXT))
        return question_element.text
    
    def answer_security_question(self, answer):
        """Enter and submit security question answer."""
        question = self.get_security_question()
        self.logger.info(f"Answering security question: {question}")
        
        answer_input = self.wait.until(EC.element_to_be_clickable(self.SECURITY_ANSWER_INPUT))
        answer_input.clear()
        answer_input.send_keys(answer)
        
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SECURITY_SUBMIT_BUTTON))
        submit_button.click()
        
        self.logger.info("Submitted security question answer")
        
        # Check if verification was successful
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            self.logger.warning(f"Security question verification failed. Error: {error.text}")
            return self
        except TimeoutException:
            # If no error, assume success
            self.logger.info("Security question verification successful")
            from page_objects.dashboard_page import DashboardPage
            return DashboardPage(self.driver)
    
    # Biometric Methods
    def is_biometric_prompt_displayed(self):
        """Check if biometric authentication prompt is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.BIOMETRIC_PROMPT))
            return True
        except TimeoutException:
            return False
    
    def use_password_instead(self):
        """Click 'Use Password Instead' link on biometric prompt."""
        password_link = self.wait.until(EC.element_to_be_clickable(self.USE_PASSWORD_INSTEAD_LINK))
        password_link.click()
        self.logger.info("Clicked 'Use Password Instead' link")
        return self
