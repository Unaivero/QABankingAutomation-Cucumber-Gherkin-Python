import requests
import json
import os
import logging
from json import JSONDecodeError

class APIClient:
    """
    Base API client for making requests to the bank API
    """
    
    def __init__(self, base_url=None, token=None):
        """
        Initialize the API client
        
        :param base_url: Base URL for the API
        :param token: Authentication token
        """
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.base_url = base_url if base_url else self.config.get('api_base_url')
        self.token = token
        self.timeout = (
            self.config.get('api_timeouts', {}).get('connect', 5),
            self.config.get('api_timeouts', {}).get('read', 10)
        )
        self.logger = logging.getLogger('api_client')
    
    def authenticate(self, username, password):
        """
        Authenticate and get a token
        
        :param username: Username
        :param password: Password
        :return: Authentication response
        """
        endpoint = f"{self.base_url}/auth/login"
        payload = {"username": username, "password": password}
        
        self.logger.info(f"Authenticating user: {username}")
        
        response = requests.post(endpoint, json=payload, timeout=self.timeout)
        if response.status_code == 200:
            self.token = response.json().get('token')
            self.logger.info("Authentication successful")
        else:
            self.logger.error(f"Authentication failed: {response.status_code} - {response.text}")
        
        return response
    
    def get_headers(self):
        """
        Get HTTP headers for API requests
        
        :return: Dictionary of headers
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"
        
        return headers
    
    def get(self, endpoint, params=None):
        """
        Make a GET request
        
        :param endpoint: API endpoint
        :param params: Query parameters
        :return: API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self.logger.debug(f"GET request: {url}")
        
        response = requests.get(
            url, 
            params=params, 
            headers=self.get_headers(),
            timeout=self.timeout
        )
        
        self._log_response(response)
        return response
    
    def post(self, endpoint, data=None, json_data=None):
        """
        Make a POST request
        
        :param endpoint: API endpoint
        :param data: Form data
        :param json_data: JSON data
        :return: API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self.logger.debug(f"POST request: {url}")
        
        response = requests.post(
            url, 
            data=data, 
            json=json_data, 
            headers=self.get_headers(),
            timeout=self.timeout
        )
        
        self._log_response(response)
        return response
    
    def put(self, endpoint, data=None, json_data=None):
        """
        Make a PUT request
        
        :param endpoint: API endpoint
        :param data: Form data
        :param json_data: JSON data
        :return: API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self.logger.debug(f"PUT request: {url}")
        
        response = requests.put(
            url, 
            data=data, 
            json=json_data, 
            headers=self.get_headers(),
            timeout=self.timeout
        )
        
        self._log_response(response)
        return response
    
    def delete(self, endpoint):
        """
        Make a DELETE request
        
        :param endpoint: API endpoint
        :return: API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self.logger.debug(f"DELETE request: {url}")
        
        response = requests.delete(
            url, 
            headers=self.get_headers(),
            timeout=self.timeout
        )
        
        self._log_response(response)
        return response
    
    def _log_response(self, response):
        """
        Log API response
        
        :param response: API response
        """
        log_msg = f"Response: {response.status_code}"
        
        if response.status_code >= 400:
            self.logger.error(log_msg)
            self.logger.error(f"Response body: {response.text}")
        else:
            self.logger.debug(log_msg)
            try:
                # Only log first 1000 chars of response body to avoid huge logs
                response_text = response.text[:1000]
                if len(response.text) > 1000:
                    response_text += "... (truncated)"
                self.logger.debug(f"Response body: {response_text}")
            except Exception as e:
                self.logger.debug(f"Could not log response body: {e}")
