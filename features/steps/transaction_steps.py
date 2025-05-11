from behave import given, when, then
from hamcrest import assert_that, equal_to, is_not, empty, has_length, contains_string
from page_objects.dashboard_page import DashboardPage
from page_objects.transaction_page import TransactionPage
from page_objects.transfer_page import TransferPage
from page_objects.bill_payment_page import BillPaymentPage
from decimal import Decimal


@given('I am logged into my bank account')
def step_impl(context):
    # Setup precondition - user is already logged in
    context.browser.get(context.config.userdata.get('base_url'))
    # Use direct API call or DB setup to create test session
    context.dashboard_page = DashboardPage(context.browser)


@given('I have an active checking account with balance of ${balance:f}')
def step_impl(context, balance):
    # Store the balance for later verification
    context.checking_balance = Decimal(str(balance))
    # Setup via API or verify it's already set up
    assert context.dashboard_page.get_checking_balance() == context.checking_balance


@given('I have a savings account with balance of ${balance:f}')
def step_impl(context, balance):
    context.savings_balance = Decimal(str(balance))
    assert context.dashboard_page.get_savings_balance() == context.savings_balance


@when('I navigate to the transaction history page')
def step_impl(context):
    context.dashboard_page.click_transaction_history()
    context.transaction_page = TransactionPage(context.browser)


@then('I should see a list of my recent transactions')
def step_impl(context):
    transactions = context.transaction_page.get_transactions()
    assert_that(transactions, is_not(empty()))


@then('each transaction should display date, description, and amount')
def step_impl(context):
    for transaction in context.transaction_page.get_transactions():
        assert transaction.has_date()
        assert transaction.has_description()
        assert transaction.has_amount()


@then('the transactions should be sorted by date in descending order')
def step_impl(context):
    transactions = context.transaction_page.get_transactions()
    dates = [transaction.get_date() for transaction in transactions]
    sorted_dates = sorted(dates, reverse=True)
    assert_that(dates, equal_to(sorted_dates))


@when('I initiate a transfer of ${amount:f} from checking to savings account')
def step_impl(context, amount):
    context.transfer_amount = Decimal(str(amount))
    context.dashboard_page.click_transfer_funds()
    context.transfer_page = TransferPage(context.browser)
    context.transfer_page.select_from_account("Checking")
    context.transfer_page.select_to_account("Savings")
    context.transfer_page.enter_amount(context.transfer_amount)


@when('I confirm the transfer')
def step_impl(context):
    context.transfer_page.click_confirm_transfer()
    context.transfer_reference = context.transfer_page.get_confirmation_reference()


@then('I should see a success message')
def step_impl(context):
    assert context.transfer_page.is_success_message_displayed()


@then('my checking account balance should be ${balance:f}')
def step_impl(context, balance):
    expected_balance = Decimal(str(balance))
    # Navigate back to dashboard to check balance
    context.browser.get(context.config.userdata.get('base_url') + "/dashboard")
    context.dashboard_page = DashboardPage(context.browser)
    actual_balance = context.dashboard_page.get_checking_balance()
    assert_that(actual_balance, equal_to(expected_balance))


@then('my savings account balance should be ${balance:f}')
def step_impl(context, balance):
    expected_balance = Decimal(str(balance))
    actual_balance = context.dashboard_page.get_savings_balance()
    assert_that(actual_balance, equal_to(expected_balance))


@then('the transaction should appear in my transaction history')
def step_impl(context):
    context.dashboard_page.click_transaction_history()
    context.transaction_page = TransactionPage(context.browser)
    transactions = context.transaction_page.get_transactions()
    
    # Look for the transaction with matching reference number
    found = False
    for transaction in transactions:
        if context.transfer_reference in transaction.get_description():
            found = True
            break
    
    assert found, f"Transaction with reference {context.transfer_reference} not found"


@given('I have a payee "{payee}" set up in my account')
def step_impl(context, payee):
    # Verify or set up the payee
    assert context.dashboard_page.is_payee_set_up(payee)


@when('I navigate to the bill payment page')
def step_impl(context):
    context.dashboard_page.click_bill_pay()
    context.bill_payment_page = BillPaymentPage(context.browser)


@when('I select payee "{payee}"')
def step_impl(context, payee):
    context.bill_payment_page.select_payee(payee)


@when('I enter payment amount of ${amount:f}')
def step_impl(context, amount):
    context.payment_amount = Decimal(str(amount))
    context.bill_payment_page.enter_amount(context.payment_amount)


@when('I set the payment date to {date}')
def step_impl(context, date):
    context.bill_payment_page.set_payment_date(date)


@when('I confirm the payment')
def step_impl(context):
    context.bill_payment_page.click_confirm_payment()
    context.payment_reference = context.bill_payment_page.get_confirmation_reference()


@then('I should see a confirmation message with reference number')
def step_impl(context):
    assert context.bill_payment_page.is_confirmation_displayed()
    assert context.payment_reference is not None


@when('I initiate a transfer of ${amount:f} to an external account')
def step_impl(context, amount):
    context.dashboard_page.click_external_transfer()
    context.external_transfer_page = context.dashboard_page.get_external_transfer_page()
    context.external_transfer_page.enter_recipient_details("External Account")
    context.external_transfer_page.enter_amount(Decimal(str(amount)))


@then('I should be prompted for additional verification')
def step_impl(context):
    assert context.external_transfer_page.is_additional_verification_displayed()


@then('I should see information about regulatory requirements for large transactions')
def step_impl(context):
    regulatory_info = context.external_transfer_page.get_regulatory_information()
    assert_that(regulatory_info, contains_string("regulatory"))


@when('I complete the additional verification')
def step_impl(context):
    context.external_transfer_page.complete_additional_verification()


@then('the transaction should be marked as "{status}"')
def step_impl(context, status):
    actual_status = context.external_transfer_page.get_transaction_status()
    assert_that(actual_status, equal_to(status))
