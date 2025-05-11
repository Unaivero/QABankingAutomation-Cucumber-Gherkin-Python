Feature: Regulatory Compliance
  As a bank
  I want to ensure compliance with banking regulations
  So that we avoid penalties and protect customers

  Background:
    Given I am logged into my bank account as an administrator
    And the regulatory compliance module is enabled

  @regulatory @aml
  Scenario: Large transaction reporting
    Given I have a customer with account number "CHECKING-1234567890"
    When the customer initiates a cash deposit of $12,000
    Then the system should flag it as a large transaction
    And a Currency Transaction Report (CTR) should be generated
    And the transaction should be held for review

  @regulatory @aml
  Scenario: Suspicious activity detection
    Given I have a customer with the following transaction history:
      | date       | type      | amount   |
      | 2025-05-01 | Deposit   | $2,000   |
      | 2025-05-02 | Deposit   | $2,500   |
      | 2025-05-03 | Deposit   | $3,000   |
      | 2025-05-04 | Deposit   | $2,800   |
      | 2025-05-05 | Withdrawal| $9,500   |
    When the system runs the daily AML check
    Then a Suspicious Activity Report (SAR) should be triggered
    And the account should be flagged for review

  @regulatory @compliance
  Scenario: Customer identification verification
    Given I am creating a new customer account
    When I submit the application without a valid ID document
    Then the system should reject the application
    And I should see a message "Valid identification document required per KYC regulations"

  @regulatory @consent
  Scenario: Customer consent for data processing
    Given I am creating a new customer account
    When I complete the application form
    Then I should be presented with clear consent options for:
      | consent_type                 | required |
      | Terms and Conditions         | Yes      |
      | Privacy Policy               | Yes      |
      | Data Processing              | Yes      |
      | Marketing Communications     | No       |
      | Third-Party Data Sharing     | No       |
    And I cannot proceed without accepting the required consents

  @regulatory @audit
  Scenario: User activity audit trail
    Given I am logged in as an administrator
    When I update a customer's personal information
    Then the system should record in the audit log:
      | field            | information                   |
      | timestamp        | Current date and time         |
      | user_id          | My administrator ID           |
      | action           | "Updated customer information"|
      | affected_records | Customer ID                   |
      | changes_made     | Old and new values            |
      | ip_address       | My current IP address         |

  @regulatory @gdpr
  Scenario: Data subject access request
    Given I have a customer with account number "CHECKING-9876543210"
    When I process a data subject access request for this customer
    Then the system should generate a report containing:
      | data_category            |
      | Personal Information     |
      | Account Information      |
      | Transaction History      |
      | Communication History    |
      | Consent Records          |
    And the report should be available for download in a readable format

  @regulatory @data_retention
  Scenario: Data retention policy enforcement
    Given I have customer data that is 8 years old
    And our retention policy is set to 7 years for closed accounts
    When the nightly data retention job runs
    Then the outdated customer data should be anonymized or deleted
    And a compliance record of the data deletion should be created

  @regulatory @pci
  Scenario: Card data protection
    Given I am viewing a customer's payment card information
    Then the full card number should not be displayed
    And only the last 4 digits should be visible
    And when exported, the CSV file should not contain full card numbers

  @regulatory @sanctions
  Scenario: Sanctions list screening
    Given I have a new international wire transfer
    When the payment is for a recipient named "Blocked Entity Ltd"
    And the recipient country is on the sanctions list
    Then the transfer should be blocked
    And an alert should be sent to the compliance team
    And I should see a message "Transfer blocked due to sanctions compliance"
