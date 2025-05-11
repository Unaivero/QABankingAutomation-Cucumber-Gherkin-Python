from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import re
from decimal import Decimal

class Transaction:
    """Class representing a transaction in the account details."""
    
    def __init__(self, element, is_android=True):
        """Initialize a transaction with its element."""
        self.element = element
        self.is_android = is_android
        
        # Extract transaction details based on platform
        if is_android:
            self._date_locator = (MobileBy.ID, "com.mybank.banking:id/transactionDate")
            self._merchant_locator = (MobileBy.ID, "com.mybank.banking:id/transactionMerchant")
            self._amount_locator = (MobileBy.ID, "com.mybank.banking:id/transactionAmount")
            self._description_locator = (MobileBy.ID, "com.mybank.banking:id/transactionDescription")
            self._category_locator = (MobileBy.ID, "com.mybank.banking:id/transactionCategory")
        else:
            self._date_locator = (MobileBy.ACCESSIBILITY_ID, "transactionDate")
            self._merchant_locator = (MobileBy.ACCESSIBILITY_ID, "transactionMerchant")
            self._amount_locator = (MobileBy.ACCESSIBILITY_ID, "transactionAmount")
            self._description_locator = (MobileBy.ACCESSIBILITY_ID, "transactionDescription")
            self._category_locator = (MobileBy.ACCESSIBILITY_ID, "transactionCategory")
    
    def has_date(self):
        """Check if the transaction has a date."""
        try:
            return self.element.find_element(*self._date_locator) is not None
        except NoSuchElementException:
            return False
    
    def has_merchant(self):
        """Check if the transaction has a merchant."""
        try:
            return self.element.find_element(*self._merchant_locator) is not None
        except NoSuchElementException:
            return False
    
    def has_amount(self):
        """Check if the transaction has an amount."""
        try:
            return self.element.find_element(*self._amount_locator) is not None
        except NoSuchElementException:
            return False
    
    def get_date(self):
        """Get the transaction date."""
        try:
            date_element = self.element.find_element(*self._date_locator)
            return date_element.text
        except NoSuchElementException:
            return ""
    
    def get_merchant(self):
        """Get the transaction merchant."""
        try:
            merchant_element = self.element.find_element(*self._merchant_locator)
            return merchant_element.text
        except NoSuchElementException:
            return ""
    
    def get_amount(self):
        """Get the transaction amount as a Decimal."""
        try:
            amount_element = self.element.find_element(*self._amount_locator)
            amount_text = amount_element.text
            
            # Parse amount, removing currency symbol and commas
            # Example: "$123.45" -> 123.45, "-$50.00" -> -50.00
            numeric_value = re.search(r'[-+]?\$?([\d,]+\.\d+)', amount_text)
            if numeric_value:
                cleaned_value = numeric_value.group(1).replace(',', '')
                # Check if it's a negative amount
                if '-' in amount_text:
                    return Decimal('-' + cleaned_value)
                return Decimal(cleaned_value)
            return Decimal('0')
        except NoSuchElementException:
            return Decimal('0')
    
    def get_description(self):
        """Get the transaction description."""
        try:
            desc_element = self.element.find_element(*self._description_locator)
            return desc_element.text
        except NoSuchElementException:
            return ""
    
    def get_category(self):
        """Get the transaction category."""
        try:
            category_element = self.element.find_element(*self._category_locator)
            return category_element.text
        except NoSuchElementException:
            return ""
    
    def __str__(self):
        """String representation of the transaction."""
        return f"{self.get_date()} | {self.get_merchant()} | ${self.get_amount()}"


class MobileAccountDetailsPage:
    """Page object for the mobile account details page."""
    
    # Common Locators (for both Android and iOS)
    ACCOUNT_DETAILS_TITLE = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Account Details')]|//XCUIElementTypeStaticText[contains(@name, 'Account Details')]")
    
    # Android-specific Locators
    ACCOUNT_NAME_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountName")
    ACCOUNT_NUMBER_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountNumber")
    BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountBalance")
    AVAILABLE_BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/availableBalance")
    
    TRANSACTIONS_LIST_ANDROID = (MobileBy.ID, "com.mybank.banking:id/transactionsList")
    TRANSACTION_ITEMS_ANDROID = (MobileBy.ID, "com.mybank.banking:id/transactionItem")
    PENDING_TRANSACTIONS_SECTION_ANDROID = (MobileBy.ID, "com.mybank.banking:id/pendingTransactionsSection")
    PENDING_TRANSACTION_ITEMS_ANDROID = (MobileBy.ID, "com.mybank.banking:id/pendingTransactionItem")
    
    SEARCH_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/searchButton")
    SEARCH_INPUT_ANDROID = (MobileBy.ID, "com.mybank.banking:id/searchInput")
    SEARCH_CLEAR_ANDROID = (MobileBy.ID, "com.mybank.banking:id/clearSearch")
    
    FILTER_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/filterButton")
    SORT_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/sortButton")
    
    DATE_RANGE_FILTER_ANDROID = (MobileBy.ID, "com.mybank.banking:id/dateRangeFilter")
    CATEGORY_FILTER_ANDROID = (MobileBy.ID, "com.mybank.banking:id/categoryFilter")
    AMOUNT_FILTER_ANDROID = (MobileBy.ID, "com.mybank.banking:id/amountFilter")
    
    BACK_BUTTON_ANDROID = (MobileBy.ACCESSIBILITY_ID, "Navigate up")
    
    # iOS-specific Locators
    ACCOUNT_NAME_IOS = (MobileBy.ACCESSIBILITY_ID, "accountName")
    ACCOUNT_NUMBER_IOS = (MobileBy.ACCESSIBILITY_ID, "accountNumber")
    BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "accountBalance")
    AVAILABLE_BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "availableBalance")
    
    TRANSACTIONS_LIST_IOS = (MobileBy.ACCESSIBILITY_ID, "transactionsList")
    TRANSACTION_ITEMS_IOS = (MobileBy.ACCESSIBILITY_ID, "transactionItem")
    PENDING_TRANSACTIONS_SECTION_IOS = (MobileBy.ACCESSIBILITY_ID, "pendingTransactionsSection")
    PENDING_TRANSACTION_ITEMS_IOS = (MobileBy.ACCESSIBILITY_ID, "pendingTransactionItem")
    
    SEARCH_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "searchButton")
    SEARCH_INPUT_IOS = (MobileBy.ACCESSIBILITY_ID, "searchInput")
    SEARCH_CLEAR_IOS = (MobileBy.ACCESSIBILITY_ID, "clearSearch")
    
    FILTER_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "filterButton")
    SORT_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "sortButton")
    
    DATE_RANGE_FILTER_IOS = (MobileBy.ACCESSIBILITY_ID, "dateRangeFilter")
    CATEGORY_FILTER_IOS = (MobileBy.ACCESSIBILITY_ID, "categoryFilter")
    AMOUNT_FILTER_IOS = (MobileBy.ACCESSIBILITY_ID, "amountFilter")
    
    BACK_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "Back")
    
    def __init__(self, driver):
        """Initialize the account details page with Appium driver."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('mobile_account_details_page')
        
        # Determine platform
        self.is_android = 'platformName' in driver.capabilities and driver.capabilities['platformName'].lower() == 'android'
        self.logger.info(f"Initialized mobile account details page (Platform: {'Android' if self.is_android else 'iOS'})")
    
    def is_account_details_displayed(self):
        """Check if the account details page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_DETAILS_TITLE))
            return True
        except TimeoutException:
            return False
    
    def get_account_name(self):
        """Get the account name."""
        locator = self.ACCOUNT_NAME_ANDROID if self.is_android else self.ACCOUNT_NAME_IOS
        try:
            name_element = self.wait.until(EC.visibility_of_element_located(locator))
            return name_element.text
        except TimeoutException:
            return ""
    
    def get_account_number(self):
        """Get the account number (might be masked)."""
        locator = self.ACCOUNT_NUMBER_ANDROID if self.is_android else self.ACCOUNT_NUMBER_IOS
        try:
            number_element = self.wait.until(EC.visibility_of_element_located(locator))
            return number_element.text
        except TimeoutException:
            return ""
    
    def get_balance(self):
        """Get the account balance as a Decimal."""
        locator = self.BALANCE_ANDROID if self.is_android else self.BALANCE_IOS
        try:
            balance_element = self.wait.until(EC.visibility_of_element_located(locator))
            balance_text = balance_element.text
            
            # Parse balance, removing currency symbol and commas
            numeric_value = re.search(r'\$?([\d,]+\.\d+)', balance_text)
            if numeric_value:
                cleaned_value = numeric_value.group(1).replace(',', '')
                return Decimal(cleaned_value)
            return Decimal('0')
        except TimeoutException:
            return Decimal('0')
    
    def get_available_balance(self):
        """Get the available balance as a Decimal."""
        locator = self.AVAILABLE_BALANCE_ANDROID if self.is_android else self.AVAILABLE_BALANCE_IOS
        try:
            balance_element = self.wait.until(EC.visibility_of_element_located(locator))
            balance_text = balance_element.text
            
            # Parse balance, removing currency symbol and commas
            numeric_value = re.search(r'\$?([\d,]+\.\d+)', balance_text)
            if numeric_value:
                cleaned_value = numeric_value.group(1).replace(',', '')
                return Decimal(cleaned_value)
            return Decimal('0')
        except TimeoutException:
            return Decimal('0')
    
    def get_transactions(self):
        """Get all transactions displayed on the page."""
        transactions = []
        
        # Wait for transactions list to be visible
        transactions_list_locator = self.TRANSACTIONS_LIST_ANDROID if self.is_android else self.TRANSACTIONS_LIST_IOS
        transaction_item_locator = self.TRANSACTION_ITEMS_ANDROID if self.is_android else self.TRANSACTION_ITEMS_IOS
        
        try:
            self.wait.until(EC.visibility_of_element_located(transactions_list_locator))
            
            # Find all transaction items
            transaction_elements = self.driver.find_elements(*transaction_item_locator)
            
            for element in transaction_elements:
                transaction = Transaction(element, self.is_android)
                transactions.append(transaction)
            
            self.logger.info(f"Found {len(transactions)} transactions")
            return transactions
        
        except TimeoutException:
            self.logger.warning("Transactions list not found or empty")
            return []
    
    def get_pending_transactions(self):
        """Get pending transactions."""
        pending_transactions = []
        
        # Wait for pending transactions section to be visible
        pending_section_locator = self.PENDING_TRANSACTIONS_SECTION_ANDROID if self.is_android else self.PENDING_TRANSACTIONS_SECTION_IOS
        pending_item_locator = self.PENDING_TRANSACTION_ITEMS_ANDROID if self.is_android else self.PENDING_TRANSACTION_ITEMS_IOS
        
        try:
            self.wait.until(EC.visibility_of_element_located(pending_section_locator))
            
            # Find all pending transaction items
            pending_elements = self.driver.find_elements(*pending_item_locator)
            
            for element in pending_elements:
                transaction = Transaction(element, self.is_android)
                pending_transactions.append(transaction)
            
            self.logger.info(f"Found {len(pending_transactions)} pending transactions")
            return pending_transactions
        
        except TimeoutException:
            self.logger.info("No pending transactions found")
            return []
    
    def search_transactions(self, search_text):
        """Search for transactions by text."""
        # Click search button
        search_button_locator = self.SEARCH_BUTTON_ANDROID if self.is_android else self.SEARCH_BUTTON_IOS
        search_input_locator = self.SEARCH_INPUT_ANDROID if self.is_android else self.SEARCH_INPUT_IOS
        
        search_button = self.wait.until(EC.element_to_be_clickable(search_button_locator))
        search_button.click()
        
        # Enter search text
        search_input = self.wait.until(EC.element_to_be_clickable(search_input_locator))
        search_input.clear()
        search_input.send_keys(search_text)
        
        # Submit search (might be handled differently on different platforms)
        if self.is_android:
            # On Android, might need to press Enter/Search key
            from appium.webdriver.common.touch_action import TouchAction
            actions = TouchAction(self.driver)
            actions.tap(x=self.driver.get_window_size()['width'] - 10, y=search_input.location['y'] + 10).perform()
        else:
            # On iOS, tap the search button on keyboard
            search_button = self.driver.find_element(MobileBy.ACCESSIBILITY_ID, "Search")
            search_button.click()
        
        self.logger.info(f"Searched for transactions with text: {search_text}")
        
        # Wait for search results
        import time
        time.sleep(2)  # Give time for search results to update
    
    def clear_search(self):
        """Clear the search and return to full transaction list."""
        clear_button_locator = self.SEARCH_CLEAR_ANDROID if self.is_android else self.SEARCH_CLEAR_IOS
        
        try:
            clear_button = self.wait.until(EC.element_to_be_clickable(clear_button_locator))
            clear_button.click()
            self.logger.info("Cleared search")
        except TimeoutException:
            self.logger.warning("Search clear button not found")
    
    def filter_transactions_by_date(self, start_date=None, end_date=None):
        """Filter transactions by date range."""
        # Click filter button
        filter_button_locator = self.FILTER_BUTTON_ANDROID if self.is_android else self.FILTER_BUTTON_IOS
        filter_button = self.wait.until(EC.element_to_be_clickable(filter_button_locator))
        filter_button.click()
        
        # Select date range filter
        date_filter_locator = self.DATE_RANGE_FILTER_ANDROID if self.is_android else self.DATE_RANGE_FILTER_IOS
        date_filter = self.wait.until(EC.element_to_be_clickable(date_filter_locator))
        date_filter.click()
        
        # This would need to be expanded with the actual date selection UI interaction,
        # which can be very different across apps and platforms
        self.logger.info(f"Setting date filter: {start_date} to {end_date}")
        
        # For now, we'll just log this as a placeholder
        self.logger.warning("Date filter implementation is app-specific and not fully implemented")
    
    def filter_transactions_by_category(self, category):
        """Filter transactions by category."""
        # Click filter button
        filter_button_locator = self.FILTER_BUTTON_ANDROID if self.is_android else self.FILTER_BUTTON_IOS
        filter_button = self.wait.until(EC.element_to_be_clickable(filter_button_locator))
        filter_button.click()
        
        # Select category filter
        category_filter_locator = self.CATEGORY_FILTER_ANDROID if self.is_android else self.CATEGORY_FILTER_IOS
        category_filter = self.wait.until(EC.element_to_be_clickable(category_filter_locator))
        category_filter.click()
        
        # Select the specific category
        # This would need app-specific implementation
        self.logger.info(f"Setting category filter: {category}")
        self.logger.warning("Category filter implementation is app-specific and not fully implemented")
    
    def go_back_to_accounts(self):
        """Navigate back to the accounts list."""
        back_button_locator = self.BACK_BUTTON_ANDROID if self.is_android else self.BACK_BUTTON_IOS
        back_button = self.wait.until(EC.element_to_be_clickable(back_button_locator))
        back_button.click()
        
        # Wait for accounts page to load
        from mobile_page_objects.accounts_page import MobileAccountsPage
        accounts_page = MobileAccountsPage(self.driver)
        
        # Verify we're on the accounts page
        assert accounts_page.is_accounts_page_displayed(), "Failed to navigate back to accounts page"
        
        self.logger.info("Navigated back to accounts page")
        return accounts_page
