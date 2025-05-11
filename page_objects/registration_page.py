from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class RegistrationPage:
    """Page object for the new user registration page."""
    
    # Personal Information Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    DOB_INPUT = (By.ID, "date-of-birth")
    SSN_INPUT = (By.ID, "ssn")
    
    # Address Locators
    ADDRESS_LINE1_INPUT = (By.ID, "address-line1")
    ADDRESS_LINE2_INPUT = (By.ID, "address-line2")
    CITY_INPUT = (By.ID, "city")
    STATE_DROPDOWN = (By.ID, "state")
    ZIP_CODE_INPUT = (By.ID, "zip-code")
    
    # Account Credentials Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password")
    
    # Security Questions
    SECURITY_QUESTION1_DROPDOWN = (By.ID, "security-question1")
    SECURITY_ANSWER1_INPUT = (By.ID, "security-answer1")
    SECURITY_QUESTION2_DROPDOWN = (By.ID, "security-question2")
    SECURITY_ANSWER2_INPUT = (By.ID, "security-answer2")
    SECURITY_QUESTION3_DROPDOWN = (By.ID, "security-question3")
    SECURITY_ANSWER3_INPUT = (By.ID, "security-answer3")
    
    # Terms and Agreements
    TERMS_CHECKBOX = (By.ID, "accept-terms")
    PRIVACY_POLICY_CHECKBOX = (By.ID, "accept-privacy")
    EMAIL_CONSENT_CHECKBOX = (By.ID, "email-consent")
    
    # Navigation Buttons
    NEXT_BUTTON = (By.ID, "next-btn")
    PREVIOUS_BUTTON = (By.ID, "previous-btn")
    SUBMIT_BUTTON = (By.ID, "submit-registration-btn")
    
    # Section Headers (to verify current page)
    PERSONAL_INFO_HEADER = (By.XPATH, "//h2[contains(text(), 'Personal Information')]")
    ADDRESS_HEADER = (By.XPATH, "//h2[contains(text(), 'Address')]")
    ACCOUNT_CREDENTIALS_HEADER = (By.XPATH, "//h2[contains(text(), 'Account Credentials')]")
    SECURITY_QUESTIONS_HEADER = (By.XPATH, "//h2[contains(text(), 'Security Questions')]")
    TERMS_HEADER = (By.XPATH, "//h2[contains(text(), 'Terms and Agreements')]")
    
    # Success and Error Messages
    SUCCESS_MESSAGE = (By.CLASS_NAME, "registration-success")
    ERROR_MESSAGE = (By.CLASS_NAME, "registration-error")
    FIELD_ERROR_MESSAGE = (By.CLASS_NAME, "field-error")
    
    # Progress Indicator
    PROGRESS_INDICATOR = (By.ID, "registration-progress")
    
    def __init__(self, driver):
        """Initialize the registration page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('registration_page')
        self.current_step = 1
    
    def navigate(self):
        """Navigate to the registration page."""
        base_url = self.driver.base_url if hasattr(self.driver, 'base_url') else "https://mybank.example.com"
        self.driver.get(f"{base_url}/register")
        self.logger.info("Navigated to registration page")
        return self
    
    def is_registration_page_displayed(self):
        """Check if the registration page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.PERSONAL_INFO_HEADER))
            self.logger.info("Registration page is displayed")
            return True
        except TimeoutException:
            self.logger.warning("Registration page is not displayed")
            return False
    
    def get_current_step(self):
        """Get the current registration step number."""
        try:
            progress = self.wait.until(EC.visibility_of_element_located(self.PROGRESS_INDICATOR))
            step_text = progress.text
            # Extract step number from text like "Step 2 of 5"
            step_parts = step_text.split(" ")
            if len(step_parts) >= 2:
                self.current_step = int(step_parts[1])
            self.logger.info(f"Current registration step: {self.current_step}")
        except (TimeoutException, ValueError, IndexError):
            self.logger.warning("Could not determine current registration step")
        
        return self.current_step
    
    # Personal Information Methods
    def enter_personal_information(self, first_name, last_name, email, phone, dob, ssn):
        """Enter all personal information."""
        self.wait.until(EC.visibility_of_element_located(self.PERSONAL_INFO_HEADER))
        
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT)).send_keys(first_name)
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT)).send_keys(last_name)
        self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT)).send_keys(email)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT)).send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.DOB_INPUT)).send_keys(dob)
        self.wait.until(EC.element_to_be_clickable(self.SSN_INPUT)).send_keys(ssn)
        
        self.logger.info(f"Entered personal information for {first_name} {last_name}")
        return self
    
    # Address Methods
    def enter_address(self, address_line1, city, state, zip_code, address_line2=None):
        """Enter address information."""
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS_HEADER))
        
        self.wait.until(EC.element_to_be_clickable(self.ADDRESS_LINE1_INPUT)).send_keys(address_line1)
        if address_line2:
            self.wait.until(EC.element_to_be_clickable(self.ADDRESS_LINE2_INPUT)).send_keys(address_line2)
        
        self.wait.until(EC.element_to_be_clickable(self.CITY_INPUT)).send_keys(city)
        
        # Select state from dropdown
        state_select = Select(self.wait.until(EC.element_to_be_clickable(self.STATE_DROPDOWN)))
        state_select.select_by_visible_text(state)
        
        self.wait.until(EC.element_to_be_clickable(self.ZIP_CODE_INPUT)).send_keys(zip_code)
        
        self.logger.info(f"Entered address in {city}, {state}")
        return self
    
    # Account Credentials Methods
    def enter_account_credentials(self, username, password, confirm_password):
        """Enter account credentials."""
        self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_CREDENTIALS_HEADER))
        
        self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_PASSWORD_INPUT)).send_keys(confirm_password)
        
        self.logger.info(f"Entered account credentials for username: {username}")
        return self
    
    # Security Questions Methods
    def enter_security_questions(self, q1_answer, q2_answer, q3_answer, q1_index=0, q2_index=1, q3_index=2):
        """Enter security questions and answers."""
        self.wait.until(EC.visibility_of_element_located(self.SECURITY_QUESTIONS_HEADER))
        
        # Select questions from dropdowns
        q1_select = Select(self.wait.until(EC.element_to_be_clickable(self.SECURITY_QUESTION1_DROPDOWN)))
        q1_select.select_by_index(q1_index)
        
        q2_select = Select(self.wait.until(EC.element_to_be_clickable(self.SECURITY_QUESTION2_DROPDOWN)))
        q2_select.select_by_index(q2_index)
        
        q3_select = Select(self.wait.until(EC.element_to_be_clickable(self.SECURITY_QUESTION3_DROPDOWN)))
        q3_select.select_by_index(q3_index)
        
        # Enter answers
        self.wait.until(EC.element_to_be_clickable(self.SECURITY_ANSWER1_INPUT)).send_keys(q1_answer)
        self.wait.until(EC.element_to_be_clickable(self.SECURITY_ANSWER2_INPUT)).send_keys(q2_answer)
        self.wait.until(EC.element_to_be_clickable(self.SECURITY_ANSWER3_INPUT)).send_keys(q3_answer)
        
        self.logger.info("Entered security questions and answers")
        return self
    
    # Terms and Agreements Methods
    def accept_terms(self, accept_email_consent=True):
        """Accept terms and agreements."""
        self.wait.until(EC.visibility_of_element_located(self.TERMS_HEADER))
        
        # Check required checkboxes
        if not self.wait.until(EC.element_to_be_clickable(self.TERMS_CHECKBOX)).is_selected():
            self.wait.until(EC.element_to_be_clickable(self.TERMS_CHECKBOX)).click()
        
        if not self.wait.until(EC.element_to_be_clickable(self.PRIVACY_POLICY_CHECKBOX)).is_selected():
            self.wait.until(EC.element_to_be_clickable(self.PRIVACY_POLICY_CHECKBOX)).click()
        
        # Email consent is optional
        if accept_email_consent:
            if not self.wait.until(EC.element_to_be_clickable(self.EMAIL_CONSENT_CHECKBOX)).is_selected():
                self.wait.until(EC.element_to_be_clickable(self.EMAIL_CONSENT_CHECKBOX)).click()
        
        self.logger.info(f"Accepted terms and agreements (email consent: {accept_email_consent})")
        return self
    
    # Navigation Methods
    def click_next(self):
        """Click the Next button to proceed to the next step."""
        next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
        next_button.click()
        self.logger.info(f"Clicked Next button (moving from step {self.current_step})")
        self.current_step += 1
        return self
    
    def click_previous(self):
        """Click the Previous button to return to the previous step."""
        previous_button = self.wait.until(EC.element_to_be_clickable(self.PREVIOUS_BUTTON))
        previous_button.click()
        self.logger.info(f"Clicked Previous button (moving from step {self.current_step})")
        self.current_step -= 1
        return self
    
    def submit_registration(self):
        """Submit the registration form."""
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_button.click()
        self.logger.info("Submitted registration form")
        
        # Check for success or failure
        try:
            success_message = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            self.logger.info(f"Registration successful: {success_message.text}")
            from page_objects.registration_success_page import RegistrationSuccessPage
            return RegistrationSuccessPage(self.driver)
        except TimeoutException:
            try:
                error_message = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                self.logger.warning(f"Registration failed: {error_message.text}")
            except TimeoutException:
                self.logger.warning("Registration status unknown - no success or error message")
            return self
    
    def get_error_message(self):
        """Get the main error message."""
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except TimeoutException:
            return ""
    
    def get_field_errors(self):
        """Get all field-specific error messages."""
        errors = {}
        try:
            error_elements = self.driver.find_elements(*self.FIELD_ERROR_MESSAGE)
            for error in error_elements:
                # Try to associate error with field based on proximity or parent/child relationship
                field_id = error.get_attribute("data-field-id") or "unknown"
                errors[field_id] = error.text
            return errors
        except:
            return {}
    
    # Complete Registration Flow
    def complete_registration(self, user_data):
        """Complete the entire registration process with the provided user data."""
        self.logger.info(f"Starting registration for {user_data.get('first_name')} {user_data.get('last_name')}")
        
        # Step 1: Personal Information
        self.enter_personal_information(
            user_data.get('first_name'),
            user_data.get('last_name'),
            user_data.get('email'),
            user_data.get('phone'),
            user_data.get('dob'),
            user_data.get('ssn')
        )
        self.click_next()
        
        # Step 2: Address
        self.enter_address(
            user_data.get('address_line1'),
            user_data.get('city'),
            user_data.get('state'),
            user_data.get('zip_code'),
            user_data.get('address_line2')
        )
        self.click_next()
        
        # Step 3: Account Credentials
        self.enter_account_credentials(
            user_data.get('username'),
            user_data.get('password'),
            user_data.get('password')  # Same for confirm_password
        )
        self.click_next()
        
        # Step 4: Security Questions
        self.enter_security_questions(
            user_data.get('security_answer1'),
            user_data.get('security_answer2'),
            user_data.get('security_answer3'),
            user_data.get('security_question1_index', 0),
            user_data.get('security_question2_index', 1),
            user_data.get('security_question3_index', 2)
        )
        self.click_next()
        
        # Step 5: Terms and Agreements
        self.accept_terms(user_data.get('accept_email_consent', True))
        
        # Submit the registration
        return self.submit_registration()
