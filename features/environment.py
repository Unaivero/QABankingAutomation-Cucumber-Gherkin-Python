from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import json
import logging
from datetime import datetime

# Setup logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'test_run_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('banking_tests')

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def before_all(context):
    context.logger = setup_logging()
    context.logger.info("Starting test execution")
    
    # Load configuration
    try:
        context.config_data = load_config()
        context.logger.info("Configuration loaded successfully")
    except Exception as e:
        context.logger.error(f"Error loading configuration: {e}")
        raise

    # Set up base URL
    if not context.config.userdata.get('base_url'):
        context.config.userdata['base_url'] = context.config_data.get('base_url', 'https://banking-app-test.example.com')

def before_feature(context, feature):
    context.logger.info(f"Starting feature: {feature.name}")

def before_scenario(context, scenario):
    context.logger.info(f"Starting scenario: {scenario.name}")
    
    # Get browser type from config
    browser_type = context.config.userdata.get('browser', 'chrome')
    context.logger.info(f"Using browser: {browser_type}")
    
    # Initialize webdriver based on browser type
    if browser_type.lower() == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if context.config_data.get('headless', False):
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        context.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    elif browser_type.lower() == 'firefox':
        firefox_options = webdriver.FirefoxOptions()
        if context.config_data.get('headless', False):
            firefox_options.add_argument('--headless')
        context.browser = webdriver.Firefox(service=webdriver.firefox.service.Service(GeckoDriverManager().install()), options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set window size and timeouts
    context.browser.maximize_window()
    context.browser.implicitly_wait(10)

def after_scenario(context, scenario):
    context.logger.info(f"Finished scenario: {scenario.name}")
    if hasattr(context, 'browser'):
        context.logger.info("Closing browser")
        context.browser.quit()

def after_feature(context, feature):
    context.logger.info(f"Finished feature: {feature.name}")

def after_all(context):
    context.logger.info("Test execution completed")
