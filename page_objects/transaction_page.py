from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

class Transaction:
    def __init__(self, element):
        self.element = element
        
    def has_date(self):
        return len(self.element.find_elements(By.CLASS_NAME, "transaction-date")) > 0
    
    def has_description(self):
        return len(self.element.find_elements(By.CLASS_NAME, "transaction-description")) > 0
    
    def has_amount(self):
        return len(self.element.find_elements(By.CLASS_NAME, "transaction-amount")) > 0
    
    def get_date(self):
        date_element = self.element.find_element(By.CLASS_NAME, "transaction-date")
        date_str = date_element.text
        return datetime.strptime(date_str, "%m/%d/%Y")
    
    def get_description(self):
        desc_element = self.element.find_element(By.CLASS_NAME, "transaction-description")
        return desc_element.text
    
    def get_amount(self):
        amount_element = self.element.find_element(By.CLASS_NAME, "transaction-amount")
        amount_str = amount_element.text.replace('$', '').replace(',', '')
        return float(amount_str)


class TransactionPage:
    # Locators
    TRANSACTION_HEADER = (By.ID, "transaction-history-header")
    TRANSACTION_LIST = (By.ID, "transaction-list")
    TRANSACTION_ITEMS = (By.CLASS_NAME, "transaction-item")
    FILTER_DROPDOWN = (By.ID, "filter-transactions")
    DATE_RANGE_START = (By.ID, "date-range-start")
    DATE_RANGE_END = (By.ID, "date-range-end")
    APPLY_FILTER_BUTTON = (By.ID, "apply-filter")
    DOWNLOAD_CSV_BUTTON = (By.ID, "download-csv")
    PAGINATION_NEXT = (By.ID, "pagination-next")
    PAGINATION_PREV = (By.ID, "pagination-prev")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_transaction_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.TRANSACTION_HEADER))
            return True
        except TimeoutException:
            return False
    
    def get_transactions(self):
        transaction_elements = self.wait.until(
            EC.presence_of_all_elements_located(self.TRANSACTION_ITEMS)
        )
        return [Transaction(element) for element in transaction_elements]
    
    def filter_by_date_range(self, start_date, end_date):
        """
        Filter transactions by date range
        
        :param start_date: Start date in format "MM/DD/YYYY"
        :param end_date: End date in format "MM/DD/YYYY"
        """
        start_date_input = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_START))
        start_date_input.clear()
        start_date_input.send_keys(start_date)
        
        end_date_input = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_END))
        end_date_input.clear()
        end_date_input.send_keys(end_date)
        
        apply_button = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON))
        apply_button.click()
    
    def filter_by_type(self, transaction_type):
        """
        Filter transactions by type
        
        :param transaction_type: Type of transaction to filter ("deposits", "withdrawals", "transfers", "all")
        """
        filter_dropdown = self.wait.until(EC.element_to_be_clickable(self.FILTER_DROPDOWN))
        filter_dropdown.click()
        
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//option[@value='{transaction_type}']"))
        )
        option.click()
        
        apply_button = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON))
        apply_button.click()
    
    def download_csv(self):
        download_button = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_CSV_BUTTON))
        download_button.click()
    
    def go_to_next_page(self):
        next_button = self.wait.until(EC.element_to_be_clickable(self.PAGINATION_NEXT))
        if "disabled" not in next_button.get_attribute("class"):
            next_button.click()
            return True
        return False
    
    def go_to_previous_page(self):
        prev_button = self.wait.until(EC.element_to_be_clickable(self.PAGINATION_PREV))
        if "disabled" not in prev_button.get_attribute("class"):
            prev_button.click()
            return True
        return False
