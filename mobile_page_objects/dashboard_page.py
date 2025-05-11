from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class MobileDashboardPage:
    """Page object for the mobile dashboard/home page."""
    
    # Common Locators (for both Android and iOS)
    DASHBOARD_TITLE = (MobileBy.XPATH, "//android.widget.TextView[@text='Dashboard']|//XCUIElementTypeStaticText[@name='Dashboard']")
    
    # Android-specific Locators
    ACCOUNTS_SECTION_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountsSection")
    ACCOUNT_ITEMS_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountItem")
    ACCOUNTS_TAB_ANDROID = (MobileBy.ID, "com.mybank.banking:id/accountsTab")
    TRANSFER_TAB_ANDROID = (MobileBy.ID, "com.mybank.banking:id/transferTab")
    BILL_PAY_TAB_ANDROID = (MobileBy.ID, "com.mybank.banking:id/billPayTab")
    DEPOSIT_TAB_ANDROID = (MobileBy.ID, "com.mybank.banking:id/depositTab")
    MORE_TAB_ANDROID = (MobileBy.ID, "com.mybank.banking:id/moreTab")
    NOTIFICATIONS_ICON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/notificationsIcon")
    LOGOUT_BUTTON_ANDROID = (MobileBy.ID, "com.mybank.banking:id/logoutButton")
    USERNAME_DISPLAY_ANDROID = (MobileBy.ID, "com.mybank.banking:id/usernameDisplay")
    TOTAL_BALANCE_ANDROID = (MobileBy.ID, "com.mybank.banking:id/totalBalance")
    
    # iOS-specific Locators
    ACCOUNTS_SECTION_IOS = (MobileBy.ACCESSIBILITY_ID, "accountsSection")
    ACCOUNT_ITEMS_IOS = (MobileBy.ACCESSIBILITY_ID, "accountItem")
    ACCOUNTS_TAB_IOS = (MobileBy.ACCESSIBILITY_ID, "accountsTab")
    TRANSFER_TAB_IOS = (MobileBy.ACCESSIBILITY_ID, "transferTab")
    BILL_PAY_TAB_IOS = (MobileBy.ACCESSIBILITY_ID, "billPayTab")
    DEPOSIT_TAB_IOS = (MobileBy.ACCESSIBILITY_ID, "depositTab")
    MORE_TAB_IOS = (MobileBy.ACCESSIBILITY_ID, "moreTab")
    NOTIFICATIONS_ICON_IOS = (MobileBy.ACCESSIBILITY_ID, "notificationsIcon")
    LOGOUT_BUTTON_IOS = (MobileBy.ACCESSIBILITY_ID, "logoutButton")
    USERNAME_DISPLAY_IOS = (MobileBy.ACCESSIBILITY_ID, "usernameDisplay")
    TOTAL_BALANCE_IOS = (MobileBy.ACCESSIBILITY_ID, "totalBalance")
    
    def __init__(self, driver):
        """Initialize the dashboard page with Appium driver."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger('mobile_dashboard_page')
        
        # Determine platform
        self.is_android = 'platformName' in driver.capabilities and driver.capabilities['platformName'].lower() == 'android'
        self.logger.info(f"Initialized mobile dashboard page (Platform: {'Android' if self.is_android else 'iOS'})")
    
    def is_dashboard_displayed(self):
        """Check if the dashboard page is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_TITLE))
            return True
        except TimeoutException:
            return False
    
    def is_accounts_section_displayed(self):
        """Check if the accounts section is displayed on the dashboard."""
        try:
            locator = self.ACCOUNTS_SECTION_ANDROID if self.is_android else self.ACCOUNTS_SECTION_IOS
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def get_account_count(self):
        """Get the number of accounts displayed on the dashboard."""
        try:
            locator = self.ACCOUNT_ITEMS_ANDROID if self.is_android else self.ACCOUNT_ITEMS_IOS
            accounts = self.driver.find_elements(*locator)
            return len(accounts)
        except NoSuchElementException:
            return 0
    
    def get_total_balance(self):
        """Get the total balance displayed on the dashboard."""
        locator = self.TOTAL_BALANCE_ANDROID if self.is_android else self.TOTAL_BALANCE_IOS
        balance_element = self.wait.until(EC.visibility_of_element_located(locator))
        balance_text = balance_element.text
        
        # Extract numeric value from text like "Total Balance: $10,000.00"
        import re
        numeric_value = re.search(r'[\d,]+\.\d+', balance_text)
        if numeric_value:
            # Convert to decimal, removing commas
            from decimal import Decimal
            cleaned_value = numeric_value.group(0).replace(',', '')
            return Decimal(cleaned_value)
        
        return None
    
    def get_username_displayed(self):
        """Get the username displayed on the dashboard."""
        locator = self.USERNAME_DISPLAY_ANDROID if self.is_android else self.USERNAME_DISPLAY_IOS
        username_element = self.wait.until(EC.visibility_of_element_located(locator))
        return username_element.text
    
    def tap_accounts_tab(self):
        """Tap the Accounts tab in the bottom navigation."""
        locator = self.ACCOUNTS_TAB_ANDROID if self.is_android else self.ACCOUNTS_TAB_IOS
        accounts_tab = self.wait.until(EC.element_to_be_clickable(locator))
        accounts_tab.click()
        self.logger.info("Tapped Accounts tab")
    
    def tap_transfer_tab(self):
        """Tap the Transfer tab in the bottom navigation."""
        locator = self.TRANSFER_TAB_ANDROID if self.is_android else self.TRANSFER_TAB_IOS
        transfer_tab = self.wait.until(EC.element_to_be_clickable(locator))
        transfer_tab.click()
        self.logger.info("Tapped Transfer tab")
    
    def tap_bill_pay_tab(self):
        """Tap the Bill Pay tab in the bottom navigation."""
        locator = self.BILL_PAY_TAB_ANDROID if self.is_android else self.BILL_PAY_TAB_IOS
        bill_pay_tab = self.wait.until(EC.element_to_be_clickable(locator))
        bill_pay_tab.click()
        self.logger.info("Tapped Bill Pay tab")
    
    def tap_deposit_tab(self):
        """Tap the Deposit tab in the bottom navigation."""
        locator = self.DEPOSIT_TAB_ANDROID if self.is_android else self.DEPOSIT_TAB_IOS
        deposit_tab = self.wait.until(EC.element_to_be_clickable(locator))
        deposit_tab.click()
        self.logger.info("Tapped Deposit tab")
    
    def tap_more_tab(self):
        """Tap the More tab in the bottom navigation."""
        locator = self.MORE_TAB_ANDROID if self.is_android else self.MORE_TAB_IOS
        more_tab = self.wait.until(EC.element_to_be_clickable(locator))
        more_tab.click()
        self.logger.info("Tapped More tab")
    
    def tap_notifications_icon(self):
        """Tap the notifications icon."""
        locator = self.NOTIFICATIONS_ICON_ANDROID if self.is_android else self.NOTIFICATIONS_ICON_IOS
        notifications = self.wait.until(EC.element_to_be_clickable(locator))
        notifications.click()
        self.logger.info("Tapped Notifications icon")
    
    def logout(self):
        """Logout from the app."""
        # On some banking apps, logout might be in a menu or settings
        # This is a simple implementation assuming direct access
        locator = self.LOGOUT_BUTTON_ANDROID if self.is_android else self.LOGOUT_BUTTON_IOS
        
        try:
            logout_button = self.wait.until(EC.element_to_be_clickable(locator))
            logout_button.click()
            self.logger.info("Tapped Logout button")
            
            # Handle confirmation dialog if present
            try:
                if self.is_android:
                    confirm = self.driver.find_element(MobileBy.ID, "android:id/button1")
                else:
                    confirm = self.driver.find_element(MobileBy.ACCESSIBILITY_ID, "Confirm")
                
                confirm.click()
                self.logger.info("Confirmed logout")
            except NoSuchElementException:
                self.logger.info("No logout confirmation dialog found")
            
            from mobile_page_objects.login_page import MobileLoginPage
            return MobileLoginPage(self.driver)
        except TimeoutException:
            self.logger.warning("Could not find direct logout button, trying More tab")
            self.tap_more_tab()
            
            # Look for logout in the More menu
            if self.is_android:
                logout_menu = self.driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='Logout']")
            else:
                logout_menu = self.driver.find_element(MobileBy.ACCESSIBILITY_ID, "Logout")
            
            logout_menu.click()
            self.logger.info("Tapped Logout from More menu")
            
            # Handle confirmation
            try:
                if self.is_android:
                    confirm = self.driver.find_element(MobileBy.ID, "android:id/button1")
                else:
                    confirm = self.driver.find_element(MobileBy.ACCESSIBILITY_ID, "Confirm")
                
                confirm.click()
                self.logger.info("Confirmed logout")
            except NoSuchElementException:
                self.logger.info("No logout confirmation dialog found")
            
            from mobile_page_objects.login_page import MobileLoginPage
            return MobileLoginPage(self.driver)
