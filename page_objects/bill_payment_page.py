from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from decimal import Decimal

class BillPaymentPage:
    # Locators
    BILL_PAY_HEADER = (By.ID, "bill-payment-header")
    PAYEE_DROPDOWN = (By.ID, "payee-selection")
    ACCOUNT_DROPDOWN = (By.ID, "payment-account")
    AMOUNT_INPUT = (By.ID, "payment-amount")
    PAYMENT_DATE = (By.ID, "payment-date")
    PAYMENT_MEMO = (By.ID, "payment-memo")
    CONFIRM_PAYMENT_BUTTON = (By.ID, "confirm-payment")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    CONFIRMATION_NUMBER = (By.ID, "confirmation-number")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    ADD_PAYEE_BUTTON = (By.ID, "add-new-payee")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_bill_payment_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.BILL_PAY_HEADER))
            return True
        except TimeoutException:
            return False
    
    def select_payee(self, payee_name):
        """
        Select a payee from the dropdown
        
        :param payee_name: Name of the payee
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.PAYEE_DROPDOWN))
        select = Select(dropdown)
        select.select_by_visible_text(payee_name)
    
    def select_account(self, account_name):
        """
        Select the account to pay from
        
        :param account_name: Name of the account ("Checking", "Savings", etc.)
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_DROPDOWN))
        select = Select(dropdown)
        select.select_by_visible_text(account_name)
    
    def enter_amount(self, amount):
        """
        Enter the payment amount
        
        :param amount: Decimal amount to pay
        """
        amount_input = self.wait.until(EC.element_to_be_clickable(self.AMOUNT_INPUT))
        amount_input.clear()
        amount_input.send_keys(str(amount))
    
    def set_payment_date(self, date_str):
        """
        Set the payment date
        
        :param date_str: Date in format "YYYY-MM-DD"
        """
        date_input = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_DATE))
        date_input.clear()
        date_input.send_keys(date_str)
    
    def enter_memo(self, memo):
        """
        Enter an optional memo for the payment
        
        :param memo: Memo text
        """
        memo_input = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_MEMO))
        memo_input.clear()
        memo_input.send_keys(memo)
    
    def click_confirm_payment(self):
        """
        Click the button to confirm and execute the payment
        """
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_PAYMENT_BUTTON))
        confirm_button.click()
    
    def is_confirmation_displayed(self):
        """
        Check if a confirmation message is displayed after payment
        
        :return: True if confirmation is displayed, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except TimeoutException:
            return False
    
    def get_confirmation_reference(self):
        """
        Get the confirmation reference number for a successful payment
        
        :return: Reference number as a string
        """
        ref_element = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_NUMBER))
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
    
    def click_add_new_payee(self):
        """
        Click the button to add a new payee
        """
        add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_PAYEE_BUTTON))
        add_button.click()
