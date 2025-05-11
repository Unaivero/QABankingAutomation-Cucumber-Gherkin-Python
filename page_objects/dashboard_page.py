from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from decimal import Decimal
from page_objects.transaction_page import TransactionPage
from page_objects.transfer_page import TransferPage
from page_objects.bill_payment_page import BillPaymentPage
from page_objects.external_transfer_page import ExternalTransferPage

class DashboardPage:
    # Locators
    DASHBOARD_HEADER = (By.ID, "dashboard-header")
    ACCOUNT_SUMMARY_SECTION = (By.ID, "account-summary")
    CHECKING_BALANCE = (By.ID, "checking-balance")
    SAVINGS_BALANCE = (By.ID, "savings-balance")
    TRANSACTION_HISTORY_LINK = (By.ID, "transaction-history-link")
    TRANSFER_FUNDS_LINK = (By.ID, "transfer-funds-link")
    BILL_PAY_LINK = (By.ID, "bill-pay-link")
    EXTERNAL_TRANSFER_LINK = (By.ID, "external-transfer-link")
    PAYEE_LIST = (By.ID, "registered-payees")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_dashboard_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except TimeoutException:
            return False
    
    def is_account_summary_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_SUMMARY_SECTION))
            return True
        except TimeoutException:
            return False
    
    def get_checking_balance(self):
        balance_element = self.wait.until(EC.visibility_of_element_located(self.CHECKING_BALANCE))
        # Remove currency symbol and commas, then convert to Decimal
        balance_text = balance_element.text.replace('$', '').replace(',', '')
        return Decimal(balance_text)
    
    def get_savings_balance(self):
        balance_element = self.wait.until(EC.visibility_of_element_located(self.SAVINGS_BALANCE))
        # Remove currency symbol and commas, then convert to Decimal
        balance_text = balance_element.text.replace('$', '').replace(',', '')
        return Decimal(balance_text)
    
    def click_transaction_history(self):
        link = self.wait.until(EC.element_to_be_clickable(self.TRANSACTION_HISTORY_LINK))
        link.click()
        return TransactionPage(self.driver)
    
    def click_transfer_funds(self):
        link = self.wait.until(EC.element_to_be_clickable(self.TRANSFER_FUNDS_LINK))
        link.click()
        return TransferPage(self.driver)
    
    def click_bill_pay(self):
        link = self.wait.until(EC.element_to_be_clickable(self.BILL_PAY_LINK))
        link.click()
        return BillPaymentPage(self.driver)
    
    def click_external_transfer(self):
        link = self.wait.until(EC.element_to_be_clickable(self.EXTERNAL_TRANSFER_LINK))
        link.click()
        return ExternalTransferPage(self.driver)
    
    def is_payee_set_up(self, payee_name):
        try:
            payee_list = self.wait.until(EC.visibility_of_element_located(self.PAYEE_LIST))
            payees = payee_list.find_elements(By.TAG_NAME, "li")
            for payee in payees:
                if payee_name in payee.text:
                    return True
            return False
        except TimeoutException:
            return False
    
    def get_external_transfer_page(self):
        return ExternalTransferPage(self.driver)
