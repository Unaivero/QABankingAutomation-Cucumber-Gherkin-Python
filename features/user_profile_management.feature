Feature: User Profile Management
  As a bank customer
  I want to manage my user profile and security settings
  So that I can maintain my account securely and according to my preferences

  Background:
    Given I am logged into my online banking account
    And I navigate to the "Profile Management" section

  @profile @smoke
  Scenario: View user profile information
    When I select "Personal Information" from the profile menu
    Then I should see my profile information including:
      | Field          | Value                  |
      | Full Name      | John Doe               |
      | Email Address  | john.doe@example.com   |
      | Phone Number   | +1 (555) 123-4567      |
      | Mailing Address| 123 Main St, Anytown   |
    And the information should match my account details

  @profile @edit
  Scenario: Update contact information
    When I select "Contact Information" from the profile menu
    And I click the "Edit" button
    And I update the following information:
      | Field          | New Value                |
      | Email Address  | john.updated@example.com |
      | Phone Number   | +1 (555) 987-6543        |
    And I submit the changes
    Then I should see a success message
    And my contact information should be updated in the system
    And I should receive a confirmation email to both email addresses

  @profile @verification
  Scenario: Update email address with verification
    When I select "Contact Information" from the profile menu
    And I click the "Edit" button
    And I update my email address to "john.new@example.com"
    And I submit the changes
    Then I should be informed that email verification is required
    And a verification link should be sent to "john.new@example.com"
    When I follow the verification link
    Then my email address should be updated to "john.new@example.com"
    And I should receive a confirmation of the change

  @security @password
  Scenario: Change password successfully
    When I select "Security Settings" from the profile menu
    And I select "Change Password"
    And I enter my current password "OldP@ssw0rd123"
    And I enter a new password "NewP@ssw0rd456"
    And I confirm the new password "NewP@ssw0rd456"
    And I submit the password change
    Then I should see a success message
    And I should receive a password change confirmation email
    And I should be able to login with the new password

  @security @password @validation
  Scenario Outline: Password strength validation
    When I select "Security Settings" from the profile menu
    And I select "Change Password"
    And I enter my current password "CurrentP@ssw0rd"
    And I enter a new password "<password>"
    Then I should see the password strength indicator show "<strength>"
    And the following password requirements should be highlighted:
      | Requirement         | Status   |
      | Minimum length      | <length> |
      | Uppercase letter    | <upper>  |
      | Lowercase letter    | <lower>  |
      | Number              | <number> |
      | Special character   | <special>|

    Examples:
      | password      | strength | length | upper  | lower  | number | special |
      | pass          | Weak     | Failed | Failed | Passed | Failed | Failed  |
      | Password      | Weak     | Passed | Passed | Passed | Failed | Failed  |
      | Password1     | Medium   | Passed | Passed | Passed | Passed | Failed  |
      | Password1!    | Strong   | Passed | Passed | Passed | Passed | Passed  |
      | P@ssw0rd123$! | Very Strong | Passed | Passed | Passed | Passed | Passed  |

  @security @2fa
  Scenario: Enable two-factor authentication
    When I select "Security Settings" from the profile menu
    And I select "Two-Factor Authentication"
    And I click "Enable Two-Factor Authentication"
    Then I should see the setup instructions
    And I should see a QR code for my authenticator app
    When I scan the QR code with my authenticator app
    And I enter the verification code from my app
    Then two-factor authentication should be enabled for my account
    And I should receive a confirmation email
    And I should see backup recovery codes for my account

  @security @questions
  Scenario: Update security questions
    When I select "Security Settings" from the profile menu
    And I select "Security Questions"
    Then I should see my current security questions
    When I click "Edit Security Questions"
    And I update my security questions and answers:
      | Question                           | Answer       |
      | What was your first pet's name?    | Fluffy       |
      | What is your mother's maiden name? | Johnson      |
      | What was your first car?           | Toyota Camry |
    And I submit the changes
    Then my security questions should be updated
    And I should receive a confirmation of the changes

  @profile @preferences
  Scenario: Update notification preferences
    When I select "Notification Preferences" from the profile menu
    Then I should see my current notification settings
    When I update my preferences to:
      | Channel | Transaction Alerts | Security Alerts | Marketing Messages |
      | Email   | Yes                | Yes             | No                 |
      | SMS     | Yes                | Yes             | No                 |
      | Push    | Yes                | Yes             | No                 |
    And I save my preferences
    Then my notification preferences should be updated
    And I should receive confirmation of the changes

  @profile @statements
  Scenario: Change statement delivery preference to paperless
    When I select "Statement Preferences" from the profile menu
    Then I should see my current statement delivery method
    When I select "Paperless Statements"
    And I confirm the change
    Then my statement preference should be updated to paperless
    And I should receive confirmation of the change
    And I should see information about accessing my statements online

  @security @devices
  Scenario: View and manage trusted devices
    When I select "Security Settings" from the profile menu
    And I select "Trusted Devices"
    Then I should see a list of devices that have accessed my account
    And each device should show last access date and location
    When I select a device and click "Remove"
    Then the device should be removed from my trusted devices
    And I should receive a confirmation email about the device removal
