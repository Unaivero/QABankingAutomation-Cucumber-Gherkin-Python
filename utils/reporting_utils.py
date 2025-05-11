import os
import json
import datetime
import logging
import requests
from PIL import Image
from io import BytesIO

class ReportingUtils:
    """
    Utility class for test reporting functions, including:
    - Screenshot capture
    - Test results logging
    - Report generation helpers
    """
    
    def __init__(self):
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        self.screenshots_dir = os.path.join(self.reports_dir, 'screenshots')
        self.logger = logging.getLogger('reporting')
        
        # Create directories if they don't exist
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def take_screenshot(self, driver, scenario_name, step_name=None):
        """
        Take a screenshot and save it to the screenshots directory
        
        :param driver: Selenium WebDriver instance
        :param scenario_name: Name of the scenario
        :param step_name: Optional name of the step
        :return: Path to the saved screenshot
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario_name = self._sanitize_filename(scenario_name)
        
        if step_name:
            step_name = self._sanitize_filename(step_name)
            filename = f"{timestamp}_{scenario_name}_{step_name}.png"
        else:
            filename = f"{timestamp}_{scenario_name}.png"
        
        file_path = os.path.join(self.screenshots_dir, filename)
        
        try:
            driver.save_screenshot(file_path)
            self.logger.info(f"Screenshot saved to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def _sanitize_filename(self, name):
        """
        Sanitize a string to be used as a filename
        
        :param name: Name to sanitize
        :return: Sanitized name
        """
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        
        # Remove invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '')
        
        # Limit length
        return name[:50]
    
    def capture_full_page_screenshot(self, driver, scenario_name, step_name=None):
        """
        Take a screenshot of the entire page (even parts not visible in viewport)
        
        :param driver: Selenium WebDriver instance
        :param scenario_name: Name of the scenario
        :param step_name: Optional name of the step
        :return: Path to the saved screenshot
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario_name = self._sanitize_filename(scenario_name)
        
        if step_name:
            step_name = self._sanitize_filename(step_name)
            filename = f"{timestamp}_{scenario_name}_{step_name}_full.png"
        else:
            filename = f"{timestamp}_{scenario_name}_full.png"
        
        file_path = os.path.join(self.screenshots_dir, filename)
        
        try:
            # Get the total height of the page
            total_width = driver.execute_script("return document.body.offsetWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            viewport_width = driver.execute_script("return document.body.clientWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            
            # Scroll through the page and take screenshots
            rectangles = []
            i = 0
            while i < total_height:
                j = 0
                while j < total_width:
                    driver.execute_script(f"window.scrollTo({j}, {i})")
                    driver.implicitly_wait(2)
                    
                    rectangles.append((j, i, viewport_width, viewport_height))
                    j += viewport_width
                i += viewport_height
            
            # Create a blank canvas
            stitched_image = Image.new('RGB', (total_width, total_height))
            
            # Take screenshots and stitch them together
            for i, rect in enumerate(rectangles):
                driver.execute_script(f"window.scrollTo({rect[0]}, {rect[1]})")
                driver.implicitly_wait(1)
                
                screenshot = driver.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                
                # Add the screenshot to the canvas
                box = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
                stitched_image.paste(screenshot, box)
            
            # Save the stitched image
            stitched_image.save(file_path)
            self.logger.info(f"Full page screenshot saved to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to take full page screenshot: {e}")
            return None
    
    def log_api_request(self, method, url, headers=None, data=None, json_data=None):
        """
        Log API request details
        
        :param method: HTTP method
        :param url: URL
        :param headers: Request headers
        :param data: Form data
        :param json_data: JSON data
        """
        request_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "method": method,
            "url": url,
            "headers": headers,
            "data": data,
            "json": json_data
        }
        
        log_path = os.path.join(self.reports_dir, 'api_logs.json')
        
        try:
            # Load existing logs if the file exists
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add the new log entry
            logs.append({"request": request_data})
            
            # Save logs
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to log API request: {e}")
    
    def log_api_response(self, response, request_details=None):
        """
        Log API response details
        
        :param response: Response object
        :param request_details: Optional request details
        """
        try:
            # Get response content as text
            if isinstance(response, requests.Response):
                status_code = response.status_code
                headers = dict(response.headers)
                
                # Try to parse response as JSON, if possible
                try:
                    content = response.json()
                except Exception:
                    content = response.text
            else:
                status_code = getattr(response, 'status_code', None)
                headers = getattr(response, 'headers', {})
                content = getattr(response, 'content', str(response))
            
            response_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "status_code": status_code,
                "headers": headers,
                "content": content
            }
            
            log_path = os.path.join(self.reports_dir, 'api_logs.json')
            
            # Load existing logs if the file exists
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add the new log entry or update the last one if it matches the request
            if request_details and logs:
                last_log = logs[-1]
                if last_log.get('request', {}).get('url') == request_details.get('url'):
                    last_log['response'] = response_data
                    logs[-1] = last_log
                else:
                    logs.append({"response": response_data})
            else:
                logs.append({"response": response_data})
            
            # Save logs
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to log API response: {e}")
    
    def create_execution_summary(self, result_data):
        """
        Create a summary of test execution results
        
        :param result_data: Test result data
        :return: Path to the summary file
        """
        summary = {
            "execution_time": datetime.datetime.now().isoformat(),
            "summary": {
                "total": result_data.get('total', 0),
                "passed": result_data.get('passed', 0),
                "failed": result_data.get('failed', 0),
                "skipped": result_data.get('skipped', 0),
                "duration": result_data.get('duration', 0)
            },
            "failures": result_data.get('failures', [])
        }
        
        summary_path = os.path.join(self.reports_dir, 'execution_summary.json')
        
        try:
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            self.logger.info(f"Execution summary saved to {summary_path}")
            return summary_path
        except Exception as e:
            self.logger.error(f"Failed to create execution summary: {e}")
            return None
