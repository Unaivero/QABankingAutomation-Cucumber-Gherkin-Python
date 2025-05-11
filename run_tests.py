#!/usr/bin/env python3
"""
Test runner script with various options for test execution and reporting
"""

import os
import sys
import argparse
import subprocess
import json
import shutil
from datetime import datetime

def setup_directories():
    """Set up required directories"""
    directories = [
        'reports',
        'reports/allure-results',
        'reports/screenshots',
        'reports/junit',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")

def generate_test_data():
    """Generate test data if needed"""
    try:
        # Import the generator module and generate data
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        from utils.data_generator import DataGenerator
        generator = DataGenerator()
        generator.generate_test_data_set()
        print("Test data generated successfully")
    except Exception as e:
        print(f"Error generating test data: {e}")
        sys.exit(1)

def run_behave(args):
    """Run behave with the specified arguments"""
    behave_cmd = ['behave']
    
    # Add tags if specified
    if args.tags:
        behave_cmd.extend(['--tags', args.tags])
    
    # Add specific feature if specified
    if args.feature:
        behave_cmd.append(args.feature)
    
    # Add formatter based on report type
    if args.report == 'allure':
        behave_cmd.extend(['-f', 'allure_behave.formatter:AllureFormatter', '-o', 'reports/allure-results'])
    elif args.report == 'junit':
        behave_cmd.extend(['-f', 'junit', '-o', 'reports/junit'])
    
    # Add additional behave arguments
    if args.behave_args:
        behave_cmd.extend(args.behave_args.split())
    
    # Print command being run
    print(f"Running: {' '.join(behave_cmd)}")
    
    # Run behave
    process = subprocess.run(behave_cmd)
    return process.returncode

def generate_report(args):
    """Generate the report after running tests"""
    if args.report == 'allure':
        print("Generating Allure report...")
        
        # Check if allure command is available
        try:
            subprocess.run(['allure', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Allure command not found. Please ensure Allure is installed and in your PATH.")
            print("You can install it from: https://docs.qameta.io/allure/")
            return
        
        # Generate and open the report
        subprocess.run(['allure', 'generate', 'reports/allure-results', '-o', 'reports/allure-report', '--clean'])
        
        if not args.no_open:
            print("Opening Allure report in browser...")
            subprocess.run(['allure', 'open', 'reports/allure-report'])
    
    elif args.report == 'junit':
        print("JUnit XML reports saved to reports/junit directory.")
        print("You can view these reports with any JUnit-compatible viewer.")

def main():
    parser = argparse.ArgumentParser(description='Run banking automation tests')
    parser.add_argument('--feature', help='Specific feature file to run')
    parser.add_argument('--tags', help='Behave tags to include (e.g. "@smoke,@security")')
    parser.add_argument('--report', choices=['allure', 'junit', 'none'], default='allure', 
                        help='Report type to generate (default: allure)')
    parser.add_argument('--generate-data', action='store_true', help='Generate test data before running tests')
    parser.add_argument('--no-open', action='store_true', help='Do not open report automatically')
    parser.add_argument('--behave-args', help='Additional arguments to pass to behave')
    parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome',
                        help='Browser to use for tests (default: chrome)')
    parser.add_argument('--env', choices=['test', 'dev', 'staging', 'prod'], default='test',
                        help='Environment to run tests against (default: test)')
    
    args = parser.parse_args()
    
    # Set up environment variables
    os.environ['TEST_BROWSER'] = args.browser
    os.environ['TEST_ENV'] = args.env
    
    # Setup directories
    setup_directories()
    
    # Generate test data if requested
    if args.generate_data:
        generate_test_data()
    
    # Run the tests
    returncode = run_behave(args)
    
    # Generate report if not disabled
    if args.report != 'none':
        generate_report(args)
    
    sys.exit(returncode)

if __name__ == '__main__':
    main()
