from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from decimal import Decimal

class ExternalTransferPage:
    # Locators
    EXTERNAL_TRANSFER_HEADER = (By.ID, "external-transfer-header")
    RECIPIENT_NAME_INPUT = (By.ID, "recipient-name")
    RECIPIENT_ACCOUNT_INPUT = (By.ID, "recipient-account")
    RECIPIENT_ROUTING_INPUT = (By.ID, "recipient-routing")
    RECIPIENT_BANK_INPUT = (By.ID, "recipient-bank")
    FROM_ACCOUNT_DROPDOWN = (By.ID, "from-account")
    AMOUNT_INPUT = (By.ID, "transfer-amount")
    TRANSFER_DATE = (By.ID, "transfer-date")
    MEMO_INPUT = (By.ID, "transfer-memo")
    CONFIRM_TRANSFER_BUTTON = (By.ID, "confirm-transfer")
    VERIFICATION_SECTION = (By.ID, "additional-verification")
    REGULATORY_INFO = (By.ID, "regulatory-information")
    VERIFICATION_CODE_INPUT = (By.ID, "verification-code")
    SUBMIT_VERIFICATION_BUTTON = (By.ID, "submit-verification")
    TRANSACTION_STATUS = (By.ID, "transaction-status")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_external_transfer_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EXTERNAL_TRANSFER_HEADER))
            return True
        except TimeoutException:
            return False
    
    def enter_recipient_details(self, recipient_name, account_number=None, routing_number=None, bank_name=None):
        """
        Enter recipient details for the external transfer
        
        :param recipient_name: Name of the recipient
        :param account_number: Recipient's account number
        :param routing_number: Recipient's routing number
        :param bank_name: Recipient's bank name
        """
        # For the demo, if only recipient_name is provided, assume it's a saved recipient
        if recipient_name and not any([account_number, routing_number, bank_name]):
            # Select from saved recipients dropdown
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "saved-recipients")))
            select = Select(dropdown)
            select.select_by_visible_text(recipient_name)
        else:
            # Enter new recipient details
            name_input = self.wait.until(EC.element_to_be_clickable(self.RECIPIENT_NAME_INPUT))
            name_input.clear()
            name_input.send_keys(recipient_name)
            
            if account_number:
                account_input = self.wait.until(EC.element_to_be_clickable(self.RECIPIENT_ACCOUNT_INPUT))
                account_input.clear()
                account_input.send_keys(account_number)
            
            if routing_number:
                routing_input = self.wait.until(EC.element_to_be_clickable(self.RECIPIENT_ROUTING_INPUT))
                routing_input.clear()
                routing_input.send_keys(routing_number)
            
            if bank_name:
                bank_input = self.wait.until(EC.element_to_be_clickable(self.RECIPIENT_BANK_INPUT))
                bank_input.clear()
                bank_input.send_keys(bank_name)
    
    def select_from_account(self, account_name):
        """
        Select the source account for the transfer
        
        :param account_name: Name of the account ("Checking", "Savings", etc.)
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.FROM_ACCOUNT_DROPDOWN))
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
    
    def is_additional_verification_displayed(self):
        """
        Check if additional verification is required for the transfer
        
        :return: True if verification is required, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.VERIFICATION_SECTION))
            return True
        except TimeoutException:
            return False
    
    def get_regulatory_information(self):
        """
        Get the regulatory information displayed for large transfers
        
        :return: Regulatory information text
        """
        info_element = self.wait.until(EC.visibility_of_element_located(self.REGULATORY_INFO))
        return info_element.text
    
    def complete_additional_verification(self, verification_code=None):
        """
        Complete the additional verification process
        
        :param verification_code: Verification code (if None, a test code will be used)
        """
        if not verification_code:
            verification_code = "123456"  # Test code for automation
        
        code_input = self.wait.until(EC.element_to_be_clickable(self.VERIFICATION_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(verification_code)
        
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_VERIFICATION_BUTTON))
        submit_button.click()
    
    def get_transaction_status(self):
        """
        Get the current status of the transaction
        
        :return: Status text
        """
        status_element = self.wait.until(EC.visibility_of_element_located(self.TRANSACTION_STATUS))
        return status_element.text
