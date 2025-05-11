from api_clients.api_client import APIClient
import json
import logging

class UserManagementAPI(APIClient):
    """
    API client for user management endpoints
    """
    
    def __init__(self, base_url=None, token=None):
        super().__init__(base_url, token)
        self.logger = logging.getLogger('user_management_api')
    
    def get_user_profile(self, user_id=None):
        """
        Get user profile information
        
        :param user_id: Optional user ID (defaults to current authenticated user)
        :return: API response
        """
        endpoint = 'users/profile'
        if user_id:
            endpoint = f'users/{user_id}/profile'
        
        self.logger.info(f"Getting user profile for {'current user' if not user_id else user_id}")
        return self.get(endpoint)
    
    def update_user_profile(self, profile_data):
        """
        Update user profile information
        
        :param profile_data: Dictionary of profile fields to update
        :return: API response
        """
        endpoint = 'users/profile'
        
        self.logger.info(f"Updating user profile with fields: {list(profile_data.keys())}")
        return self.put(endpoint, json_data=profile_data)
    
    def change_password(self, current_password, new_password):
        """
        Change user password
        
        :param current_password: Current password
        :param new_password: New password
        :return: API response
        """
        endpoint = 'users/password'
        payload = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        
        self.logger.info("Initiating password change request")
        return self.post(endpoint, json_data=payload)
    
    def create_user(self, user_data):
        """
        Create a new user account (admin function)
        
        :param user_data: User data including username, password, email, etc.
        :return: API response
        """
        endpoint = 'admin/users'
        
        self.logger.info(f"Creating new user: {user_data.get('username')}")
        return self.post(endpoint, json_data=user_data)
    
    def get_user_status(self, user_id):
        """
        Get user account status
        
        :param user_id: User ID
        :return: API response
        """
        endpoint = f'admin/users/{user_id}/status'
        
        self.logger.info(f"Getting status for user: {user_id}")
        return self.get(endpoint)
    
    def set_user_status(self, user_id, status, reason=None):
        """
        Set user account status (active, locked, suspended)
        
        :param user_id: User ID
        :param status: New status (active, locked, suspended)
        :param reason: Optional reason for status change
        :return: API response
        """
        endpoint = f'admin/users/{user_id}/status'
        payload = {
            "status": status
        }
        
        if reason:
            payload["reason"] = reason
        
        self.logger.info(f"Setting status for user {user_id} to {status}")
        return self.put(endpoint, json_data=payload)
    
    def request_password_reset(self, username_or_email):
        """
        Initiate password reset process
        
        :param username_or_email: Username or email
        :return: API response
        """
        endpoint = 'auth/password-reset'
        payload = {
            "identifier": username_or_email
        }
        
        self.logger.info(f"Requesting password reset for: {username_or_email}")
        return self.post(endpoint, json_data=payload)
    
    def complete_password_reset(self, token, new_password):
        """
        Complete password reset with token
        
        :param token: Reset token from email
        :param new_password: New password
        :return: API response
        """
        endpoint = 'auth/password-reset/confirm'
        payload = {
            "token": token,
            "newPassword": new_password
        }
        
        self.logger.info("Completing password reset")
        return self.post(endpoint, json_data=payload)
    
    def get_security_questions(self, username=None):
        """
        Get security questions for a user
        
        :param username: Optional username
        :return: API response
        """
        endpoint = 'auth/security-questions'
        params = {}
        
        if username:
            params["username"] = username
        
        self.logger.info(f"Getting security questions for {'current user' if not username else username}")
        return self.get(endpoint, params=params)
    
    def update_security_questions(self, questions_data):
        """
        Update security questions and answers
        
        :param questions_data: List of question/answer pairs
        :return: API response
        """
        endpoint = 'users/security-questions'
        
        self.logger.info(f"Updating security questions ({len(questions_data)} questions)")
        return self.put(endpoint, json_data=questions_data)
    
    def verify_security_question(self, question_id, answer):
        """
        Verify answer to security question
        
        :param question_id: Question ID
        :param answer: Answer to verify
        :return: API response
        """
        endpoint = 'auth/security-questions/verify'
        payload = {
            "questionId": question_id,
            "answer": answer
        }
        
        self.logger.info(f"Verifying answer for security question: {question_id}")
        return self.post(endpoint, json_data=payload)
    
    def enable_two_factor_auth(self):
        """
        Enable two-factor authentication for current user
        
        :return: API response with setup info (including QR code)
        """
        endpoint = 'users/2fa/enable'
        
        self.logger.info("Enabling two-factor authentication")
        return self.post(endpoint)
    
    def verify_two_factor_setup(self, verification_code):
        """
        Verify two-factor authentication setup with code
        
        :param verification_code: Code from authenticator app
        :return: API response
        """
        endpoint = 'users/2fa/verify'
        payload = {
            "code": verification_code
        }
        
        self.logger.info("Verifying two-factor authentication setup")
        return self.post(endpoint, json_data=payload)
    
    def disable_two_factor_auth(self, verification_code):
        """
        Disable two-factor authentication
        
        :param verification_code: Code from authenticator app
        :return: API response
        """
        endpoint = 'users/2fa/disable'
        payload = {
            "code": verification_code
        }
        
        self.logger.info("Disabling two-factor authentication")
        return self.post(endpoint, json_data=payload)
    
    def get_audit_log(self, user_id=None, params=None):
        """
        Get user activity audit log
        
        :param user_id: Optional user ID (defaults to current user)
        :param params: Optional parameters (date range, filters, etc.)
        :return: API response
        """
        endpoint = 'users/audit-log'
        if user_id:
            endpoint = f'admin/users/{user_id}/audit-log'
        
        self.logger.info(f"Getting audit log for {'current user' if not user_id else user_id}")
        return self.get(endpoint, params=params)
