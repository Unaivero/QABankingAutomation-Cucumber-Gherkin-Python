# Banking Automation Framework

A Python-based test automation framework for banking applications using Behave (Cucumber for Python) with Gherkin.

## 📋 Overview

This framework provides a comprehensive solution for testing banking applications with a focus on:

- Behavior-Driven Development (BDD) using Gherkin and Behave
- Strong security testing capabilities
- Regulatory compliance verification
- Multi-layered testing (UI, API, database)
- Rich reporting

## 🔑 Key Features

- **BDD Approach**: Tests written in Gherkin for better collaboration with business stakeholders
- **Page Object Model**: Clean separation of test logic and UI interactions
- **Parallel Test Execution**: Improved test execution speed
- **Security Testing**: Specialized utilities for security validation
- **Data Generation**: Realistic test data generation for banking scenarios
- **Cross-Browser Testing**: Support for Chrome, Firefox
- **API Testing**: Integrated API clients for backend validation
- **Robust Reporting**: Allure reporting for detailed test results

## 🏗 Project Structure

```
QABankingAutomation-Cucumber-Gherkin-Python/
├── features/                # Gherkin feature files
│   ├── steps/               # Step definitions
│   └── environment.py       # Behave environment setup
├── page_objects/            # Page Object classes
├── api_clients/             # API client classes
├── utils/                   # Utility functions and helpers
├── config/                  # Configuration files
├── test_data/               # Test data files
├── reports/                 # Test reports directory
└── requirements.txt         # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Chrome/Firefox browser
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/QABankingAutomation-Cucumber-Gherkin-Python.git
   cd QABankingAutomation-Cucumber-Gherkin-Python
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Update the configuration in `config/config.json`
2. Generate test data (optional):
   ```
   python utils/data_generator.py
   ```

### Running Tests

Run all tests:
```
behave
```

Run specific feature:
```
behave features/account_login.feature
```

Run with tags:
```
behave --tags=@smoke
```

Generate Allure report:
```
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results
```

## 🧪 Test Examples

### Account Login (Gherkin)

```gherkin
Feature: Bank Account Login
  As a bank customer
  I want to securely login to my account
  So that I can access my banking services

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid username "testuser" and password "SecureP@ss123"
    And I click the login button
    Then I should be redirected to the account dashboard
    And I should see my account summary
```

### Fund Transfer (Gherkin)

```gherkin
Feature: Account Transactions
  As a bank customer
  I want to perform various financial transactions
  So that I can manage my money effectively

  Scenario: Transfer money between own accounts
    Given I am logged into my bank account
    And I have a checking account with balance of $5000.00
    And I have a savings account with balance of $10000.00
    When I initiate a transfer of $2000.00 from checking to savings account
    And I confirm the transfer
    Then I should see a success message
    And my checking account balance should be $3000.00
    And my savings account balance should be $12000.00
```

## 🔒 Security Testing

The framework includes specialized utilities for security testing:

- Two-factor authentication testing
- Secure credential management
- Session management tests
- Cross-site scripting (XSS) checks
- SQL injection tests
- Encryption verification

## 📊 Reporting

Test results are presented using Allure reports, offering:

- Detailed test execution statistics
- Step-by-step test visualization
- Screenshot captures on failures
- Environment information
- History of test runs

## 🌐 API Testing

In addition to UI testing, the framework supports API testing with:

- REST API clients for all banking endpoints
- Request/response validation
- Authentication handling
- Error scenario testing

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
