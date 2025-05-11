Feature: Mobile Banking Features
  As a modern bank customer
  I want to access banking features on my mobile device
  So that I can manage my finances on the go

  Background:
    Given I have installed the MyBank mobile app
    And I have valid credentials for mobile banking

  @mobile @smoke
  Scenario: Login to mobile banking app
    When I open the mobile banking app
    And I enter my username "mobile_user@example.com"
    And I enter my password "MobileP@ss123"
    And I tap the login button
    Then I should be logged into the mobile app successfully
    And I should see the accounts dashboard

  @mobile @biometric
  Scenario: Login using biometric authentication
    Given I have enabled biometric authentication for my account
    When I open the mobile banking app
    And I tap "Login with Biometrics"
    And I confirm the biometric prompt
    Then I should be logged into the mobile app successfully
    And I should see the accounts dashboard

  @mobile @account
  Scenario: View account balances on mobile app
    Given I am logged into the mobile banking app
    When I navigate to the accounts screen
    Then I should see my checking account balance
    And I should see my savings account balance
    And I should see my credit card balance
    And the balances should be accurate and up-to-date

  @mobile @transaction
  Scenario: View recent transactions on mobile app
    Given I am logged into the mobile banking app
    When I navigate to the accounts screen
    And I select my checking account
    Then I should see a list of recent transactions
    And each transaction should display the date, merchant, and amount
    And I should be able to search transactions by merchant name

  @mobile @transfer @smoke
  Scenario: Transfer funds between accounts on mobile app
    Given I am logged into the mobile banking app
    And I have a checking account with balance of $2000.00
    And I have a savings account with balance of $5000.00
    When I navigate to the transfer screen
    And I select my checking account as the source account
    And I select my savings account as the destination account
    And I enter $500.00 as the transfer amount
    And I confirm the transfer
    Then I should see a success message
    And my checking account balance should be $1500.00
    And my savings account balance should be $5500.00

  @mobile @billpay
  Scenario: Pay a bill using the mobile app
    Given I am logged into the mobile banking app
    And I have a checking account with balance of $2000.00
    And I have a registered payee "Electric Company"
    When I navigate to the bill payment screen
    And I select "Electric Company" as the payee
    And I select my checking account as the source account
    And I enter $150.00 as the payment amount
    And I set the payment date to 5 days from today
    And I confirm the bill payment
    Then I should see a confirmation with a reference number
    And the payment should be scheduled for the correct date
    And my checking account should show a pending payment of $150.00

  @mobile @deposit
  Scenario: Mobile check deposit
    Given I am logged into the mobile banking app
    And I have a checking account with balance of $1000.00
    When I navigate to the deposit screen
    And I select my checking account for deposit
    And I enter $250.00 as the check amount
    And I capture the front image of the check
    And I capture the back image of the check
    And I confirm the check deposit
    Then I should see a success message for the deposit
    And the deposit should appear as pending in my transaction history
    And I should see a notification about the deposit hold period

  @mobile @card_control @security
  Scenario: Temporarily freeze credit card
    Given I am logged into the mobile banking app
    And I have an active credit card ending in "1234"
    When I navigate to the card management screen
    And I select my credit card ending in "1234"
    And I toggle the "Freeze Card" switch to ON
    Then I should see a confirmation that the card is frozen
    And the card status should be updated to "Frozen"
    When I toggle the "Freeze Card" switch to OFF
    Then I should see a confirmation that the card is unfrozen
    And the card status should be updated to "Active"

  @mobile @alert
  Scenario: Set up account alerts
    Given I am logged into the mobile banking app
    When I navigate to the alerts screen
    And I select "Low Balance Alert" for my checking account
    And I set the threshold amount to $100.00
    And I enable email notifications
    And I enable push notifications
    And I save the alert settings
    Then I should see a confirmation that the alert is set up
    And the alert should appear in my list of active alerts

  @mobile @location
  Scenario: Find nearby ATMs and branches
    Given I am logged into the mobile banking app
    And I have granted location permissions to the app
    When I navigate to the locations screen
    Then I should see a map showing nearby ATMs and branches
    And I should see a list of the closest locations with distances
    When I select "ATMs only" filter
    Then I should only see ATMs in the results
    When I search for a specific zip code "10001"
    Then I should see locations near that zip code

  @mobile @security
  Scenario: Update security settings
    Given I am logged into the mobile banking app
    When I navigate to the settings screen
    And I select "Security Settings"
    Then I should be able to enable or disable biometric login
    And I should be able to change my password
    And I should be able to update my security questions
    And I should be able to manage trusted devices

  @mobile @p2p
  Scenario: Send money to a contact
    Given I am logged into the mobile banking app
    And I have a checking account with balance of $1000.00
    And I have a saved contact "Jane Doe" with email "jane.doe@example.com"
    When I navigate to the send money screen
    And I select "Jane Doe" as the recipient
    And I select my checking account as the source account
    And I enter $50.00 as the payment amount
    And I enter "Lunch repayment" as the memo
    And I confirm the payment
    Then I should see a confirmation that the money was sent
    And my checking account balance should be $950.00
    And "Jane Doe" should receive a notification about the payment
