Feature: Bank Account Login
  As a bank customer
  I want to securely login to my account
  So that I can access my banking services

  Background:
    Given the banking application is accessible

  @smoke @security
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid username "testuser" and password "SecureP@ss123"
    And I click the login button
    Then I should be redirected to the account dashboard
    And I should see my account summary

  @security
  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter invalid username "wronguser" and password "WrongP@ss123"
    And I click the login button
    Then I should see an error message "Invalid username or password"
    And I should remain on the login page

  @security
  Scenario Outline: Account lockout after multiple failed attempts
    Given I am on the login page
    When I attempt to login with username "<username>" and incorrect password "<password>" <attempts> times
    Then my account should be locked
    And I should see a message "Your account has been locked for security reasons"

    Examples:
      | username  | password      | attempts |
      | testuser1 | WrongPass123! | 3        |
      | testuser2 | BadPassword!  | 5        |

  @security @2fa
  Scenario: Two-factor authentication during login
    Given I am on the login page
    And I have 2FA enabled for my account
    When I enter valid username "2fauser" and password "SecureP@ss123"
    And I click the login button
    Then I should be prompted for a two-factor authentication code
    When I enter a valid authentication code
    Then I should be redirected to the account dashboard
