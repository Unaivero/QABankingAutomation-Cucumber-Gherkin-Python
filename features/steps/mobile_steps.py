from behave import given, when, then
from hamcrest import assert_that, equal_to, is_not, empty, contains_string, greater_than_or_equal_to
from decimal import Decimal
import datetime
import time
from utils.mobile_driver_manager import get_android_driver, get_ios_driver

@given('I have installed the MyBank mobile app')
def step_impl(context):
    # This is a precondition that is assumed to be true
    # The app installation should be handled outside the test
    # or as part of the setup
    context.driver_type = context.config.userdata.get('mobile_platform', 'android')
    context.logger.info(f"Using mobile platform: {context.driver_type}")

@given('I have valid credentials for mobile banking')
def step_impl(context):
    # Load test user credentials from config or environment
    if context.driver_type.lower() == 'android':
        context.mobile_username = context.config.userdata.get('android_username', 'mobile_user@example.com')
        context.mobile_password = context.config.userdata.get('android_password', 'MobileP@ss123')
    else:
        context.mobile_username = context.config.userdata.get('ios_username', 'ios_user@example.com')
        context.mobile_password = context.config.userdata.get('ios_password', 'iOSP@ss123')
    
    context.logger.info(f"Using mobile credentials for user: {context.mobile_username}")

@when('I open the mobile banking app')
def step_impl(context):
    # Initialize the appropriate mobile driver based on config
    if context.driver_type.lower() == 'android':
        context.mobile_driver = get_android_driver(context)
    else:
        context.mobile_driver = get_ios_driver(context)
    
    # Wait for app to initialize
    time.sleep(3)
    
    # Initialize page objects
    from mobile_page_objects.login_page import MobileLoginPage
    context.mobile_login_page = MobileLoginPage(context.mobile_driver)
    
    assert context.mobile_login_page.is_login_page_displayed(), "Mobile login page not displayed"
    context.logger.info("Mobile banking app opened successfully")

@when('I enter my username "{username}"')
def step_impl(context, username):
    context.mobile_login_page.enter_username(username)

@when('I enter my password "{password}"')
def step_impl(context, password):
    context.mobile_login_page.enter_password(password)

@when('I tap the login button')
def step_impl(context):
    context.mobile_login_page.tap_login_button()

@then('I should be logged into the mobile app successfully')
def step_impl(context):
    from mobile_page_objects.dashboard_page import MobileDashboardPage
    context.mobile_dashboard = MobileDashboardPage(context.mobile_driver)
    
    # Verify login success
    assert context.mobile_dashboard.is_dashboard_displayed(), "Mobile dashboard not displayed after login"
    context.logger.info("Successfully logged into mobile app")

@then('I should see the accounts dashboard')
def step_impl(context):
    assert context.mobile_dashboard.is_accounts_section_displayed(), "Accounts section not displayed on dashboard"
    assert context.mobile_dashboard.get_account_count() > 0, "No accounts displayed on dashboard"
    context.logger.info(f"Found {context.mobile_dashboard.get_account_count()} accounts on dashboard")

@given('I have enabled biometric authentication for my account')
def step_impl(context):
    # This is a precondition that would be set up via API or DB directly
    # For test purposes, we'll just set a flag
    context.biometric_enabled = True
    context.logger.info("Biometric authentication is enabled for test account")

@when('I tap "Login with Biometrics"')
def step_impl(context):
    context.mobile_login_page.tap_biometric_login_button()
    context.logger.info("Tapped biometric login button")

@when('I confirm the biometric prompt')
def step_impl(context):
    # In a real test, this might be handled differently depending on emulator or real device
    # For emulated biometrics, we can mock the response
    context.mobile_login_page.mock_successful_biometric_auth()
    context.logger.info("Mocked successful biometric authentication")

@given('I am logged into the mobile banking app')
def step_impl(context):
    # This step combines multiple steps to get us to a logged-in state
    context.execute_steps('''
        Given I have installed the MyBank mobile app
        And I have valid credentials for mobile banking
        When I open the mobile banking app
        And I enter my username "mobile_user@example.com"
        And I enter my password "MobileP@ss123"
        And I tap the login button
        Then I should be logged into the mobile app successfully
    ''')

@when('I navigate to the accounts screen')
def step_impl(context):
    context.mobile_dashboard.tap_accounts_tab()
    
    from mobile_page_objects.accounts_page import MobileAccountsPage
    context.mobile_accounts_page = MobileAccountsPage(context.mobile_driver)
    
    assert context.mobile_accounts_page.is_accounts_page_displayed(), "Accounts page not displayed"
    context.logger.info("Navigated to accounts screen")

@then('I should see my checking account balance')
def step_impl(context):
    checking_balance = context.mobile_accounts_page.get_checking_account_balance()
    assert checking_balance is not None, "Checking account balance not displayed"
    context.logger.info(f"Checking account balance: ${checking_balance}")

@then('I should see my savings account balance')
def step_impl(context):
    savings_balance = context.mobile_accounts_page.get_savings_account_balance()
    assert savings_balance is not None, "Savings account balance not displayed"
    context.logger.info(f"Savings account balance: ${savings_balance}")

@then('I should see my credit card balance')
def step_impl(context):
    credit_balance = context.mobile_accounts_page.get_credit_card_balance()
    assert credit_balance is not None, "Credit card balance not displayed"
    context.logger.info(f"Credit card balance: ${credit_balance}")

@then('the balances should be accurate and up-to-date')
def step_impl(context):
    # We'd need to compare against expected values from a backend API or database
    # For this example, we'll just verify that the update timestamp is recent
    last_updated = context.mobile_accounts_page.get_last_updated_timestamp()
    current_time = datetime.datetime.now()
    time_difference = current_time - last_updated
    
    # Balances should have been updated within the last hour
    assert time_difference.total_seconds() < 3600, "Account balances may not be up-to-date"
    context.logger.info(f"Balances were last updated at {last_updated}")

@when('I select my checking account')
def step_impl(context):
    context.mobile_accounts_page.select_checking_account()
    
    from mobile_page_objects.account_details_page import MobileAccountDetailsPage
    context.account_details_page = MobileAccountDetailsPage(context.mobile_driver)
    
    assert context.account_details_page.is_account_details_displayed(), "Account details page not displayed"
    context.logger.info("Selected checking account")

@then('I should see a list of recent transactions')
def step_impl(context):
    transactions = context.account_details_page.get_transactions()
    assert_that(transactions, is_not(empty()))
    context.logger.info(f"Found {len(transactions)} recent transactions")

@then('each transaction should display the date, merchant, and amount')
def step_impl(context):
    transactions = context.account_details_page.get_transactions()
    for transaction in transactions[:5]:  # Check first 5 transactions
        assert transaction.has_date(), f"Transaction missing date: {transaction}"
        assert transaction.has_merchant(), f"Transaction missing merchant: {transaction}"
        assert transaction.has_amount(), f"Transaction missing amount: {transaction}"
    
    context.logger.info("Verified transaction details are properly displayed")

@then('I should be able to search transactions by merchant name')
def step_impl(context):
    # Get a merchant name from an existing transaction to search for
    transactions = context.account_details_page.get_transactions()
    if transactions:
        merchant_to_search = transactions[0].get_merchant()
        
        context.account_details_page.search_transactions(merchant_to_search)
        search_results = context.account_details_page.get_transactions()
        
        assert_that(search_results, is_not(empty()))
        for transaction in search_results:
            assert merchant_to_search.lower() in transaction.get_merchant().lower()
        
        context.logger.info(f"Successfully searched for transactions with merchant: {merchant_to_search}")

@given('I have a checking account with balance of ${balance:f}')
def step_impl(context, balance):
    context.checking_balance = Decimal(str(balance))
    
    # Verify account exists with expected balance or set it up via API
    context.logger.info(f"Setting up checking account with balance: ${context.checking_balance}")
    # In a real test, we might verify this via API or DB

@given('I have a savings account with balance of ${balance:f}')
def step_impl(context, balance):
    context.savings_balance = Decimal(str(balance))
    
    # Verify account exists with expected balance or set it up via API
    context.logger.info(f"Setting up savings account with balance: ${context.savings_balance}")
    # In a real test, we might verify this via API or DB

@when('I navigate to the transfer screen')
def step_impl(context):
    context.mobile_dashboard.tap_transfer_tab()
    
    from mobile_page_objects.transfer_page import MobileTransferPage
    context.mobile_transfer_page = MobileTransferPage(context.mobile_driver)
    
    assert context.mobile_transfer_page.is_transfer_page_displayed(), "Transfer page not displayed"
    context.logger.info("Navigated to transfer screen")

@when('I select my checking account as the source account')
def step_impl(context):
    context.mobile_transfer_page.select_from_account("Checking")
    context.logger.info("Selected checking account as source")

@when('I select my savings account as the destination account')
def step_impl(context):
    context.mobile_transfer_page.select_to_account("Savings")
    context.logger.info("Selected savings account as destination")

@when('I enter ${amount:f} as the transfer amount')
def step_impl(context, amount):
    context.transfer_amount = Decimal(str(amount))
    context.mobile_transfer_page.enter_amount(context.transfer_amount)
    context.logger.info(f"Entered transfer amount: ${context.transfer_amount}")

@when('I confirm the transfer')
def step_impl(context):
    context.mobile_transfer_page.tap_confirm_transfer()
    context.logger.info("Confirmed transfer")

@then('I should see a success message')
def step_impl(context):
    success = context.mobile_transfer_page.is_success_message_displayed()
    assert success, "Transfer success message not displayed"
    
    # Optionally capture the reference number
    context.transfer_reference = context.mobile_transfer_page.get_confirmation_reference()
    context.logger.info(f"Transfer successful with reference: {context.transfer_reference}")

@then('my checking account balance should be ${balance:f}')
def step_impl(context, balance):
    expected_balance = Decimal(str(balance))
    
    # Navigate back to accounts page to verify balance
    context.mobile_transfer_page.tap_done_button()
    context.mobile_dashboard.tap_accounts_tab()
    
    from mobile_page_objects.accounts_page import MobileAccountsPage
    accounts_page = MobileAccountsPage(context.mobile_driver)
    
    actual_balance = accounts_page.get_checking_account_balance()
    assert_that(actual_balance, equal_to(expected_balance))
    context.logger.info(f"Verified checking account balance is now ${actual_balance}")

@then('my savings account balance should be ${balance:f}')
def step_impl(context, balance):
    expected_balance = Decimal(str(balance))
    
    # Assuming we're on the accounts page from the previous step
    from mobile_page_objects.accounts_page import MobileAccountsPage
    accounts_page = MobileAccountsPage(context.mobile_driver)
    
    actual_balance = accounts_page.get_savings_account_balance()
    assert_that(actual_balance, equal_to(expected_balance))
    context.logger.info(f"Verified savings account balance is now ${actual_balance}")

@given('I have a registered payee "{payee_name}"')
def step_impl(context, payee_name):
    # This would be set up via API or DB in a real test
    context.logger.info(f"Setting up registered payee: {payee_name}")
    # In a real test, verify the payee exists or set it up

@when('I navigate to the bill payment screen')
def step_impl(context):
    context.mobile_dashboard.tap_bill_pay_tab()
    
    from mobile_page_objects.bill_pay_page import MobileBillPayPage
    context.mobile_bill_pay_page = MobileBillPayPage(context.mobile_driver)
    
    assert context.mobile_bill_pay_page.is_bill_pay_page_displayed(), "Bill pay page not displayed"
    context.logger.info("Navigated to bill payment screen")

@when('I select "{payee_name}" as the payee')
def step_impl(context, payee_name):
    context.mobile_bill_pay_page.select_payee(payee_name)
    context.logger.info(f"Selected payee: {payee_name}")

@when('I set the payment date to {days:d} days from today')
def step_impl(context, days):
    payment_date = datetime.date.today() + datetime.timedelta(days=days)
    formatted_date = payment_date.strftime("%m/%d/%Y")
    
    context.payment_date = payment_date
    context.mobile_bill_pay_page.set_payment_date(formatted_date)
    context.logger.info(f"Set payment date to {formatted_date} ({days} days from today)")

@when('I confirm the bill payment')
def step_impl(context):
    context.mobile_bill_pay_page.tap_confirm_payment()
    context.logger.info("Confirmed bill payment")

@then('I should see a confirmation with a reference number')
def step_impl(context):
    success = context.mobile_bill_pay_page.is_confirmation_displayed()
    assert success, "Bill payment confirmation not displayed"
    
    context.payment_reference = context.mobile_bill_pay_page.get_confirmation_reference()
    assert context.payment_reference, "Payment reference number not displayed"
    
    context.logger.info(f"Bill payment successful with reference: {context.payment_reference}")

@then('the payment should be scheduled for the correct date')
def step_impl(context):
    scheduled_date = context.mobile_bill_pay_page.get_scheduled_payment_date()
    expected_date = context.payment_date.strftime("%m/%d/%Y")
    
    assert_that(scheduled_date, equal_to(expected_date))
    context.logger.info(f"Verified payment is scheduled for {scheduled_date}")

@then('my checking account should show a pending payment of ${amount:f}')
def step_impl(context, amount):
    # Navigate to account details to verify pending payment
    context.mobile_bill_pay_page.tap_done_button()
    context.mobile_dashboard.tap_accounts_tab()
    
    from mobile_page_objects.accounts_page import MobileAccountsPage
    accounts_page = MobileAccountsPage(context.mobile_driver)
    accounts_page.select_checking_account()
    
    from mobile_page_objects.account_details_page import MobileAccountDetailsPage
    details_page = MobileAccountDetailsPage(context.mobile_driver)
    
    # Check pending transactions
    pending_transactions = details_page.get_pending_transactions()
    
    payment_found = False
    for transaction in pending_transactions:
        if transaction.get_amount() == Decimal(str(amount)) and "payment" in transaction.get_description().lower():
            payment_found = True
            break
    
    assert payment_found, f"Pending payment of ${amount} not found in transactions"
    context.logger.info(f"Verified pending payment of ${amount} is displayed")
