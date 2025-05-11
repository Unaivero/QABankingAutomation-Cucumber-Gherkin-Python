Feature: Account Transactions
  As a bank customer
  I want to perform various financial transactions
  So that I can manage my money effectively

  Background:
    Given I am logged into my bank account
    And I have an active checking account with balance of $5000.00

  @transaction @smoke
  Scenario: View transaction history
    When I navigate to the transaction history page
    Then I should see a list of my recent transactions
    And each transaction should display date, description, and amount
    And the transactions should be sorted by date in descending order

  @transaction @transfer
  Scenario: Transfer money between own accounts
    Given I have a savings account with balance of $10000.00
    When I initiate a transfer of $2000.00 from checking to savings account
    And I confirm the transfer
    Then I should see a success message
    And my checking account balance should be $3000.00
    And my savings account balance should be $12000.00
    And the transaction should appear in my transaction history

  @transaction @payment
  Scenario Outline: Bill payment with different amounts
    Given I have a payee "<payee>" set up in my account
    When I navigate to the bill payment page
    And I select payee "<payee>"
    And I enter payment amount of $<amount>
    And I set the payment date to <date>
    And I confirm the payment
    Then I should see a confirmation message with reference number
    And my checking account balance should be $<new_balance>

    Examples:
      | payee              | amount | date       | new_balance |
      | Electric Company   | 150.00 | 2025-05-20 | 4850.00     |
      | Water Utility      | 75.50  | 2025-05-25 | 4924.50     |
      | Internet Provider  | 89.99  | 2025-05-15 | 4910.01     |

  @transaction @regulatory
  Scenario: Large transaction requiring additional verification
    When I initiate a transfer of $9500.00 to an external account
    Then I should be prompted for additional verification
    And I should see information about regulatory requirements for large transactions
    When I complete the additional verification
    Then the transaction should be marked as "Pending Review"
