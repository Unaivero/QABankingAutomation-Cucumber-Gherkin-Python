from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from decimal import Decimal

class TransferPage:
    # Locators
    TRANSFER_HEADER = (By.ID, "transfer-funds-header")
    FROM_ACCOUNT_DROPDOWN = (By.ID, "from-account")
    TO_ACCOUNT_DROPDOWN = (By.ID, "to-account")
    AMOUNT_INPUT = (By.ID, "transfer-amount")
    TRANSFER_DATE = (By.ID, "transfer-date")
    MEMO_INPUT = (By.ID, "transfer-memo")
    CONFIRM_TRANSFER_BUTTON = (By.ID, "confirm-transfer")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    CONFIRMATION_REFERENCE = (By.ID, "confirmation-reference")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_transfer_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.TRANSFER_HEADER))
            return True
        except TimeoutException:
            return False
    
    def select_from_account(self, account_name):
        """
        Select the source account for the transfer
        
        :param account_name: Name of the account ("Checking", "Savings", etc.)
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.FROM_ACCOUNT_DROPDOWN))
        select = Select(dropdown)
        select.select_by_visible_text(account_name)
    
    def select_to_account(self, account_name):
        """
        Select the destination account for the transfer
        
        :param account_name: Name of the account ("Checking", "Savings", etc.)
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.TO_ACCOUNT_DROPDOWN))
        select = Select(dropdown)
        select.select_by_visible_text(account_name)
    
    def enter_amount(self, amount):
        """
        Enter the transfer amount
        
        :param amount: Decimal amount to transfer
        """
        amount_input = self.wait.until(EC.element_to_be_clickable(self.AMOUNT_INPUT))
        amount_input.clear()
        amount_input.send_keys(str(amount))
    
    def set_transfer_date(self, date_str):
        """
        Set the transfer date
        
        :param date_str: Date in format "MM/DD/YYYY"
        """
        date_input = self.wait.until(EC.element_to_be_clickable(self.TRANSFER_DATE))
        date_input.clear()
        date_input.send_keys(date_str)
    
    def enter_memo(self, memo):
        """
        Enter an optional memo for the transfer
        
        :param memo: Memo text
        """
        memo_input = self.wait.until(EC.element_to_be_clickable(self.MEMO_INPUT))
        memo_input.clear()
        memo_input.send_keys(memo)
    
    def click_confirm_transfer(self):
        """
        Click the button to confirm and execute the transfer
        """
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_TRANSFER_BUTTON))
        confirm_button.click()
    
    def is_success_message_displayed(self):
        """
        Check if a success message is displayed after transfer
        
        :return: True if success message is displayed, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except TimeoutException:
            return False
    
    def get_confirmation_reference(self):
        """
        Get the confirmation reference number for a successful transfer
        
        :return: Reference number as a string
        """
        ref_element = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_REFERENCE))
        return ref_element.text
    
    def get_error_message(self):
        """
        Get any error message that appears
        
        :return: Error message as a string, or empty string if no error
        """
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except TimeoutException:
            return ""
