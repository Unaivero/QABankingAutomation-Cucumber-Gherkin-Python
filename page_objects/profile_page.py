from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import re
import time
import json

class ProfilePage:
    """
    Page object for the user profile management pages.
    """
    
    # Common elements
    PROFILE_HEADER = (By.ID, "profile-management-header")
    PROFILE_MENU = (By.ID, "profile-menu")
    EDIT_BUTTON = (By.ID, "edit-button")
    SAVE_BUTTON = (By.ID, "save-button")
    CANCEL_BUTTON = (By.ID, "cancel-button")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    VERIFICATION_MESSAGE = (By.CLASS_NAME, "verification-message")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    
    # Personal Information elements
    PERSONAL_INFO_SECTION = (By.ID, "personal-information-section")
    FULL_NAME_FIELD = (By.ID, "full-name")
    EMAIL_FIELD = (By.ID, "email-address")
    PHONE_FIELD = (By.ID, "phone-number")
    ADDRESS_FIELD = (By.ID, "mailing-address")
    
    # Password Change elements
    CURRENT_PASSWORD_FIELD = (By.ID, "current-password")
    NEW_PASSWORD_FIELD = (By.ID, "new-password")
    CONFIRM_PASSWORD_FIELD = (By.ID, "confirm-password")
    CHANGE_PASSWORD_BUTTON = (By.ID, "change-password-button")
    PASSWORD_STRENGTH_INDICATOR = (By.ID, "password-strength")
    PASSWORD_REQUIREMENTS = (By.ID, "password-requirements")
    
    # Security Questions elements
    SECURITY_QUESTIONS_SECTION = (By.ID, "security-questions-section")
    EDIT_SECURITY_QUESTIONS_BUTTON = (By.ID, "edit-security-questions-button")
    QUESTION_DROPDOWNS = (By.CSS_SELECTOR, "select[id^='security-question-']")
    ANSWER_INPUTS = (By.CSS_SELECTOR, "input[id^='security-answer-']")
    
    # Two-Factor Authentication elements
    TWO_FACTOR_SECTION = (By.ID, "two-factor-section")
    ENABLE_2FA_BUTTON = (By.ID, "enable-2fa-button")
    DISABLE_2FA_BUTTON = (By.ID, "disable-2fa-button")
    QR_CODE_IMAGE = (By.ID, "qr-code-image")
    SETUP_KEY_TEXT = (By.ID, "setup-key-text")
    VERIFICATION_CODE_INPUT = (By.ID, "verification-code")
    SUBMIT_VERIFICATION_BUTTON = (By.ID, "submit-verification-button")
    RECOVERY_CODES_CONTAINER = (By.ID, "recovery-codes-container")
    RECOVERY_CODES = (By.CSS_SELECTOR, "#recovery-codes-container .recovery-code")
    
    # Notification Preferences elements
    NOTIFICATION_PREFS_SECTION = (By.ID, "notification-preferences-section")
    NOTIFICATION_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox'][id^='notification-']")
    SAVE_NOTIFICATION_PREFS_BUTTON = (By.ID, "save-notification-prefs-button")
    
    # Statement Preferences elements
    STATEMENT_PREFS_SECTION = (By.ID, "statement-preferences-section")
    PAPER_STATEMENTS_RADIO = (By.ID, "paper-statements")
    PAPERLESS_STATEMENTS_RADIO = (By.ID, "paperless-statements")
    SAVE_STATEMENT_PREFS_BUTTON = (By.ID, "save-statement-prefs-button")
    CONFIRM_STATEMENT_CHANGE_BUTTON = (By.ID, "confirm-statement-change-button")
    
    # Trusted Devices elements
    TRUSTED_DEVICES_SECTION = (By.ID, "trusted-devices-section")
    TRUSTED_DEVICES_LIST = (By.ID, "trusted-devices-list")
    DEVICE_ITEMS = (By.CSS_SELECTOR, "#trusted-devices-list .device-item")
    
    def __init__(self, driver):
        """Initialize the profile page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('profile_page')
    
    def is_profile_page_displayed(self):
        """Check if the profile management page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.PROFILE_HEADER))
            self.wait.until(EC.visibility_of_element_located(self.PROFILE_MENU))
            return True
        except TimeoutException:
            return False
    
    def select_menu_option(self, option):
        """Select an option from the profile menu."""
        # First, ensure the menu is visible
        menu = self.wait.until(EC.visibility_of_element_located(self.PROFILE_MENU))
        
        # Find and click the specified option
        option_xpath = f"//ul[@id='profile-menu']//a[contains(text(), '{option}')]"
        option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_element.click()
        self.logger.info(f"Selected '{option}' from profile menu")
    
    def get_personal_information(self):
        """Get the personal information displayed on the page."""
        # Wait for the personal information section to be visible
        self.wait.until(EC.visibility_of_element_located(self.PERSONAL_INFO_SECTION))
        
        # Extract information from fields
        personal_info = {}
        
        try:
            full_name = self.driver.find_element(*self.FULL_NAME_FIELD).text
            personal_info["Full Name"] = full_name
        except NoSuchElementException:
            pass
        
        try:
            email = self.driver.find_element(*self.EMAIL_FIELD).text
            personal_info["Email Address"] = email
        except NoSuchElementException:
            pass
        
        try:
            phone = self.driver.find_element(*self.PHONE_FIELD).text
            personal_info["Phone Number"] = phone
        except NoSuchElementException:
            pass
        
        try:
            address = self.driver.find_element(*self.ADDRESS_FIELD).text
            personal_info["Mailing Address"] = address
        except NoSuchElementException:
            pass
        
        return personal_info
    
    def get_contact_information(self):
        """Get the contact information displayed on the page."""
        # This is similar to get_personal_information but focused on contact fields
        contact_info = {}
        
        try:
            email = self.driver.find_element(*self.EMAIL_FIELD).text
            contact_info["Email Address"] = email
        except NoSuchElementException:
            pass
        
        try:
            phone = self.driver.find_element(*self.PHONE_FIELD).text
            contact_info["Phone Number"] = phone
        except NoSuchElementException:
            pass
        
        return contact_info
    
    def click_edit_button(self):
        """Click the Edit button."""
        edit_button = self.wait.until(EC.element_to_be_clickable(self.EDIT_BUTTON))
        edit_button.click()
        self.logger.info("Clicked Edit button")
    
    def update_field(self, field_name, new_value):
        """Update a field with a new value."""
        # Map field names to their IDs or locators
        field_map = {
            "Full Name": self.FULL_NAME_FIELD,
            "Email Address": self.EMAIL_FIELD,
            "Phone Number": self.PHONE_FIELD,
            "Mailing Address": self.ADDRESS_FIELD
        }
        
        if field_name not in field_map:
            raise ValueError(f"Field '{field_name}' is not supported for updating")
        
        # Find and update the field
        field_locator = field_map[field_name]
        field_element = self.wait.until(EC.element_to_be_clickable(field_locator))
        field_element.clear()
        field_element.send_keys(new_value)
        self.logger.info(f"Updated {field_name} to: {new_value}")
    
    def submit_changes(self):
        """Submit the changes by clicking the Save button."""
        save_button = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        save_button.click()
        self.logger.info("Clicked Save button to submit changes")
    
    def get_success_message(self):
        """Get the success message text, if displayed."""
        try:
            message = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return message.text
        except TimeoutException:
            return ""
    
    def get_error_message(self):
        """Get the error message text, if displayed."""
        try:
            message = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return message.text
        except TimeoutException:
            return ""
    
    def get_verification_message(self):
        """Get the verification message text, if displayed."""
        try:
            message = self.wait.until(EC.visibility_of_element_located(self.VERIFICATION_MESSAGE))
            return message.text
        except TimeoutException:
            return ""
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        # Wait for the page to load after refresh
        self.wait.until(EC.visibility_of_element_located(self.PROFILE_HEADER))
        self.logger.info("Page refreshed")
    
    def logout(self):
        """Log out of the application."""
        logout_button = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
        logout_button.click()
        self.logger.info("Clicked Logout button")
        
        # Wait for redirect to login page
        from page_objects.login_page import LoginPage
        login_page = LoginPage(self.driver)
        assert login_page.is_login_page_displayed(), "Not redirected to login page after logout"
        
        return login_page
    
    # Password Change Methods
    def select_change_password(self):
        """Navigate to the Change Password section."""
        self.select_menu_option("Security Settings")
        
        # Find and click the Change Password option
        change_password_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Change Password')]"))
        )
        change_password_link.click()
        self.logger.info("Navigated to Change Password section")
    
    def enter_current_password(self, password):
        """Enter the current password."""
        current_password_field = self.wait.until(EC.element_to_be_clickable(self.CURRENT_PASSWORD_FIELD))
        current_password_field.clear()
        current_password_field.send_keys(password)
        self.logger.info("Entered current password")
    
    def enter_new_password(self, password):
        """Enter the new password."""
        new_password_field = self.wait.until(EC.element_to_be_clickable(self.NEW_PASSWORD_FIELD))
        new_password_field.clear()
        new_password_field.send_keys(password)
        self.logger.info("Entered new password")
    
    def enter_confirm_password(self, password):
        """Enter the password confirmation."""
        confirm_field = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_PASSWORD_FIELD))
        confirm_field.clear()
        confirm_field.send_keys(password)
        self.logger.info("Entered password confirmation")
    
    def submit_password_change(self):
        """Submit the password change."""
        submit_button = self.wait.until(EC.element_to_be_clickable(self.CHANGE_PASSWORD_BUTTON))
        submit_button.click()
        self.logger.info("Submitted password change")
    
    def get_password_strength(self):
        """Get the password strength indicator value."""
        strength_element = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_STRENGTH_INDICATOR))
        return strength_element.text
    
    def get_password_requirements_status(self):
        """Get the status of each password requirement."""
        requirements_section = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_REQUIREMENTS))
        
        # Find all requirement items
        requirements = {}
        requirement_elements = requirements_section.find_elements(By.CSS_SELECTOR, ".password-requirement")
        
        for element in requirement_elements:
            # Get the requirement name and status
            name = element.find_element(By.CSS_SELECTOR, ".requirement-text").text
            status_class = element.get_attribute("class")
            
            # Determine status based on class
            if "requirement-met" in status_class:
                status = "Passed"
            else:
                status = "Failed"
            
            requirements[name] = status
        
        return requirements
    
    # Two-Factor Authentication Methods
    def select_two_factor_authentication(self):
        """Navigate to the Two-Factor Authentication section."""
        self.select_menu_option("Security Settings")
        
        # Find and click the 2FA option
        tfa_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Two-Factor Authentication')]"))
        )
        tfa_link.click()
        self.logger.info("Navigated to Two-Factor Authentication section")
        
        # Wait for the 2FA section to load
        self.wait.until(EC.visibility_of_element_located(self.TWO_FACTOR_SECTION))
    
    def click_enable_2fa(self):
        """Click the button to enable 2FA."""
        enable_button = self.wait.until(EC.element_to_be_clickable(self.ENABLE_2FA_BUTTON))
        enable_button.click()
        self.logger.info("Clicked Enable Two-Factor Authentication button")
    
    def get_2fa_setup_instructions(self):
        """Get the 2FA setup instructions text."""
        try:
            instructions = self.driver.find_element(By.ID, "setup-instructions")
            return instructions.text
        except NoSuchElementException:
            return ""
    
    def is_qr_code_displayed(self):
        """Check if the QR code is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.QR_CODE_IMAGE))
            return True
        except TimeoutException:
            return False
    
    def get_2fa_setup_key(self):
        """Get the 2FA setup key text."""
        try:
            key_element = self.wait.until(EC.visibility_of_element_located(self.SETUP_KEY_TEXT))
            # Extract the key from text like "Setup key: ABCDEFGHIJKLMNOP"
            key_text = key_element.text
            match = re.search(r'([A-Z0-9]{16,})', key_text)
            if match:
                return match.group(1)
            return key_text
        except (TimeoutException, NoSuchElementException):
            return ""
    
    def enter_verification_code(self, code):
        """Enter the verification code."""
        code_input = self.wait.until(EC.element_to_be_clickable(self.VERIFICATION_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)
        self.logger.info(f"Entered verification code: {code}")
    
    def submit_verification_code(self):
        """Submit the verification code."""
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_VERIFICATION_BUTTON))
        submit_button.click()
        self.logger.info("Submitted verification code")
    
    def is_2fa_enabled(self):
        """Check if 2FA is enabled."""
        try:
            # Look for the disable button, which indicates 2FA is enabled
            self.wait.until(EC.visibility_of_element_located(self.DISABLE_2FA_BUTTON))
            return True
        except TimeoutException:
            return False
    
    def get_recovery_codes(self):
        """Get the list of recovery codes."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.RECOVERY_CODES_CONTAINER))
            code_elements = self.driver.find_elements(*self.RECOVERY_CODES)
            return [code.text for code in code_elements]
        except TimeoutException:
            return []
    
    # Security Questions Methods
    def select_security_questions(self):
        """Navigate to the Security Questions section."""
        self.select_menu_option("Security Settings")
        
        # Find and click the Security Questions option
        questions_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Security Questions')]"))
        )
        questions_link.click()
        self.logger.info("Navigated to Security Questions section")
        
        # Wait for the section to load
        self.wait.until(EC.visibility_of_element_located(self.SECURITY_QUESTIONS_SECTION))
    
    def get_security_questions(self):
        """Get the list of current security questions."""
        questions_list = {}
        
        # Find all question elements
        try:
            question_elements = self.driver.find_elements(By.CSS_SELECTOR, ".security-question-item")
            
            for element in question_elements:
                question_text = element.find_element(By.CSS_SELECTOR, ".question-text").text
                questions_list[question_text] = "********"  # Answers are masked
            
            return questions_list
        except NoSuchElementException:
            return {}
    
    def click_edit_security_questions(self):
        """Click the button to edit security questions."""
        edit_button = self.wait.until(EC.element_to_be_clickable(self.EDIT_SECURITY_QUESTIONS_BUTTON))
        edit_button.click()
        self.logger.info("Clicked Edit Security Questions button")
    
    def update_security_question(self, index, question_text, answer):
        """Update a security question and answer."""
        # Get the dropdown and answer input for this index
        question_dropdowns = self.driver.find_elements(*self.QUESTION_DROPDOWNS)
        answer_inputs = self.driver.find_elements(*self.ANSWER_INPUTS)
        
        if index >= len(question_dropdowns) or index >= len(answer_inputs):
            raise IndexError(f"Security question index {index} is out of range")
        
        # Select the question from the dropdown
        question_dropdown = question_dropdowns[index]
        select = Select(question_dropdown)
        
        # First try to select by visible text
        try:
            select.select_by_visible_text(question_text)
        except NoSuchElementException:
            # If not found, try to select by partial text match
            options = select.options
            for option in options:
                if question_text in option.text:
                    select.select_by_visible_text(option.text)
                    break
        
        # Enter the answer
        answer_input = answer_inputs[index]
        answer_input.clear()
        answer_input.send_keys(answer)
        
        self.logger.info(f"Updated security question {index} to '{question_text}' with answer '{answer}'")
    
    # Notification Preferences Methods
    def select_notification_preferences(self):
        """Navigate to the Notification Preferences section."""
        self.select_menu_option("Notification Preferences")
        
        # Wait for the section to load
        self.wait.until(EC.visibility_of_element_located(self.NOTIFICATION_PREFS_SECTION))
        self.logger.info("Navigated to Notification Preferences section")
    
    def get_notification_settings(self):
        """Get the current notification settings."""
        settings = {}
        
        # Find all notification preference checkboxes
        checkboxes = self.driver.find_elements(*self.NOTIFICATION_CHECKBOXES)
        
        for checkbox in checkboxes:
            # Parse the ID to get channel and type
            # Example ID: notification-email-transactions
            checkbox_id = checkbox.get_attribute("id")
            id_parts = checkbox_id.split("-")
            
            if len(id_parts) >= 3:
                channel = id_parts[1].capitalize()  # email -> Email
                alert_type = " ".join([part.capitalize() for part in id_parts[2:]])  # transactions -> Transactions
                
                # Check if this channel exists in the settings dict
                if channel not in settings:
                    settings[channel] = {}
                
                # Store the checkbox state
                is_checked = checkbox.is_selected()
                settings[channel][alert_type] = is_checked
        
        return settings
    
    def set_notification_preference(self, channel, alert_type, enabled):
        """Set a notification preference."""
        # Convert channel and alert type to the format used in the ID
        channel_id = channel.lower()
        alert_id = alert_type.lower().replace(" ", "-")
        
        # Construct the checkbox ID
        checkbox_id = f"notification-{channel_id}-{alert_id}"
        
        try:
            checkbox = self.driver.find_element(By.ID, checkbox_id)
            
            # Check or uncheck based on the enabled parameter
            is_checked = checkbox.is_selected()
            
            if (enabled and not is_checked) or (not enabled and is_checked):
                checkbox.click()
                self.logger.info(f"Changed {channel} {alert_type} notification preference to {enabled}")
        
        except NoSuchElementException:
            self.logger.error(f"Could not find checkbox for {channel} {alert_type}")
    
    def save_notification_preferences(self):
        """Save the notification preferences."""
        save_button = self.wait.until(EC.element_to_be_clickable(self.SAVE_NOTIFICATION_PREFS_BUTTON))
        save_button.click()
        self.logger.info("Saved notification preferences")
    
    # Statement Preferences Methods
    def select_statement_preferences(self):
        """Navigate to the Statement Preferences section."""
        self.select_menu_option("Statement Preferences")
        
        # Wait for the section to load
        self.wait.until(EC.visibility_of_element_located(self.STATEMENT_PREFS_SECTION))
        self.logger.info("Navigated to Statement Preferences section")
    
    def get_statement_delivery_method(self):
        """Get the current statement delivery method."""
        try:
            paper_radio = self.driver.find_element(*self.PAPER_STATEMENTS_RADIO)
            paperless_radio = self.driver.find_element(*self.PAPERLESS_STATEMENTS_RADIO)
            
            if paper_radio.is_selected():
                return "Paper"
            elif paperless_radio.is_selected():
                return "Paperless"
            else:
                return "Unknown"
        
        except NoSuchElementException:
            return "Unknown"
    
    def select_paperless_statements(self):
        """Select the Paperless Statements option."""
        paperless_radio = self.wait.until(EC.element_to_be_clickable(self.PAPERLESS_STATEMENTS_RADIO))
        
        if not paperless_radio.is_selected():
            paperless_radio.click()
            self.logger.info("Selected Paperless Statements")
    
    def confirm_statement_preference_change(self):
        """Confirm the statement preference change."""
        # First click Save
        save_button = self.wait.until(EC.element_to_be_clickable(self.SAVE_STATEMENT_PREFS_BUTTON))
        save_button.click()
        
        # Then confirm in the dialog
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_STATEMENT_CHANGE_BUTTON))
        confirm_button.click()
        self.logger.info("Confirmed statement preference change")
    
    # Trusted Devices Methods
    def select_trusted_devices(self):
        """Navigate to the Trusted Devices section."""
        self.select_menu_option("Security Settings")
        
        # Find and click the Trusted Devices option
        devices_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Trusted Devices')]"))
        )
        devices_link.click()
        self.logger.info("Navigated to Trusted Devices section")
        
        # Wait for the section to load
        self.wait.until(EC.visibility_of_element_located(self.TRUSTED_DEVICES_SECTION))
    
    def get_trusted_devices(self):
        """Get the list of trusted devices."""
        devices = []
        
        # Wait for the devices list to load
        self.wait.until(EC.visibility_of_element_located(self.TRUSTED_DEVICES_LIST))
        
        # Find all device items
        device_elements = self.driver.find_elements(*self.DEVICE_ITEMS)
        
        for element in device_elements:
            device = {}
            
            # Extract device details
            try:
                device['id'] = element.get_attribute("data-device-id")
                device['name'] = element.find_element(By.CSS_SELECTOR, ".device-name").text
                device['type'] = element.find_element(By.CSS_SELECTOR, ".device-type").text
                device['last_access'] = element.find_element(By.CSS_SELECTOR, ".last-access").text
                device['location'] = element.find_element(By.CSS_SELECTOR, ".access-location").text
                
                devices.append(device)
            except NoSuchElementException:
                # Skip devices with incomplete information
                continue
        
        return devices
    
    def remove_trusted_device(self, device_id):
        """Remove a trusted device by its ID."""
        # Find the device element
        device_selector = f".device-item[data-device-id='{device_id}']"
        
        try:
            device_element = self.driver.find_element(By.CSS_SELECTOR, device_selector)
            
            # Find and click the remove button
            remove_button = device_element.find_element(By.CSS_SELECTOR, ".remove-device-button")
            remove_button.click()
            
            # Confirm removal in dialog
            confirm_button = self.wait.until(EC.element_to_be_clickable((By.ID, "confirm-remove-device")))
            confirm_button.click()
            
            self.logger.info(f"Removed trusted device with ID: {device_id}")
            
            # Wait for the removal to complete
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, device_selector))
            )
            
            return True
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Failed to remove device {device_id}: {e}")
            return False
