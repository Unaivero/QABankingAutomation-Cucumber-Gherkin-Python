from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from decimal import Decimal
import datetime
import re

class MobileAccountsPage:
    """Page object for the mobile accounts page."""
    
    # Common Locators (for both Android and iOS)
    ACCOUNTS_TITLE = (MobileBy.XPATH, "//android.widget.TextView[@text='Accounts']|//XCUIElementTypeStaticText[@name='Accounts']")
    
    # Android-specific Locators
    CHECKING_ACCOUNT_ANDROID = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Checking')]")
    SAVINGS_ACCOUNT_ANDROID = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Savings')]")
    CREDIT_CARD_ANDROID = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Credit Card')]")
    
    CHECKING_BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/checkingBalance")
    SAVINGS_BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/savingsBalance")
    CREDIT_CARD_BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/creditBalance")
    
    LAST_UPDATED_ANDROID = (MobileBy.ID, "com.mybank.banking:id/lastUpdated")
    REFRESH_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/refreshButton")
    ADD_ACCOUNT_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/addAccountButton")
    
    # iOS-specific Locators
    CHECKING_ACCOUNT_IOS = (MobileBy.ACCESSIBILITY_ID, "checkingAccount")
    SAVINGS_ACCOUNT_IOS = (MobileBy.ACCESSIBILITY_ID, "savingsAccount")
    CREDIT_CARD_IOS = (MobileBy.ACCESSIBILITY_ID, "creditCardAccount")
    
    CHECKING_BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "checkingBalance")
    SAVINGS_BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "savingsBalance")
    CREDIT_CARD_BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "creditBalance")
    
    LAST_UPDATED_IOS = (MobileBy.ACCESSIBILITY_ID, "lastUpdated")
    REFRESH_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "refreshButton")
    ADD_ACCOUNT_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "addAccountButton")
    
    def __init__(self, driver):
        """Initialize the accounts page with Appium driver."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('mobile_accounts_page')
        
        # Determine platform
        self.is_android = 'platformName' in driver.capabilities and driver.capabilities['platformName'].lower() == 'android'
        self.logger.info(f"Initialized mobile accounts page (Platform: {'Android' if self.is_android else 'iOS'})")
    
    def is_accounts_page_displayed(self):
        """Check if the accounts page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ACCOUNTS_TITLE))
            return True
        except TimeoutException:
            return False
    
    def _parse_balance(self, balance_text):
        """Parse balance text to Decimal value."""
        # Extract numeric value from text like "$10,000.00"
        numeric_value = re.search(r'(\$)?([\d,]+\.\d+)', balance_text)
        if numeric_value:
            # Convert to decimal, removing commas and dollar sign
            cleaned_value = numeric_value.group(2).replace(',', '')
            return Decimal(cleaned_value)
        return None
    
    def _parse_date(self, date_text):
        """Parse date text to datetime object."""
        # Extract datetime from text like "Last Updated: 05/10/2025 10:30 AM"
        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s+[AP]M)', date_text)
        if date_match:
            date_str = date_match.group(1)
            try:
                return datetime.datetime.strptime(date_str, "%m/%d/%Y %I:%M %p")
            except ValueError:
                self.logger.warning(f"Could not parse date string: {date_str}")
        return datetime.datetime.now()  # Fallback to current time
    
    def get_checking_account_balance(self):
        """Get the checking account balance."""
        try:
            locator = self.CHECKING_BALANCE_ANDROID if self.is_android else self.CHECKING_BALANCE_IOS
            balance_element = self.wait.until(EC.visibility_of_element_located(locator))
            balance_text = balance_element.text
            
            balance = self._parse_balance(balance_text)
            self.logger.info(f"Checking account balance: ${balance}")
            return balance
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"Could not get checking account balance: {e}")
            return None
    
    def get_savings_account_balance(self):
        """Get the savings account balance."""
        try:
            locator = self.SAVINGS_BALANCE_ANDROID if self.is_android else self.SAVINGS_BALANCE_IOS
            balance_element = self.wait.until(EC.visibility_of_element_located(locator))
            balance_text = balance_element.text
            
            balance = self._parse_balance(balance_text)
            self.logger.info(f"Savings account balance: ${balance}")
            return balance
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"Could not get savings account balance: {e}")
            return None
    
    def get_credit_card_balance(self):
        """Get the credit card balance."""
        try:
            locator = self.CREDIT_CARD_BALANCE_ANDROID if self.is_android else self.CREDIT_CARD_BALANCE_IOS
            balance_element = self.wait.until(EC.visibility_of_element_located(locator))
            balance_text = balance_element.text
            
            balance = self._parse_balance(balance_text)
            self.logger.info(f"Credit card balance: ${balance}")
            return balance
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"Could not get credit card balance: {e}")
            return None
    
    def get_last_updated_timestamp(self):
        """Get the timestamp when account information was last updated."""
        try:
            locator = self.LAST_UPDATED_ANDROID if self.is_android else self.LAST_UPDATED_IOS
            timestamp_element = self.wait.until(EC.visibility_of_element_located(locator))
            timestamp_text = timestamp_element.text
            
            last_updated = self._parse_date(timestamp_text)
            self.logger.info(f"Last updated timestamp: {last_updated}")
            return last_updated
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"Could not get last updated timestamp: {e}")
            return datetime.datetime.now()  # Return current time as fallback
    
    def refresh_accounts(self):
        """Tap the refresh button to update account information."""
        locator = self.REFRESH_BUTTON_ANDROID if self.is_android else self.REFRESH_BUTTON_IOS
        refresh_button = self.wait.until(EC.element_to_be_clickable(locator))
        refresh_button.click()
        self.logger.info("Tapped refresh button")
        
        # Wait for refresh to complete
        try:
            # Look for a loading indicator or wait for it to disappear
            if self.is_android:
                loading = (MobileBy.ID, "com.mybank.banking:id/loadingIndicator")
            else:
                loading = (MobileBy.ACCESSIBILITY_ID, "loadingIndicator")
            
            # First wait for it to appear (in case there's a delay)
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(loading))
            # Then wait for it to disappear
            WebDriverWait(self.driver, 15).until_not(EC.visibility_of_element_located(loading))
            
            self.logger.info("Refresh completed")
        except TimeoutException:
            self.logger.warning("Loading indicator not found or did not disappear")
    
    def select_checking_account(self):
        """Select/tap the checking account to view details."""
        locator = self.CHECKING_ACCOUNT_ANDROID if self.is_android else self.CHECKING_ACCOUNT_IOS
        checking_account = self.wait.until(EC.element_to_be_clickable(locator))
        checking_account.click()
        self.logger.info("Selected checking account")
    
    def select_savings_account(self):
        """Select/tap the savings account to view details."""
        locator = self.SAVINGS_ACCOUNT_ANDROID if self.is_android else self.SAVINGS_ACCOUNT_IOS
        savings_account = self.wait.until(EC.element_to_be_clickable(locator))
        savings_account.click()
        self.logger.info("Selected savings account")
    
    def select_credit_card(self):
        """Select/tap the credit card to view details."""
        locator = self.CREDIT_CARD_ANDROID if self.is_android else self.CREDIT_CARD_IOS
        credit_card = self.wait.until(EC.element_to_be_clickable(locator))
        credit_card.click()
        self.logger.info("Selected credit card")
    
    def tap_add_account(self):
        """Tap the add account button."""
        locator = self.ADD_ACCOUNT_BUTTON_ANDROID if self.is_android else self.ADD_ACCOUNT_BUTTON_IOS
        add_account = self.wait.until(EC.element_to_be_clickable(locator))
        add_account.click()
        self.logger.info("Tapped add account button")
