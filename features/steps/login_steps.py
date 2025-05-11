from behave import given, when, then
from hamcrest import assert_that, equal_to, contains_string
import time
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage
from utils.security_utils import SecurityUtils


@given('the banking application is accessible')
def step_impl(context):
    context.browser.get(context.config.userdata.get('base_url'))
    # Verify the site is up by checking the title
    assert "Banking Application" in context.browser.title


@given('I am on the login page')
def step_impl(context):
    context.browser.get(context.config.userdata.get('base_url') + "/login")
    context.login_page = LoginPage(context.browser)
    assert context.login_page.is_login_page_displayed()


@when('I enter valid username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.login_page.enter_username(username)
    context.login_page.enter_password(password)


@when('I enter invalid username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.login_page.enter_username(username)
    context.login_page.enter_password(password)


@when('I click the login button')
def step_impl(context):
    context.login_page.click_login_button()


@then('I should be redirected to the account dashboard')
def step_impl(context):
    context.dashboard_page = DashboardPage(context.browser)
    assert context.dashboard_page.is_dashboard_displayed()


@then('I should see my account summary')
def step_impl(context):
    assert context.dashboard_page.is_account_summary_displayed()


@then('I should see an error message "{error_message}"')
def step_impl(context, error_message):
    actual_error = context.login_page.get_error_message()
    assert_that(actual_error, contains_string(error_message))


@then('I should remain on the login page')
def step_impl(context):
    assert context.login_page.is_login_page_displayed()


@when('I attempt to login with username "{username}" and incorrect password "{password}" {attempts:d} times')
def step_impl(context, username, password, attempts):
    for i in range(attempts):
        context.login_page.enter_username(username)
        context.login_page.enter_password(password)
        context.login_page.click_login_button()
        time.sleep(1)  # Small wait to allow for server response


@then('my account should be locked')
def step_impl(context):
    assert context.login_page.is_account_locked_message_displayed()


@given('I have 2FA enabled for my account')
def step_impl(context):
    # This would typically be set up in test data
    context.security_utils = SecurityUtils()
    context.totp_secret = context.security_utils.get_totp_secret_for_user("2fauser")


@then('I should be prompted for a two-factor authentication code')
def step_impl(context):
    assert context.login_page.is_2fa_input_displayed()


@when('I enter a valid authentication code')
def step_impl(context):
    # Generate valid TOTP code from the secret
    totp_code = context.security_utils.generate_totp_code(context.totp_secret)
    context.login_page.enter_2fa_code(totp_code)
    context.login_page.submit_2fa_code()
